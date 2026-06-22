"""
Database models dan connection untuk sistem deteksi judol
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, JSON, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://judol_user:judol_pass@localhost:5432/judol_db")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Website(Base):
    """Model untuk menyimpan daftar website yang dipantau"""
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    page_title = Column(String, nullable=True)
    last_scan_time = Column(DateTime, nullable=True)
    status = Column(String, default="active")  # active, inactive, removed
    is_currently_detected = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scans = relationship("Scan", back_populates="website")
    detections = relationship("Detection", back_populates="website")


class Scan(Base):
    """Model untuk menyimpan riwayat scan"""
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    scan_time = Column(DateTime, default=datetime.utcnow, index=True)
    status_code = Column(Integer, nullable=True)
    detected = Column(Boolean, default=False, index=True)
    keywords_count = Column(Integer, default=0)
    suspect_urls_count = Column(Integer, default=0)
    error = Column(String, nullable=True)
    scan_duration = Column(Float, default=0)  # dalam detik
    
    # Relationships
    website = relationship("Website", back_populates="scans")
    detections = relationship("Detection", back_populates="scan")


class Detection(Base):
    """Model untuk menyimpan detail deteksi"""
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    website_id = Column(Integer, ForeignKey("websites.id"))
    keywords_found = Column(JSON)  # List of keywords
    suspect_urls = Column(JSON)  # List of suspect URLs
    page_title = Column(String)
    severity = Column(String, default="medium")  # low, medium, high
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    scan = relationship("Scan", back_populates="detections")
    website = relationship("Website", back_populates="detections")


class HourlyStatistic(Base):
    """Model untuk menyimpan statistik per jam"""
    __tablename__ = "hourly_statistics"

    id = Column(Integer, primary_key=True, index=True)
    hour = Column(DateTime, unique=True, index=True)
    total_websites_scanned = Column(Integer, default=0)
    total_detected = Column(Integer, default=0)
    detection_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DashboardCache(Base):
    """Model untuk cache data dashboard (untuk performa)"""
    __tablename__ = "dashboard_cache"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String, unique=True, index=True)
    cache_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class ScanSchedule(Base):
    """Model untuk konfigurasi jadwal scan"""
    __tablename__ = "scan_schedule"

    id = Column(Integer, primary_key=True, index=True)
    auto_scan_enabled = Column(Boolean, default=True)
    scan_interval_minutes = Column(Integer, default=10)  # Scan setiap 10 menit
    last_scan_time = Column(DateTime, nullable=True)
    next_scan_time = Column(DateTime, nullable=True)
    is_scanning = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def get_db():
    """Dependency untuk mendapatkan database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inisialisasi database - buat semua tables"""
    Base.metadata.create_all(bind=engine)

    # Migrasi kolom baru agar tidak perlu drop-recreate database lama
    from sqlalchemy import text
    migrations = [
        "ALTER TABLE websites ADD COLUMN IF NOT EXISTS is_currently_detected BOOLEAN DEFAULT FALSE",
    ]
    with engine.connect() as conn:
        for sql in migrations:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"Migration skipped (may already exist): {e}")

    print("Database initialized successfully!")
