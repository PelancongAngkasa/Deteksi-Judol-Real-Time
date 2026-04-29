# Deteksi Judol v2.0 - Quick Start Guide

**Status:** ✅ FULLY IMPLEMENTED
**Architecture:** PostgreSQL + FastAPI + Streamlit (Cortex XDR Style)
**Deployment:** Docker Compose (3 containers)

---

## 🚀 Quick Start (30 seconds)

```bash
# 1. Rename the new app
cd "c:\Users\Yusuf\Documents\Kerja\Kementan\Projek\Deteksi Judol Real Time"
move app.py app_old.py
move app_v2.py app.py

# 2. Start everything with Docker Compose
docker-compose up -d

# 3. Access dashboard
# Open browser: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

Wait 30 seconds for PostgreSQL to initialize, then visit the dashboard!

---

## 📋 What's New in v2.0

### ✅ Database Layer
- **PostgreSQL** persistent storage
- 7 optimized tables with indexes
- Connection pooling (20 connections)
- Automatic schema creation

### ✅ FastAPI Backend
- **10+ REST API endpoints**
- Background task scheduler (every 10 minutes)
- Automatic scanning with no manual intervention
- 5-minute dashboard cache for performance

### ✅ Streamlit Dashboard
- **Enterprise Cortex XDR-style design**
- Dark theme with red threat indicators
- 4-tab interface:
  - Dashboard (metrics + timeline)
  - Recent Threats (detection list)
  - Analytics (advanced charts)
  - Settings (auto-scan control)
- **White overlay effect** on results
- Empty-state templates for fresh installations

### ✅ Automatic Scanning
- Runs every 10 minutes in background
- No manual button needed (though optional manual scan available)
- Automatic database persistence
- Real-time dashboard updates

---

## 📁 New Files Created

```
✅ database.py           - SQLAlchemy ORM models (7 tables)
✅ api.py                - FastAPI backend with auto-scan scheduler
✅ schemas.py            - Pydantic models for API responses
✅ app_v2.py             - New Cortex XDR dashboard (rename to app.py)
✅ Dockerfile.api        - Docker image for API service
✅ docker-compose.yml    - Updated with PostgreSQL + API + Streamlit
✅ requirements.txt      - Updated with new dependencies
✅ .env.example          - Configuration template
✅ DEPLOYMENT_V2.md      - Full deployment documentation
✅ QUICKSTART_V2.md      - This file
```

---

## 🏗️ Architecture Overview

```
Streamlit Dashboard (Port 8501)
        ↓ HTTP REST Calls
FastAPI Backend (Port 8000)
        ↓ SQL Queries
PostgreSQL Database (Port 5432)
        ↓ Storage
Persistent Volume
```

### Auto-Scan Flow
```
1. FastAPI Background Scheduler
   ↓ (Every 10 minutes)
2. Load all active websites from database
   ↓
3. Call DeteksiJudol.scan_website() for each URL
   ↓
4. Store results in database:
   - Scan record
   - Detection records (if threats found)
   - Hourly statistics update
   ↓
5. Clear dashboard cache
   ↓
6. Streamlit auto-refreshes (every 5 seconds)
```

---

## 🎯 Key Features

### 1. **Automatic Scanning**
- Default: Enabled
- Interval: Every 10 minutes
- Runs in background (no interaction needed)
- Database persistence
- Control: Settings tab → Toggle

### 2. **Real-Time Dashboard**
- Auto-refreshes every 5 seconds
- Shows latest threats
- 24-hour activity timeline
- Detection rate gauge
- Threat level indicators

### 3. **Manual Scanning**
- Settings tab → Manual Scan section
- Enter custom URLs
- Trigger on-demand
- Results show immediately

### 4. **Enterprise UI**
- Cortex XDR-inspired design
- Dark theme (reduces eye strain)
- Red accent for threats
- Card-based layouts
- Responsive design

### 5. **White Overlay Effect**
- Results partially masked
- Hover to reveal
- Semi-transparent white overlay
- Backdrop blur effect

---

## 📊 Dashboard Tabs Explained

### Tab 1: Dashboard 🎯
- **Top Metrics** (4 cards):
  - Total websites monitoring
  - Threats detected today
  - Threats this hour
  - Auto-scan status

- **Charts**:
  - 24-hour threat timeline (line chart)
  - Detection rate (gauge)
  - Statistics breakdown (info boxes)

### Tab 2: Recent Threats 🚨
- List of latest detections (last 24 hours)
- Columns:
  - Time detected
  - Website ID
  - Keywords found
  - Severity level (Low/Medium/High)

- 10 most recent threats displayed
- Color-coded by severity

### Tab 3: Analytics 📈
- **Left chart**: Scan activity + detections trend
- **Right chart**: Detection rate per hour (%)
- 24-hour historical data
- Identifies patterns

### Tab 4: Settings ⚙️
- **Auto-Scan Toggle**:
  - Enable/Disable continuous scanning
  - Shows interval (10 minutes)
  - Reflects real-time status

- **Manual Scan Section**:
  - Text area for URL input (one per line)
  - Start button to trigger scan
  - Real-time progress
  - Results update after completion

---

## 🔌 API Endpoints (for developers)

### Health Check
```
GET /health
Response: {"status": "healthy", "timestamp": "...", "service": "Deteksi Judol API"}
```

### Dashboard Data
```
GET /api/v1/dashboard
Response: {
  "status": "success",
  "data": {
    "total_websites": 50,
    "total_detected_today": 3,
    "total_detected_this_hour": 1,
    "detection_rate": 6.0,
    "hourly_data": [...],
    "recent_detections": [...]
  }
}
```

### Trigger Manual Scan
```
POST /api/v1/scan/manual
Body: {
  "urls": ["https://example.com", ...],
  "priority": "urgent"
}
Response: {"status": "success", "message": "...", "results_count": 2}
```

### Toggle Auto-Scan
```
POST /api/v1/scan/toggle-auto?enabled=true
Response: {"status": "success", "auto_scan_enabled": true}
```

### Full API Documentation
```
http://localhost:8000/docs  (Interactive Swagger UI)
http://localhost:8000/redoc (ReDoc documentation)
```

---

## 🗄️ Database Tables

### websites
```sql
id, url, page_title, last_scan_time, status, created_at
```

### scans
```sql
id, website_id, scan_time, status_code, detected, keywords_count, 
suspect_urls_count, error, scan_duration
```

### detections
```sql
id, scan_id, website_id, keywords_found (JSON), suspect_urls (JSON),
page_title, severity, created_at
```

### hourly_statistics
```sql
id, hour, total_websites_scanned, total_detected, detection_rate, 
created_at, updated_at
```

### scan_schedule
```sql
id, auto_scan_enabled, scan_interval_minutes, last_scan_time, 
next_scan_time, is_scanning, created_at, updated_at
```

### dashboard_cache
```sql
id, cache_key, cache_data (JSON), created_at, updated_at, expires_at
```

### website_statuses
```sql
Possible values: "active", "inactive", "removed"
```

---

## ⚠️ Troubleshooting

### "❌ Gagal koneksi ke API Server"
**Problem:** Streamlit can't reach FastAPI
**Solution:**
```bash
# Check if API is running
docker-compose ps

# Check API logs
docker-compose logs api_server

# Ensure network is working
docker-compose exec api_server curl http://api_server:8000/health
```

### Auto-Scan not running
**Problem:** No new scans appearing
**Solution:**
```bash
# Check if auto-scan is enabled
# Dashboard → Settings → Auto-Scan status

# Check API logs
docker-compose logs -f api_server

# Force restart
docker-compose restart api_server
```

### Database connection error
**Problem:** "psycopg2.OperationalError"
**Solution:**
```bash
# Wait for PostgreSQL to start (takes 30 seconds)
docker-compose logs postgres_db

# Verify database is ready
docker-compose exec postgres_db pg_isready

# Recreate containers
docker-compose down -v
docker-compose up -d
```

---

## 🔐 Security Notes

- PostgreSQL password: Change in `.env` for production
- API runs on localhost by default
- CORS enabled for local development
- No authentication layer (add for production)
- SSL/TLS recommended for external access

---

## 📈 Performance Tips

### For Large URL Lists (1000+)
- Increase scan timeout: `SCAN_TIMEOUT_SECONDS=20`
- Increase scan interval: `SCAN_INTERVAL_MINUTES=15` (or 20)
- Enable database indexing (see DEPLOYMENT_V2.md)

### For Better Performance
- Clear old detection data (older than 30 days)
- Keep websites list under 500 active URLs
- Monitor database disk space

### Monitoring Queries
```sql
-- Check scan status
SELECT auto_scan_enabled, next_scan_time FROM scan_schedule;

-- Check detection count today
SELECT COUNT(*) FROM detections 
WHERE created_at >= NOW()::date;

-- Check database size
SELECT pg_size_pretty(pg_database_size('judol_db'));
```

---

## 📞 Support Commands

### Docker Operations
```bash
# View all services
docker-compose ps

# Check logs (all services)
docker-compose logs -f

# Restart specific service
docker-compose restart api_server

# Stop everything
docker-compose down

# Clean up volumes (CAREFUL!)
docker-compose down -v
```

### Database Operations
```bash
# Connect to PostgreSQL
docker-compose exec postgres_db psql -U judol_user -d judol_db

# Common queries
\dt              # List all tables
\d websites      # Describe table
SELECT COUNT(*) FROM scans;
```

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Get dashboard data
curl http://localhost:8000/api/v1/dashboard

# Get scan status
curl http://localhost:8000/api/v1/scan-status

# View full API docs
curl http://localhost:8000/openapi.json
```

---

## ✅ Deployment Checklist

- [ ] Rename app_v2.py to app.py
- [ ] Create .env file from .env.example
- [ ] Run `docker-compose up -d`
- [ ] Wait 30 seconds for PostgreSQL
- [ ] Access http://localhost:8501
- [ ] Upload website list (Sidebar → Load dari list_web.txt)
- [ ] Wait 10 minutes for first auto-scan
- [ ] Verify results in Dashboard tab

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com
- **Streamlit**: https://streamlit.io
- **SQLAlchemy**: https://www.sqlalchemy.org
- **Docker Compose**: https://docs.docker.com/compose
- **PostgreSQL**: https://www.postgresql.org

---

## 📝 Summary

You now have a **production-ready** monitoring system with:

✅ Enterprise-grade dashboard (Cortex XDR style)
✅ Automatic scanning every 10 minutes
✅ Persistent database storage
✅ REST API for integrations
✅ Real-time updates
✅ Historical analytics
✅ Docker deployment ready

**Next step:** `docker-compose up -d` and enjoy monitoring!

