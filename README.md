# 🛡️ Deteksi Defacement Judol Online - Real-Time Enterprise Dashboard

Sistem monitoring enterprise-grade real-time untuk mendeteksi website yang terkena injeksi konten judi online (judol), dengan dashboard Cortex XDR-style, database persistence, dan REST API.

**Built with**: Python, FastAPI, Streamlit, PostgreSQL, SQLAlchemy, APScheduler, Docker

## 📋 Fitur

- ✅ **Real-Time Dashboard** - Monitoring 24/7 dengan Cortex XDR dark theme
- ✅ **Auto-Scan Scheduler** - Scanning otomatis setiap 10 menit
- ✅ **REST API** - FastAPI backend dengan Swagger UI documentation
- ✅ **Database Persistence** - PostgreSQL untuk historical data & analytics
- ✅ **Deteksi Advanced** - URL-level + content-level detection dengan 25+ keywords
- ✅ **SSL Handling** - Bypass invalid SSL certificates untuk scanning sites mencurigakan
- ✅ **Cache Management** - Multi-level caching untuk performance optimization
- ✅ **Metrics & Analytics** - 24-hour timeline, detection rate, hourly statistics
- ✅ **Docker Compose** - 3-service orchestration (PostgreSQL, API, Streamlit)
- ✅ **Background Tasks** - APScheduler untuk background scanning tanpa blocking UI

## � Dokumentasi & Panduan Penggunaan

**👉 Pilih dokumentasi sesuai kebutuhan:**

| Dokumen | Durasi | Untuk Siapa |
|---------|--------|------------|
| **[QUICK_START.md](QUICK_START.md)** | 5 menit | Pemula yang ingin langsung coba |
| **[USAGE_GUIDE.md](USAGE_GUIDE.md)** ⭐ | 20+ menit | Pengguna yang ingin detail lengkap |
| **[FAQ.md](FAQ.md)** | 5-10 menit | Ada pertanyaan spesifik? |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Technical | Developer & DevOps |

**USAGE_GUIDE.md mencakup:**
- 🎨 Dashboard Web Interface - Cara menggunakan setiap fitur
- 🔌 REST API Endpoints - Dokumentasi semua API endpoints  
- 📝 Mengelola URL Website - 3 metode menambah URLs
- 🔍 Interpretasi Hasil Scan - Memahami severity levels dan metrics
- ⚡ Advanced Features - Auto-scan, caching, SSL handling
- 🔧 Troubleshooting - Solusi untuk error umum

**Interactive Resources:**
- **API Docs (Swagger)**: http://localhost:8000/docs (saat system running)
- **Dashboard**: http://localhost:8501 (saat system running)

## �🚀 Quickstart

### Option 1: Docker Compose (Recommended) ⭐

```bash
# Navigate to project directory
cd "Deteksi Judol Real Time"

# Start all services (PostgreSQL, FastAPI, Streamlit)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Services akan berjalan di:**
- 🎨 Dashboard: http://localhost:8501
- 🔌 API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs
- 🗄️ Database: localhost:5432

### Option 2: Local Development

```bash
# Clone/Navigate to project
cd "Deteksi Judol Real Time"

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with local setup (requires PostgreSQL installed)
# Configure DATABASE_URL environment variable, then:
python api.py  # Terminal 1: Start API
streamlit run app.py  # Terminal 2: Start Dashboard
```

### Option 3: Scanner Standalone (Tanpa Database)

```bash
python deteksi_judol.py
```

## 📁 Struktur Project

```
Deteksi Judol Real Time/
├── deteksi_judol.py            # Core scanning engine (25+ keywords detection)
├── api.py                       # FastAPI backend with auto-scan scheduler
├── app.py                       # Streamlit web dashboard 
├── database.py                  # SQLAlchemy ORM models (7 tables)
├── schemas.py                   # Pydantic request/response schemas
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Streamlit container definition
├── Dockerfile.api               # FastAPI container definition
├── docker-compose.yml           # 3-service orchestration
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── .gitignore
└── .dockerignore
```

### Database Schema (7 Tables)

```
Website              # URLs being monitored
├── id
├── url (unique, indexed)
├── page_title
├── status (active/inactive/removed)
├── last_scan_time
└── created_at

Scan                 # Individual scan results
├── id
├── website_id (FK)
├── scan_time (indexed)
├── status_code
├── detected (indexed)
├── keywords_count
├── scan_duration
└── error

Detection            # Detected threats
├── id
├── scan_id (FK)
├── website_id (FK)
├── keywords_found (JSON)
├── suspect_urls (JSON)
├── page_title
├── severity (low/medium/high)
└── created_at (indexed)

HourlyStatistic      # Time-series analytics
├── id
├── hour (unique, indexed)
├── total_websites_scanned
├── total_detected
├── detection_rate
└── created_at

ScanSchedule         # Background job configuration
├── auto_scan_enabled (bool)
├── scan_interval_minutes
├── last_scan_time
├── next_scan_time
├── is_scanning
└── created_at

DashboardCache       # 5-minute cache layer
├── cache_key (unique, indexed)
├── cache_data (JSON)
└── expires_at

SystemConfig         # Reserved for future configuration
```

## 🔧 Konfigurasi

### Keywords Judol

Edit `JUDOL_KEYWORDS` dalam `deteksi_judol.py`:

```python
JUDOL_KEYWORDS = [
    'togel', 'slot', 'casino', 'betting', 'taruhan', 'judi', 'sportsbook',
    'poker', 'blackjack', 'roulette', 'toto', 'lotere', 'lotto',
    'perjudian', 'baccarat', 'bookie', 'gambling', 'wager', 'stakes',
    'qq', 'jackpot', 'gacor', 'jp', 'maxwin', 'rungkad'
]
```

### Menambah URLs untuk Scanning

**Metode 1: Via Dashboard (Recommended)**
1. Buka http://localhost:8501
2. Klik "🔄 Refresh & Clear Cache" di sidebar
3. Sistem akan auto-load dari `list_web.txt` ke database
4. URLs akan langsung di-scan

**Metode 2: Edit list_web.txt**
```
https://www.pertanian.go.id/
https://csirt.pertanian.go.id/
https://example.com/
```

Satu URL per baris. Sistem akan auto-load pada startup.

**Metode 3: Via REST API**
```bash
# Refresh & scan dari list_web.txt
curl -X POST http://localhost:8000/api/v1/websites/refresh

# Manual scan specific URLs
curl -X POST http://localhost:8000/api/v1/scan/manual \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com"], "priority": "urgent"}'
```

### Environment Variables

Edit di `docker-compose.yml`:

```yaml
environment:
  DATABASE_URL: postgresql://judol_user:judol_pass@postgres_db:5432/judol_db
  API_URL: http://judol_api:8000  # Internal service name
  LOG_LEVEL: INFO
```

### Scanner Settings

Dalam `deteksi_judol.py`:
- **Timeout**: 10 seconds (untuk HTTP request)
- **Delay**: 1 second (antar-scan delay untuk respect server)
- **SSL Verify**: False (untuk scan sites dengan invalid SSL certificates)

### Background Scan Schedule

Di `api.py`, auto-scan diatur ke **setiap 10 menit**:

```python
scheduler.add_job(
    auto_scan_task,
    "interval",
    minutes=10,  # Edit di sini untuk mengubah interval
    id="auto_scan",
    name="Auto Scan Task"
)
```

## 📊 Hasil Scan

### Output Format

```python
{
    'url': 'https://example.com',
    'status': 200,
    'timestamp': '2024-01-15 10:30:45',
    'detected': True,
    'keywords_found': ['togel', 'slot'],
    'keywords_count': 2,
    'suspect_urls': ['https://...'],
    'page_title': 'Header',
    'error': None
}
```

### Interpretasi Hasil

| Status | Arti |
|--------|------|
| ✓ Aman | Website normal, tidak ada injeksi judol |
| ⚠️ Terdeteksi | Ada keyword/URL judol ditemukan |
| ❌ Error | Gagal koneksi atau error lainnya |

## 🐳 Docker Commands

```bash
# Build image dengan tag
docker build -t judol-detector:1.0 .

# Run dengan environment variables
docker run -e STREAMLIT_SERVER_HEADLESS=true \
           -p 8501:8501 \
           judol-detector:1.0

# Run dengan volume mount
docker run -v ./list_web.txt:/app/list_web.txt \
           -v ./scan_results:/app/scan_results \
           -p 8501:8501 \
           judol-detector:1.0

# Docker Compose dengan custom file
docker-compose -f docker-compose.yml up -d

# Scale service (jika dengan multiple containers)
docker-compose up -d --scale judol_detector=3
```

## 📈 Performance

- Timeout per request: 10 detik
- Delay antar request: 1 detik
- Scanning 5 URL: ~15-20 detik
- Memory usage: ~200-300MB
- CPU usage: ~10-20%

## ⚠️ Catatan Penting

1. **User-Agent**: Script menggunakan Mozilla User-Agent untuk menghindari blocking
2. **Delay**: Jangan menghilangkan delay untuk menghindari IP ban
3. **Timeout**: Sesuaikan dengan kecepatan internet Anda
4. **Privacy**: Export data scan disimpan local saja
5. **Rate Limiting**: Beberapa server mungkin rate-limit requests

## 🔒 Security

- Input validation untuk URL
- HTML sanitization (hapus script/style)
- Error handling untuk exception
- No sensitive data stored
- Container runs as non-root (recommended)

## 📝 Logging

Logs bisa dilihat di:
- Streamlit: Output langsung di UI
- Docker: `docker-compose logs -f judol_detector`

## 🛠️ Troubleshooting

### Port 8501 sudah digunakan
```bash
docker run -p 8502:8501 judol-detector:1.0
# atau ubah di docker-compose.yml
```

### Koneksi timeout
- Tambah timeout: UI Streamlit → Timeout 15-20s
- Check internet connection
- Check firewall rules

### Memory limit
- Limit dalam docker-compose.yml:
```yaml
deploy:
  resources:
    limits:
      memory: 512M
```

### Build error
- Delete cache: `docker system prune -a`
- Rebuild: `docker-compose up --build`

## 📦 Dependencies

- **requests**: HTTP library
- **beautifulsoup4**: HTML parsing
- **streamlit**: Web framework
- **pandas**: Data processing
- **plotly**: Interactive charts
- **lxml**: XML/HTML processing

## 🚀 Deployment Options

### 1. Local Machine
```bash
streamlit run app.py
```

### 2. Docker Local
```bash
docker-compose up
```

### 3. Cloud (Render, Railway, Heroku)
Push repository dan configure untuk auto-deploy

### 4. Kubernetes
```yaml
# Buat deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: judol-detector
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: judol-detector
        image: judol-detector:1.0
        ports:
        - containerPort: 8501
```

## � Documentation & Resources

**Panduan Lengkap:**
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** ⭐ - Dokumentasi komprehensif cara menggunakan sistem
  - Dashboard Web Interface walkthrough
  - Semua REST API endpoints dengan contoh
  - Mengelola URLs (3 metode)
  - Interpretasi hasil scan
  - Advanced features
  - Troubleshooting & FAQ

**API Documentation (Interactive):**
- **Swagger UI**: http://localhost:8000/docs - Explore & test endpoints langsung

**Architecture Documentation:**
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & technical details

**Quick Links:**
- 🎨 **Dashboard**: http://localhost:8501 (saat system running)
- 🔌 **API**: http://localhost:8000 (saat system running)
- 📋 **API Docs**: http://localhost:8000/docs (saat system running)

## 📞 Support & Contribution

- Report bugs: Create issue
- Suggest features: Create discussion
- Contributing: Fork & submit PR

## 📄 License

MIT License - Feel free to use and modify

## 👥 Credits

Developed by PelancongAngkasa

---

**Last Updated**: May 4, 2026
**Version**: 2.0.0 Enterprise Edition
**System Status**: ✅ Production Ready
