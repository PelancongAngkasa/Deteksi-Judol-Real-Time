# Panduan Deployment Deteksi Judol v2.0

## Prasyarat
- Docker dan Docker Compose ter-install
- Python 3.11+ (untuk development lokal)
- PostgreSQL 15+ (jika menjalankan lokal tanpa Docker)

## Struktur Komponen Baru

### 1. **Database Layer** (`database.py`)
- SQLAlchemy ORM models
- PostgreSQL connection pooling
- 7 tabel untuk menyimpan:
  - `websites` - Daftar website yang dipantau
  - `scans` - Riwayat scan
  - `detections` - Detail deteksi threats
  - `hourly_statistics` - Statistik per jam
  - `scan_schedule` - Konfigurasi auto-scan
  - `dashboard_cache` - Cache untuk performa

### 2. **FastAPI Backend** (`api.py`)
- REST API dengan 10+ endpoints
- Background task scheduler (setiap 10 menit)
- Cache management untuk dashboard
- Automatic scanning tanpa manual intervention

#### Endpoints Utama:
```
GET  /health                    - Health check
GET  /api/v1/dashboard         - Dashboard data
GET  /api/v1/scan-status       - Status scanning
POST /api/v1/scan/manual       - Manual scan
POST /api/v1/scan/toggle-auto  - Toggle auto-scan
GET  /api/v1/detections        - List deteksi
POST /api/v1/websites/upload   - Upload URL list
```

### 3. **Streamlit Frontend** (`app_v2.py` → `app.py`)
- Enterprise Cortex XDR-style dashboard
- Dark theme dengan red accent untuk threats
- 4 tab utama:
  - Dashboard: Metrics & timeline chart
  - Recent Threats: List deteksi terbaru
  - Analytics: Advanced graphs
  - Settings: Kontrol auto-scan & manual scan
- White overlay effect pada results
- Automatic refresh setiap 5 detik

### 4. **Docker Orchestration**
Tiga services dalam docker-compose.yml:

1. **PostgreSQL** (port 5432)
   - Database storage
   - Volume untuk persistence
   - Health check built-in

2. **FastAPI** (port 8000)
   - Backend server
   - Auto-scan scheduler
   - Depends on: PostgreSQL

3. **Streamlit** (port 8501)
   - Web UI
   - Calls FastAPI backend
   - Depends on: FastAPI

## Deployment Steps

### Option A: Docker Compose (Recommended)

```bash
# 1. Clone/navigate ke project directory
cd "c:\Users\Yusuf\Documents\Kerja\Kementan\Projek\Deteksi Judol Real Time"

# 2. Rename app_v2.py to app.py
cp app_v2.py app.py

# 3. Create .env file
cp .env.example .env

# 4. Start all services
docker-compose up -d

# 5. Verify services are running
docker-compose ps
```

### Option B: Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python -c "from database import init_db; init_db()"

# 3. Start FastAPI in terminal 1
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# 4. Start Streamlit in terminal 2
streamlit run app.py --server.port=8501
```

## Post-Deployment

### Initialize Database
```bash
docker-compose exec api_server python -c "from database import init_db; init_db()"
```

### Upload Website List
```bash
# Via API
curl -X POST http://localhost:8000/api/v1/websites/upload?file_path=list_web.txt

# Or via Streamlit UI: Sidebar → "Load dari list_web.txt"
```

### Monitor Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api_server
docker-compose logs -f streamlit_app
docker-compose logs -f postgres_db
```

## Feature Highlights

### Auto-Scan (Automatic)
- Runs every 10 minutes automatically
- No manual intervention required
- Background scheduler using APScheduler
- Results stored in PostgreSQL
- Dashboard auto-updates

### Manual Scan
- Access via Settings tab in dashboard
- Trigger on-demand scans
- Custom URL input
- Real-time progress tracking

### Dashboard Features
1. **Real-time Metrics**
   - Total websites monitoring
   - Threats detected today
   - This hour's threats
   - Detection rate %

2. **Threat Timeline**
   - 24-hour activity graph
   - Detection rate gauge
   - Statistics breakdown

3. **Recent Detections**
   - Severity indicators
   - Keywords found
   - Time stamps
   - White overlay masking effect

4. **Analytics**
   - Scan activity trends
   - Detection patterns
   - Hourly breakdown

## Troubleshooting

### API Connection Error
```
❌ Gagal koneksi ke API Server
```
**Solution:**
- Ensure FastAPI is running: `docker-compose ps`
- Check logs: `docker-compose logs api_server`
- Verify DATABASE_URL in .env

### Database Connection Error
```
psycopg2.OperationalError: could not connect to server
```
**Solution:**
- Wait 30 seconds for PostgreSQL to start
- Check: `docker-compose logs postgres_db`
- Verify database is healthy: `docker-compose exec postgres_db pg_isready`

### Auto-Scan Not Running
```
Background task: Scan already in progress...
```
**Solution:**
- Check previous scan status in logs
- Restart API: `docker-compose restart api_server`
- Verify schedule: Check `scan_schedule` table

## Performance Tuning

### Database Optimization
```sql
-- Add indexes for better query performance
CREATE INDEX idx_detections_created ON detections(created_at DESC);
CREATE INDEX idx_scans_website_time ON scans(website_id, scan_time DESC);
```

### Cache Strategy
- Dashboard data cached for 5 minutes
- Clear cache on manual scan
- Use GET with cache-busting on refresh

### Scaling
- Database connection pooling (20 connections)
- Background task timeout: 300 seconds
- API response timeout: 30 seconds

## Architecture Diagram

```
┌─────────────────┐
│  Streamlit UI   │ (Port 8501)
│  (Cortex XDR    │
│   Dashboard)    │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   FastAPI       │ (Port 8000)
│   Backend       │
│   - REST API    │
│   - Scheduler   │
│   (every 10min) │
└────────┬────────┘
         │ SQL
         ▼
┌─────────────────┐
│  PostgreSQL     │ (Port 5432)
│  Database       │
│  - websites     │
│  - scans        │
│  - detections   │
│  - statistics   │
└─────────────────┘
```

## File Structure

```
Deteksi Judol Real Time/
├── app.py                    # ← Rename app_v2.py
├── app_v2.py                 # ← New Cortex XDR dashboard
├── api.py                    # ← New FastAPI backend
├── database.py               # ← New database models
├── schemas.py                # ← New Pydantic schemas
├── deteksi_judol.py          # (unchanged)
├── docker-compose.yml        # Updated for 3 services
├── Dockerfile                # Updated
├── Dockerfile.api            # New for API service
├── requirements.txt          # Updated dependencies
├── .env.example              # Environment template
└── list_web.txt              # Website list
```

## Next Steps

1. **Swap app files**: `mv app.py app_old.py && mv app_v2.py app.py`
2. **Create .env**: Copy `.env.example` to `.env`
3. **Deploy**: `docker-compose up -d`
4. **Access**:
   - Dashboard: http://localhost:8501
   - API Docs: http://localhost:8000/docs
   - API: http://localhost:8000

## Support & Monitoring

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Database**: Access via `docker-compose exec postgres_db psql -U judol_user -d judol_db`
- **Logs**: Real-time via `docker-compose logs -f`

