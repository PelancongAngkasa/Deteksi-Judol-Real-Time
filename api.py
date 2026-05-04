"""
FastAPI backend untuk sistem deteksi judol dengan auto-scan
"""
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime, timedelta
import asyncio
import time
import json
from apscheduler.schedulers.background import BackgroundScheduler
from typing import List, Optional
import logging

from database import get_db, init_db, engine, SessionLocal
from database import Website, Scan, Detection, HourlyStatistic, ScanSchedule, DashboardCache
from schemas import (
    WebsiteResponse,
    ScanResponse, DashboardResponse, DashboardStatistics,
    DetectionResponse, HourlyStatisticResponse, ScanStatusResponse,
    ManualScanRequest, ManualScanResponse
)
from deteksi_judol import DeteksiJudol

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Deteksi Judol API",
    description="REST API untuk sistem deteksi defacement judol online",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global scheduler
scheduler = BackgroundScheduler()
detector = DeteksiJudol()


# ==================== STARTUP/SHUTDOWN EVENTS ====================

@app.on_event("startup")
async def startup_event():
    """Inisialisasi database dan start background scheduler"""
    logger.info("Starting up API server...")
    init_db()
    
    # Start scheduler
    scheduler.add_job(
        auto_scan_task,
        "interval",
        minutes=10,
        id="auto_scan",
        name="Auto Scan Task",
        misfire_grace_time=60
    )
    scheduler.start()
    logger.info("Auto-scan scheduler started (every 10 minutes)")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown scheduler"""
    logger.info("Shutting down API server...")
    scheduler.shutdown()


# ==================== BACKGROUND TASKS ====================

def auto_scan_task():
    """Background task untuk scan otomatis setiap 10 menit"""
    db = SessionLocal()
    try:
        logger.info("Starting auto-scan task...")
        
        # Get scan schedule
        schedule = db.query(ScanSchedule).first()
        if not schedule or not schedule.auto_scan_enabled:
            logger.info("Auto-scan is disabled")
            return
        
        if schedule.is_scanning:
            logger.info("Scan already in progress, skipping...")
            return
        
        # Mark as scanning
        schedule.is_scanning = True
        schedule.last_scan_time = datetime.utcnow()
        schedule.next_scan_time = datetime.utcnow() + timedelta(minutes=10)
        db.commit()
        
        # Get all active websites
        websites = db.query(Website).filter(Website.status == "active").all()
        if not websites:
            logger.warning("No active websites to scan")
            schedule.is_scanning = False
            db.commit()
            return
        
        urls = [w.url for w in websites]
        logger.info(f"Scanning {len(urls)} websites...")
        
        # Perform scan
        scan_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        hourly_stat = db.query(HourlyStatistic).filter(HourlyStatistic.hour == scan_hour).first()
        
        if not hourly_stat:
            hourly_stat = HourlyStatistic(hour=scan_hour)
            db.add(hourly_stat)
        
        total_detected = 0
        
        for url in urls:
            try:
                start_time = time.time()
                result = detector.scan_website(url)
                scan_duration = time.time() - start_time
                
                # Find or create website record
                website = db.query(Website).filter(Website.url == url).first()
                if not website:
                    website = Website(url=url, page_title=result.get('page_title'))
                    db.add(website)
                    db.flush()
                
                # Create scan record
                scan = Scan(
                    website_id=website.id,
                    status_code=result.get('status'),
                    detected=result.get('detected', False),
                    keywords_count=result.get('keywords_count', 0),
                    suspect_urls_count=len(result.get('suspect_urls', [])),
                    error=result.get('error'),
                    scan_duration=scan_duration
                )
                db.add(scan)
                db.flush()
                
                # Create detection record if found
                if result.get('detected'):
                    total_detected += 1
                    severity = "high" if result.get('keywords_count', 0) > 3 else "medium"
                    detection = Detection(
                        scan_id=scan.id,
                        website_id=website.id,
                        keywords_found=result.get('keywords_found', []),
                        suspect_urls=result.get('suspect_urls', []),
                        page_title=result.get('page_title'),
                        severity=severity
                    )
                    db.add(detection)
                
                # Update website last scan time
                website.last_scan_time = datetime.utcnow()
                db.add(website)
                
            except Exception as e:
                logger.error(f"Error scanning {url}: {str(e)}")
        
        # Update hourly statistics
        hourly_stat.total_websites_scanned = len(urls)
        hourly_stat.total_detected = total_detected
        hourly_stat.detection_rate = (total_detected / len(urls) * 100) if urls else 0
        hourly_stat.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Clear dashboard cache
        cache = db.query(DashboardCache).filter(DashboardCache.cache_key == "dashboard_main").first()
        if cache:
            db.delete(cache)
            db.commit()
        
        logger.info(f"Auto-scan completed: {len(urls)} websites scanned, {total_detected} threats detected")
        
    except Exception as e:
        logger.error(f"Error in auto_scan_task: {str(e)}")
    finally:
        # Mark as not scanning
        schedule = db.query(ScanSchedule).first()
        if schedule:
            schedule.is_scanning = False
            db.commit()
        db.close()


# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Deteksi Judol API"
    }


# ==================== DASHBOARD ENDPOINTS ====================

@app.get("/api/v1/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    """
    Get main dashboard data dengan cache
    """
    try:
        # Check cache
        cache = db.query(DashboardCache).filter(
            DashboardCache.cache_key == "dashboard_main",
            DashboardCache.expires_at > datetime.utcnow()
        ).first()
        
        if cache:
            logger.info("Dashboard data retrieved from cache")
            return DashboardResponse(
                status="success",
                data=DashboardStatistics(**json.loads(cache.cache_data))
            )
        
        # Get statistics
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        hour_start = now.replace(minute=0, second=0, microsecond=0)
        
        total_websites = db.query(Website).filter(Website.status == "active").count()
        
        # Total detected today (deduplicate per website)
        today_detections = (
            db.query(Detection.website_id)
            .filter(Detection.created_at >= today_start)
            .distinct()
            .count()
        )
        
        # Total detected this hour (deduplicate per website)
        hour_detections = (
            db.query(Detection.website_id)
            .filter(Detection.created_at >= hour_start)
            .distinct()
            .count()
        )
        
        # Get hourly statistics for last 24 hours
        hourly_stats = []
        for i in range(24, -1, -1):
            check_hour = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=i)
            stat = db.query(HourlyStatistic).filter(HourlyStatistic.hour == check_hour).first()
            if stat:
                hourly_stats.append(HourlyStatisticResponse.from_orm(stat))
            else:
                # Create empty stat for visualization
                hourly_stats.append(HourlyStatisticResponse(
                    hour=check_hour,
                    total_websites_scanned=0,
                    total_detected=0,
                    detection_rate=0.0,
                    created_at=check_hour,
                    updated_at=check_hour
                ))
        
        # Recent detections (deduplicate per website) with website URLs
        # So a website that's detected in consecutive scans doesn't keep inflating the list.
        recent_raw = db.query(Detection).order_by(desc(Detection.created_at)).limit(50).all()
        recent_detections = []
        seen_website_ids = set()
        for det in recent_raw:
            if det.website_id in seen_website_ids:
                continue
            website = db.query(Website).filter(Website.id == det.website_id).first()
            det_response = DetectionResponse.from_orm(det)
            det_response.website_url = website.url if website else f"ID: {det.website_id}"
            recent_detections.append(det_response)
            seen_website_ids.add(det.website_id)
            if len(recent_detections) >= 10:
                break
        
        # Get scan schedule
        schedule = db.query(ScanSchedule).first()
        if not schedule:
            schedule = ScanSchedule()
            db.add(schedule)
            db.commit()
        
        # Get last scan time
        last_scan = db.query(Scan).order_by(desc(Scan.scan_time)).first()
        last_scan_time = last_scan.scan_time if last_scan else None
        
        # Calculate detection rate
        detection_rate = (today_detections / total_websites * 100) if total_websites > 0 else 0
        
        # Prepare dashboard data
        dashboard_stats = DashboardStatistics(
            total_websites=total_websites,
            total_detected_today=today_detections,
            total_detected_this_hour=hour_detections,
            detection_rate=round(detection_rate, 2),
            last_scan_time=last_scan_time,
            auto_scan_enabled=schedule.auto_scan_enabled,
            next_scan_time=schedule.next_scan_time,
            hourly_data=hourly_stats,
            recent_detections=recent_detections
        )
        
        # Cache untuk 5 menit
        cache_data = DashboardCache(
            cache_key="dashboard_main",
            cache_data=dashboard_stats.model_dump_json(),
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        existing_cache = db.query(DashboardCache).filter(DashboardCache.cache_key == "dashboard_main").first()
        if existing_cache:
            existing_cache.cache_data = dashboard_stats.model_dump_json()
            existing_cache.expires_at = datetime.utcnow() + timedelta(minutes=5)
        else:
            db.add(cache_data)
        db.commit()
        
        return DashboardResponse(
            status="success",
            data=dashboard_stats
        )
        
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {str(e)}")
        return DashboardResponse(
            status="error",
            data=None,
            message=str(e)
        )


@app.get("/api/v1/scan-status", response_model=ScanStatusResponse)
async def get_scan_status(db: Session = Depends(get_db)):
    """Get current scan status"""
    schedule = db.query(ScanSchedule).first()
    if not schedule:
        schedule = ScanSchedule()
        db.add(schedule)
        db.commit()
    
    total_websites = db.query(Website).filter(Website.status == "active").count()
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    # Deduplicate per website so repeated scans don't inflate threats.
    total_detected_today = (
        db.query(Detection.website_id)
        .filter(Detection.created_at >= today_start)
        .distinct()
        .count()
    )
    
    return ScanStatusResponse(
        is_scanning=schedule.is_scanning,
        auto_scan_enabled=schedule.auto_scan_enabled,
        scan_interval_minutes=schedule.scan_interval_minutes,
        last_scan_time=schedule.last_scan_time,
        next_scan_time=schedule.next_scan_time,
        total_websites=total_websites,
        total_detected_today=total_detected_today
    )


# ==================== WEBSITE MANAGEMENT ====================

@app.get("/api/v1/websites", response_model=List[WebsiteResponse])
async def list_websites(db: Session = Depends(get_db)):
    """List semua website yang dipantau"""
    websites = db.query(Website).all()
    return websites


@app.delete("/api/v1/websites/{website_id}")
async def delete_website(website_id: int, db: Session = Depends(get_db)):
    """Hard delete target URL (Website) - removes all related data from database"""
    try:
        website = db.query(Website).filter(Website.id == website_id).first()
        if not website:
            raise HTTPException(status_code=404, detail="Website tidak ditemukan")
        
        # Delete all related detections
        db.query(Detection).filter(Detection.website_id == website_id).delete()
        
        # Delete all related scans
        db.query(Scan).filter(Scan.website_id == website_id).delete()
        
        # Delete website
        db.delete(website)
        db.commit()
        
        # Clear cache
        db.query(DashboardCache).filter(DashboardCache.cache_key == "dashboard_main").delete()
        db.commit()
        
        logger.info(f"Website {website_id} permanently deleted from database")
        return {
            "status": "success",
            "message": f"Website {website_id} permanently deleted",
        }
    except Exception as e:
        logger.error(f"Error deleting website: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SCAN CONTROL ====================

@app.post("/api/v1/scan/manual", response_model=ManualScanResponse)
async def trigger_manual_scan(request: ManualScanRequest, db: Session = Depends(get_db)):
    """Trigger manual scan untuk specific URLs"""
    try:
        schedule = db.query(ScanSchedule).first()
        if not schedule:
            schedule = ScanSchedule()
            db.add(schedule)
            db.commit()
        
        if schedule.is_scanning:
            return ManualScanResponse(
                status="error",
                message="Scan sudah dalam progress",
                results_count=0
            )
        
        # Run scan in background
        detected_count = 0
        for url in request.urls:
            try:
                result = detector.scan_website(url)
                
                # Find or create website
                website = db.query(Website).filter(Website.url == url).first()
                if not website:
                    website = Website(url=url, page_title=result.get('page_title'))
                    db.add(website)
                    db.flush()
                
                # Create scan record
                scan = Scan(
                    website_id=website.id,
                    status_code=result.get('status'),
                    detected=result.get('detected', False),
                    keywords_count=result.get('keywords_count', 0),
                    suspect_urls_count=len(result.get('suspect_urls', [])),
                    error=result.get('error')
                )
                db.add(scan)
                db.flush()
                
                if result.get('detected'):
                    detected_count += 1
                    detection = Detection(
                        scan_id=scan.id,
                        website_id=website.id,
                        keywords_found=result.get('keywords_found', []),
                        suspect_urls=result.get('suspect_urls', []),
                        page_title=result.get('page_title'),
                        severity="high" if result.get('keywords_count', 0) > 3 else "medium"
                    )
                    db.add(detection)
                
                website.last_scan_time = datetime.utcnow()
                
            except Exception as e:
                logger.error(f"Error scanning {url}: {str(e)}")
        
        db.commit()

        # Update hourly statistics from DB (so dashboard timeline/metrics reflect manual scans)
        now = datetime.utcnow()
        hour_start = now.replace(minute=0, second=0, microsecond=0)
        next_hour = hour_start + timedelta(hours=1)

        # Deduplicate per-website so repeated detections in the same hour
        # don't inflate "threats" counts.
        total_scanned_in_hour = (
            db.query(Scan.website_id)
            .filter(
                Scan.scan_time >= hour_start,
                Scan.scan_time < next_hour,
            )
            .distinct()
            .count()
        )

        total_detected_in_hour = (
            db.query(Detection.website_id)
            .filter(
                Detection.created_at >= hour_start,
                Detection.created_at < next_hour,
            )
            .distinct()
            .count()
        )

        hourly_stat = db.query(HourlyStatistic).filter(HourlyStatistic.hour == hour_start).first()
        if not hourly_stat:
            hourly_stat = HourlyStatistic(hour=hour_start)
            db.add(hourly_stat)

        hourly_stat.total_websites_scanned = total_scanned_in_hour
        hourly_stat.total_detected = total_detected_in_hour
        hourly_stat.detection_rate = (total_detected_in_hour / total_scanned_in_hour * 100) if total_scanned_in_hour > 0 else 0.0
        hourly_stat.updated_at = datetime.utcnow()
        db.add(hourly_stat)

        # Clear dashboard cache so GET /api/v1/dashboard recomputes immediately
        db.query(DashboardCache).filter(DashboardCache.cache_key == "dashboard_main").delete()
        db.commit()
        
        return ManualScanResponse(
            status="success",
            message=f"Manual scan completed: {detected_count} threats detected",
            results_count=len(request.urls)
        )
        
    except Exception as e:
        logger.error(f"Error in manual scan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/scan/toggle-auto")
async def toggle_auto_scan(enabled: bool, db: Session = Depends(get_db)):
    """Toggle auto-scan on/off"""
    schedule = db.query(ScanSchedule).first()
    if not schedule:
        schedule = ScanSchedule()
        db.add(schedule)
    
    schedule.auto_scan_enabled = enabled
    db.commit()
    
    return {
        "status": "success",
        "auto_scan_enabled": schedule.auto_scan_enabled,
        "message": "Auto-scan " + ("enabled" if enabled else "disabled")
    }


# ==================== CACHE & REFRESH ====================

@app.post("/api/v1/cache/clear")
async def clear_cache(db: Session = Depends(get_db)):
    """Clear dashboard cache"""
    try:
        db.query(DashboardCache).delete()
        db.commit()
        logger.info("Dashboard cache cleared")
        return {"status": "success", "message": "Cache cleared"}
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/websites/refresh")
async def refresh_websites(db: Session = Depends(get_db)):
    """Refresh websites dari list_web.txt, clear cache, dan trigger scan langsung"""
    try:
        # Load URLs dari file terbaru
        urls = detector.load_urls_from_file("list_web.txt")
        if not urls:
            raise HTTPException(status_code=400, detail="File kosong atau tidak ditemukan")
        
        # Clear cache
        db.query(DashboardCache).delete()
        
        # Count current websites
        current_count = db.query(Website).count()
        
        # Add new URLs
        added = 0
        new_urls = []
        for url in urls:
            existing = db.query(Website).filter(Website.url == url).first()
            if not existing:
                website = Website(url=url, status="active")
                db.add(website)
                new_urls.append(url)
                added += 1
        
        db.commit()
        new_count = db.query(Website).count()
        
        # Trigger immediate scan untuk semua URL (tidak hanya yang baru)
        logger.info(f"Websites refreshed: {current_count} -> {new_count} (added {added}). Starting immediate scan...")
        scan_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        hourly_stat = db.query(HourlyStatistic).filter(HourlyStatistic.hour == scan_hour).first()
        
        if not hourly_stat:
            hourly_stat = HourlyStatistic(hour=scan_hour)
            db.add(hourly_stat)
        
        total_detected = 0
        scanned_count = 0
        
        # Scan all active websites
        for url in urls:
            try:
                start_time = time.time()
                result = detector.scan_website(url)
                scan_duration = time.time() - start_time
                
                website = db.query(Website).filter(Website.url == url).first()
                if website:
                    # Create scan record
                    scan = Scan(
                        website_id=website.id,
                        scan_time=datetime.utcnow(),
                        status_code=result.get('status_code'),
                        detected=result.get('detected', False),
                        keywords_count=result.get('keywords_count', 0),
                        error=result.get('error'),
                        scan_duration=scan_duration
                    )
                    db.add(scan)
                    db.flush()
                    
                    # Create detection record if detected
                    if result.get('detected'):
                        detection = Detection(
                            scan_id=scan.id,
                            website_id=website.id,
                            keywords_found=result.get('keywords_found', []),
                            suspect_urls=result.get('suspect_urls', []),
                            page_title=result.get('page_title'),
                            severity="high" if result.get('keywords_count', 0) > 5 else "medium",
                            created_at=datetime.utcnow()
                        )
                        db.add(detection)
                        total_detected += 1
                    
                    scanned_count += 1
            except Exception as e:
                logger.error(f"Error scanning {url}: {e}")
                continue
        
        # Update hourly stats
        hourly_stat.total_websites_scanned = scanned_count
        hourly_stat.total_detected = total_detected
        if scanned_count > 0:
            hourly_stat.detection_rate = (total_detected / scanned_count) * 100
        
        db.commit()
        
        logger.info(f"Immediate scan completed: {scanned_count} scanned, {total_detected} detected")
        return {
            "status": "success",
            "total_urls": len(urls),
            "added": added,
            "current_total": new_count,
            "scanned": scanned_count,
            "detected": total_detected,
            "message": f"Refreshed from list_web.txt: added {added} new websites, scanned {scanned_count}, detected {total_detected} threats"
        }
    except Exception as e:
        logger.error(f"Error refreshing websites: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
