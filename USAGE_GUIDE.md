# 📖 Panduan Penggunaan - Deteksi Defacement Judol Online

Dokumentasi lengkap untuk menggunakan dashboard, API, dan fitur-fitur sistem deteksi judol.

---

## 📑 Daftar Isi

1. [Dashboard Web Interface](#dashboard-web-interface)
2. [REST API Documentation](#rest-api-documentation)
3. [Mengelola URL Website](#mengelola-url-website)
4. [Interpretasi Hasil Scan](#interpretasi-hasil-scan)
5. [Advanced Features](#advanced-features)
6. [Troubleshooting](#troubleshooting)

---

## 🎨 Dashboard Web Interface

### Akses Dashboard

Buka browser dan navigasi ke: **http://localhost:8501**

### Layout Dashboard

Dashboard terbagi menjadi 3 bagian utama:

#### 🔘 **Sidebar (Kiri)**

**Kontrol & Konfigurasi**
- **🟢 Auto ON / 🔴 Auto OFF** - Toggle automatic scanning (setiap 10 menit)
- **📁 Manual Scan** - Trigger scan manual untuk URL tertentu

**Upload Website URLs**
- **📤 Load dari list_web.txt** - Load URLs dari file ke database
- **🔄 Refresh & Clear Cache** - Refresh URLs dan clear semua cache

**Status Sistem**
- **Websites** - Total website yang di-monitor
- **Threats** - Total threats terdeteksi
- **⏱️ Last** - Waktu scan terakhir

---

#### 📊 **Main Dashboard (Tengah)**

**Header & Status**
- 🛡️ Title: "Deteksi Defacement Judol Online"
- Status: "🟢 ONLINE" (menunjukkan API connected)
- 🔄 Refresh button - Manual refresh data

**Quick Metrics** (4 cards)

| Card | Deskripsi |
|------|-----------|
| 🌐 Websites | Total website yang sedang di-monitor |
| ⚠️ Threats | Total detections hari ini (deduplicated per website) |
| 🔴 This Hour | Total threats detected dalam 1 jam terakhir |
| 🔄 Auto-Scan | Status auto-scan (ON/OFF) dan interval |

**Tab Navigation**

1. **📊 Dashboard** (Active by default)
   - Line chart: Detection rate (%) over 24 hours
   - Gauge chart: Current detection rate
   - Statistics: Safe websites vs Threats count
   - Threat Level indicator

2. **🚨 Recent Threats**
   - List of recent detections dengan details:
     - 🌐 **URL** - Clickable link ke website
     - 🕐 **Time** - Timestamp detection
     - 🔍 **Keywords** - Keywords yang ditemukan
     - 🟠 **Severity** - Level bahaya (MEDIUM/HIGH)
     - 🔍 **Details** - Button untuk expand details

3. **📈 Analytics**
   - Defacement count chart (24-hour)
   - Total detected (24H)
   - Peak hour detection
   - Average detections per hour

4. **⚙️ Settings**
   - Auto-scan toggle
   - Manual scan form
   - Paste URLs untuk scan manual

---

### How to Use Dashboard

#### **1. Monitor Real-Time**

1. Buka dashboard http://localhost:8501
2. Lihat "🌐 Websites" count - total URL yang di-monitor
3. Lihat "⚠️ Threats" count - update setiap scan
4. Lihat timeline chart untuk trend detection

#### **2. Menambah URL untuk Monitoring**

**Metode A: Via list_web.txt + Refresh Button**
```
1. Edit list_web.txt di root project (satu URL per baris)
2. Di sidebar, klik "🔄 Refresh & Clear Cache"
3. Sistem akan:
   - Load URLs dari file
   - Add ke database
   - Scan semua URLs
   - Update dashboard
```

**Metode B: Manual Scan**
```
1. Klik "⚙️ Settings" tab
2. Paste URL(s) di textarea
3. Klik "📁 Manual Scan"
4. Tunggu hasil scan muncul
5. Lihat results di "🚨 Recent Threats"
```

#### **3. Trigger Auto-Scan**

```
1. Sidebar → "🟢 Auto ON" button
   - Menjadi "🔴 Auto OFF" saat di-click
   - Sistem akan auto-scan setiap 10 menit
2. Toggle kembali untuk disable auto-scan
```

#### **4. View Threat Details**

```
1. Tab "🚨 Recent Threats"
2. Lihat list detections terbaru
3. Click "🔍 Details" button untuk expand
4. Lihat:
   - Keywords found
   - Suspect URLs (if any)
   - Page title
   - Full timestamp
```

#### **5. Interpret Analytics**

```
Tab "📈 Analytics" menampilkan:
- Defacement count over 24 hours
- Peak hour (jam dengan threats terbanyak)
- Average threats per hour
```

---

## 🔌 REST API Documentation

API documentation interaktif tersedia di: **http://localhost:8000/docs** (Swagger UI)

### Authentication
**Status**: Tidak ada authentication (localhost development)

### Base URL
```
http://localhost:8000/api/v1
```

---

### Endpoints

#### **1. GET /health**
Check API health status

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-04T08:30:00.000Z",
  "service": "Deteksi Judol API"
}
```

---

#### **2. GET /api/v1/dashboard**
Get dashboard data (cached 5 minutes)

```bash
curl http://localhost:8000/api/v1/dashboard
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_websites": 15,
    "total_detected_today": 3,
    "total_detected_this_hour": 1,
    "detection_rate": 20.0,
    "auto_scan_enabled": true,
    "last_scan_time": "2026-05-04T08:25:00.000Z",
    "hourly_data": [...],
    "recent_detections": [...]
  }
}
```

---

#### **3. GET /api/v1/scan-status**
Get current scan status & statistics

```bash
curl http://localhost:8000/api/v1/scan-status
```

**Response:**
```json
{
  "is_scanning": false,
  "auto_scan_enabled": true,
  "scan_interval_minutes": 10,
  "last_scan_time": "2026-05-04T08:25:00.000Z",
  "next_scan_time": "2026-05-04T08:35:00.000Z",
  "total_websites": 15,
  "total_detected_today": 3
}
```

---

#### **4. GET /api/v1/websites**
List semua websites yang sedang di-monitor

```bash
curl http://localhost:8000/api/v1/websites
```

**Response:**
```json
[
  {
    "id": 1,
    "url": "https://example.com",
    "page_title": "Homepage",
    "status": "active",
    "last_scan_time": "2026-05-04T08:25:00.000Z",
    "created_at": "2026-05-04T00:00:00.000Z"
  },
  ...
]
```

---

#### **5. POST /api/v1/scan/manual**
Trigger manual scan untuk specific URLs

```bash
curl -X POST http://localhost:8000/api/v1/scan/manual \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com", "https://example2.com"],
    "priority": "urgent"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Manual scan completed: 1 threats detected",
  "results_count": 2
}
```

---

#### **6. POST /api/v1/scan/toggle-auto**
Enable/disable automatic scanning

```bash
# Enable auto-scan
curl -X POST "http://localhost:8000/api/v1/scan/toggle-auto?enabled=true"

# Disable auto-scan
curl -X POST "http://localhost:8000/api/v1/scan/toggle-auto?enabled=false"
```

**Response:**
```json
{
  "status": "success",
  "auto_scan_enabled": true,
  "message": "Auto-scan enabled"
}
```

---

#### **7. POST /api/v1/websites/refresh**
Reload URLs dari list_web.txt dan trigger immediate scan

```bash
curl -X POST http://localhost:8000/api/v1/websites/refresh
```

**Response:**
```json
{
  "status": "success",
  "total_urls": 15,
  "added": 0,
  "current_total": 15,
  "scanned": 15,
  "detected": 3,
  "message": "Refreshed from list_web.txt: added 0 new websites, scanned 15, detected 3 threats"
}
```

---

#### **8. DELETE /api/v1/websites/{website_id}**
Permanently delete website dan semua related data

```bash
curl -X DELETE http://localhost:8000/api/v1/websites/1
```

**Response:**
```json
{
  "status": "success",
  "message": "Website 1 permanently deleted"
}
```

---

#### **9. POST /api/v1/cache/clear**
Clear all dashboard cache

```bash
curl -X POST http://localhost:8000/api/v1/cache/clear
```

**Response:**
```json
{
  "status": "success",
  "message": "Cache cleared"
}
```

---

## 📝 Mengelola URL Website

### Metode 1: Via list_web.txt (Recommended)

**File Format:**
```
https://www.pertanian.go.id/
https://csirt.pertanian.go.id/
https://example.com/
https://another-site.org/
```

**Cara Menggunakan:**
1. Edit `list_web.txt` di root project
2. Satu URL per baris
3. Save file
4. Di dashboard, klik "🔄 Refresh & Clear Cache"
5. Sistem akan auto-load ke database dan scan semua URLs

---

### Metode 2: Via Dashboard Manual Scan

**Langkah-Langkah:**
1. Tab "⚙️ Settings"
2. Copy-paste URL(s) di textarea:
   ```
   https://example1.com
   https://example2.com
   ```
3. Klik "📁 Manual Scan"
4. Tunggu hasil scan
5. Lihat results di tab "🚨 Recent Threats"

---

### Metode 3: Via REST API

**Add & Scan URLs:**
```bash
curl -X POST http://localhost:8000/api/v1/scan/manual \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example1.com", "https://example2.com"],
    "priority": "urgent"
  }'
```

**Delete URL:**
```bash
# Get website ID first
curl http://localhost:8000/api/v1/websites | grep -i example

# Delete by ID
curl -X DELETE http://localhost:8000/api/v1/websites/5
```

---

## 🔍 Interpretasi Hasil Scan

### Hasil Detection

#### **Detected (Positif/Threat)**
```
🔴 Status: ⚠️ TERDETEKSI

Indikator:
- Keywords judol ditemukan dalam URL atau content
- Severity: MEDIUM atau HIGH
- Appears di "Recent Threats" list
```

**Contoh:**
```
URL: https://example.com
Keywords Found: ['togel', 'slot']
Severity: 🟠 MEDIUM
Page Title: Homepage | Judol Togel
```

---

#### **Safe (Negatif)**
```
🟢 Status: ✅ AMAN

Indikator:
- Tidak ada keywords judol ditemukan
- Diperhitungkan di "Statistics" → "✅ Safe" count
```

---

#### **Error**
```
❌ Status: ERROR

Causes:
- Invalid URL
- Website unreachable (timeout)
- SSL certificate error (biasanya handled, retry)
- Network error

Check logs: docker-compose logs judol_api
```

---

### Severity Levels

| Level | Threshold | Arti |
|-------|-----------|------|
| 🟢 LOW | 1-2 keywords | Minor detection |
| 🟠 MEDIUM | 3-5 keywords | Suspicious activity |
| 🔴 HIGH | 6+ keywords | Strong indication of judol injection |

---

### Metrics Explanation

**Detection Rate (%)**
```
= (Total Detected Websites / Total Scanned Websites) × 100

Contoh:
- 15 websites scanned
- 3 detected
- Detection Rate = (3/15) × 100 = 20%
```

**Hourly Statistics**
- Shows detections per hour over 24-hour period
- Used for timeline visualization
- Peak hour identification

---

## ⚡ Advanced Features

### 1. Auto-Scan Scheduler

**How It Works:**
- Runs every 10 minutes (configurable)
- Scans all "active" websites in database
- Updates HourlyStatistic for trend analysis
- Non-blocking (background task)

**Control:**
```bash
# Via Dashboard: Toggle "🟢 Auto ON" button

# Via API:
curl -X POST "http://localhost:8000/api/v1/scan/toggle-auto?enabled=true"
```

**Logs:**
```bash
docker-compose logs judol_api | grep auto_scan_task
```

---

### 2. Multi-Level Caching

**Cache Layers:**
1. **Streamlit Cache** (5 seconds)
   - Dashboard API calls cached
   - Auto-refresh every 5s

2. **API Cache** (5 minutes)
   - Dashboard data cached in DashboardCache table
   - Manual cache clear available

3. **Database Cache**
   - expires_at field untuk TTL management

**Clear Cache:**
```bash
# Via Dashboard: "🔄 Refresh & Clear Cache"

# Via API:
curl -X POST http://localhost:8000/api/v1/cache/clear
```

---

### 3. SSL Certificate Handling

**Issue:** Websites dengan invalid SSL certificates

**Solution:**
- Scanner bypasses SSL verification (verify=False)
- Allows scanning suspicious sites
- urllib3 warnings suppressed

**Behavior:**
```python
# Still performs URL-level detection
# Even if SSL error occurs, keywords in URL will be found
result = scan_website("https://suspicious-site.com")
# Returns detected=True if keywords in URL
```

---

### 4. Keyword Detection Levels

**Level 1: URL Detection (Fast)**
```
Check if any keyword exists in URL string
Example: "https://example.com/togel" → detected ✅
```

**Level 2: Content Detection (Deep)**
```
Check if keywords exist in page content using regex with word boundaries
Example: Page contains "join our togel community" → detected ✅
```

**Combined Result:**
- Detected if EITHER level matches
- More thorough detection
- Catches injected content in forms/scripts

---

## 🔧 Troubleshooting

### Problem 1: Dashboard tidak tersambung ke API

**Symptoms:**
- "Error connecting to API"
- Dashboard menunjukkan 0 websites

**Solutions:**
```bash
# Check if API container running
docker ps | grep judol_api

# Check API logs
docker-compose logs judol_api --tail 50

# Verify API health
curl http://localhost:8000/health

# Restart API
docker-compose restart judol_api
```

---

### Problem 2: Scan tidak berjalan

**Symptoms:**
- Auto-scan disabled but no manual scan option
- Last scan time tidak update

**Solutions:**
```bash
# Check auto-scan status
curl http://localhost:8000/api/v1/scan-status

# Enable auto-scan
curl -X POST "http://localhost:8000/api/v1/scan/toggle-auto?enabled=true"

# Manual trigger
curl -X POST http://localhost:8000/api/v1/websites/refresh

# Check logs
docker-compose logs judol_api | grep "auto_scan_task"
```

---

### Problem 3: URLs tidak terload dari file

**Symptoms:**
- Click "📤 Load dari list_web.txt" tapi tidak ada perubahan
- Websites count tetap 0

**Solutions:**
```bash
# Verify file exists
ls -la list_web.txt

# Check file not empty
wc -l list_web.txt  # Should show > 0

# Check file permissions
chmod 644 list_web.txt

# Manual refresh via API
curl -X POST http://localhost:8000/api/v1/websites/refresh

# Check API logs for file read errors
docker-compose logs judol_api | grep "load_urls"
```

---

### Problem 4: High memory/CPU usage

**Symptoms:**
- System slow during scan
- Docker container using lots of resources

**Solutions:**
```bash
# Increase scan interval (default 10 minutes)
# Edit api.py:
scheduler.add_job(
    auto_scan_task,
    "interval",
    minutes=30,  # Change from 10 to 30
    ...
)

# Monitor resource usage
docker stats judol_api

# Set resource limits in docker-compose.yml:
api_server:
  deploy:
    resources:
      limits:
        memory: 512M
        cpus: "1.0"
```

---

### Problem 5: SSL certificate errors during scan

**Symptoms:**
- Some websites show SSL errors
- Cannot scan certain URLs

**Status:**
✅ This is expected and handled!

**How It Works:**
- SSL verification disabled by default
- URL-level detection still works
- Content detection attempted if SSL bypass successful

**Verify:**
```bash
# Check scan result
curl http://localhost:8000/api/v1/websites

# Should show status_code and detected fields
# Even if SSL error occurred
```

---

### Problem 6: Dashboard page stuck/loading

**Symptoms:**
- Streamlit app frozen
- "Running..." indicator spinning forever

**Solutions:**
```bash
# Clear Streamlit cache
docker-compose exec judol_streamlit rm -rf /root/.streamlit/cache

# Restart Streamlit container
docker-compose restart judol_streamlit

# Full restart
docker-compose down
docker-compose up -d
```

---

### Problem 7: Database connection error

**Symptoms:**
- "Connection refused" error
- "FATAL: remaining connection slots reserved"

**Solutions:**
```bash
# Check PostgreSQL container
docker ps | grep postgres

# Check database logs
docker-compose logs judol_postgres --tail 50

# Restart database
docker-compose restart judol_postgres

# Wait for healthy
docker-compose logs judol_postgres | grep "ready"
```

---

## 📞 Support & Logging

### View Logs

**API Logs:**
```bash
docker-compose logs judol_api -f
```

**Dashboard Logs:**
```bash
docker-compose logs judol_streamlit -f
```

**Database Logs:**
```bash
docker-compose logs judol_postgres -f
```

**All Services:**
```bash
docker-compose logs -f
```

---

### Debug Mode

**Enable verbose logging in api.py:**
```python
logging.basicConfig(level=logging.DEBUG)  # Change from INFO
```

Then rebuild and restart:
```bash
docker-compose up --build
```

---

## 📚 Additional Resources

- **API Docs (Interactive)**: http://localhost:8000/docs
- **System Architecture**: See ARCHITECTURE.md
- **Configuration**: See docker-compose.yml
- **Database Schema**: See database.py

---

**Last Updated**: May 4, 2026
**System Version**: 2.0.0 Enterprise Edition
