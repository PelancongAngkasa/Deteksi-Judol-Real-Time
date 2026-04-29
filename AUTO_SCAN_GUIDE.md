# 📊 Auto-Scan & Analytics Guide

## Fitur Baru

### 1. **Auto Scan 10 Menit** ⏱️

Sistem akan otomatis melakukan 6 kali scanning dalam 10 menit (setiap 2 menit).

#### Cara Menggunakan:

1. **Buka Sidebar** → Pilih **"Auto Scan (10 Menit)"**
2. **Load URL** dari file atau upload
3. **Klik "▶️ Mulai Auto Scan"**
4. Monitor progress dengan:
   - Countdown timer (sisa waktu)
   - Progress bar (% selesai)
   - Real-time metrics (jumlah terdeteksi)

#### Auto Scan Timeline:
```
Menit 0-2  → Scan #1
Menit 2-4  → Scan #2
Menit 4-6  → Scan #3
Menit 6-8  → Scan #4
Menit 8-10 → Scan #5
                ↓
         Selesai ✓
```

#### Output Auto Scan:
- **Real-time Counter** - Deteksi per scan
- **Time-series Graph** - Grafik deteksi vs waktu
- **Hourly Summary** - Ringkasan per jam
- **Session Statistics** - Total scan, detected, aman

---

### 2. **Dashboard Real-time** 📊

#### Metrics yang Ditampilkan:

| Metric | Deskripsi |
|--------|-----------|
| ⏱️ Sisa Waktu | Countdown 10 menit |
| Scan Ke | Urutan scan (1/6, 2/6, dst) |
| Progress | Persentase progress |
| ✅ Scan Selesai | Jumlah scan completed |
| ⚠️ Terdeteksi | Website dengan judol |
| ✓ Aman | Website tanpa judol |
| Detection Rate | % website terdeteksi |

#### Grafik Real-time:

**1. Time Series Graph**
```
Y-axis: Jumlah Website Terdeteksi (0-5, 0-10, dst)
X-axis: Waktu Scan (HH:MM:SS)
       ↑
       │     ●
     5 │    ╱ ╲
       │   ╱   ●
     3 │  ●     ╲
       │       ● ●
     1 │      ╱ ╲
       └────────────→ WAKTU
```

**2. Hourly Summary Chart**
```
Bar chart menampilkan total deteksi per jam
- Red bars = Terdeteksi
- Green portion = Aman
- Stacked view
```

---

### 3. **Historical Data & Analytics** 📈

#### File Storage:
```
scan_data/
├── scan_history.json       # Riwayat semua scan
└── hourly_summary.csv      # Ringkasan per jam
```

#### Data yang Disimpan:

**scan_history.json:**
```json
{
  "timestamp": "2024-01-15T10:30:45",
  "total_sites": 5,
  "detected_count": 2,
  "safe_count": 3,
  "error_count": 0,
  "duration_seconds": 120
}
```

**hourly_summary.csv:**
```
jam,detected_count,total_count,detection_rate,timestamp
00:00,5,20,25%,2024-01-15 00:30:00
01:00,3,20,15%,2024-01-15 01:30:00
02:00,7,20,35%,2024-01-15 02:30:00
```

#### Analytics Dashboard (`pages_analytics.py`):

Fitur:
- 📊 **Trend Tab** - Grafik trend 24 jam
- 📋 **Detail Tab** - Tabel detail per jam
- 📄 **Report Tab** - Laporan analisis
- 🗂️ **Raw Data Tab** - Scan history

**Filter Options:**
- Lihat data 1 jam terakhir
- Lihat data 3 jam terakhir
- Lihat data 6 jam terakhir (default)
- Lihat data 24 jam terakhir
- Lihat data 48 jam terakhir
- Lihat data 72 jam terakhir

---

## 🚀 Workflow Penggunaan

### Scenario 1: Monitoring Kontinyu

```bash
1. Buka app.py
2. Pilih Mode: "Auto Scan (10 Menit)"
3. Load URL dari list_web.txt
4. Klik "▶️ Mulai Auto Scan"
5. Monitor dashboard
6. Tunggu 10 menit - selesai otomatis
7. Data tersimpan otomatis
```

### Scenario 2: Manual Scan + Analytics

```bash
1. Pilih Mode: "Manual Scan"
2. Klik "🔍 Mulai Scan"
3. Tunggu selesai
4. Lihat hasil detail
5. Buka Analytics untuk riwayat
```

### Scenario 3: Continuous Monitoring (Production)

```bash
# Terminal 1: Run Streamlit
docker-compose up

# Dashboard akan:
# - Jalankan auto scan setiap jam
# - Simpan hasil ke database
# - Update grafik analytics
# - Generate hourly reports
```

---

## 📊 Interpretasi Grafik

### Time Series Graph

**Puncak tinggi = Deteksi banyak** 
```
8│     ●
6│    ╱╲
4│   ╱  ●
2│  ●    ╲
0└────────●──→
```
⚠️ Alert: Website banyak yang terdeteksi pada jam tersebut!

### Hourly Summary

**Red bars = Website terdeteksi**
```
08:00 ■■■■■■■■ (9 website)
09:00 ■■■ (3 website)
10:00 ■■■■■ (5 website)
```

**Detection Rate (%):**
```
08:00 = 45% (9 dari 20)
09:00 = 15% (3 dari 20)
10:00 = 25% (5 dari 20)
```

---

## ⚙️ Konfigurasi Auto Scan

### Mengubah Interval

Edit di `app.py`:
```python
total_duration = 600   # 10 menit (detik)
scan_interval = 120    # Scan setiap 2 menit
max_scans = 6          # Total 6 scan (10÷2)
```

Contoh: Untuk 15 menit, 3 scan:
```python
total_duration = 900   # 15 menit
scan_interval = 300    # Scan setiap 5 menit
max_scans = 3          # Total 3 scan
```

### Data Persistence

Untuk menyimpan ke database (opsional):

```python
from data_storage import ScanDataStorage

storage = ScanDataStorage()

# Setelah scan selesai
storage.save_scan_session({
    'timestamp': datetime.now(),
    'total_sites': len(results),
    'detected_count': detected,
    'safe_count': safe,
    'error_count': errors,
    'duration_seconds': elapsed_time,
    'results': results
})

# Update hourly summary
storage.save_hourly_summary(current_hour, detected, len(results))
```

---

## 💾 Export & Reporting

### Export Opsi:

1. **CSV Export** (dari tab Detail)
   - Langsung download dari UI
   - Format: `judol_scan_YYYYMMDD_HHMMSS.csv`

2. **JSON Export** (dari scan_data/)
   - Automation data
   - For integration dengan sistem lain

3. **HTML Report** (dari utils.py)
   ```python
   from utils import ReportGenerator
   ReportGenerator.generate_html_report(results, 'report.html')
   ```

---

## 🔔 Alerts & Notifications

### Alert Conditions:

⚠️ **Red Alert**: Detection rate > 30%
```
Jika > 30% dari website terdeteksi judol
→ Trigger alert notification
```

🟡 **Yellow Alert**: Detection rate 10-30%
```
Jika 10-30% website terdeteksi
→ Monitor closely
```

✅ **Green Alert**: Detection rate < 10%
```
Jika < 10% website terdeteksi
→ Status OK
```

---

## 🐳 Docker Auto-Scan

### Docker Compose + Scheduled Scan:

Edit `docker-compose.yml`:
```yaml
services:
  judol_detector:
    ...
    environment:
      - AUTO_SCAN_ENABLED=true
      - AUTO_SCAN_INTERVAL=3600  # Every hour
      - AUTO_SCAN_DURATION=600   # 10 minutes
```

---

## 📈 Advanced Analytics

### Weekly Report

```python
# Get 7-day statistics
stats_7d = storage.get_statistics(hours_lookback=168)

# Generate trend
trend_report = storage.generate_trend_report()
```

### ML Integration (Future)

```python
# Anomaly detection
import pandas as pd
from sklearn.ensemble import IsolationForest

data = storage.get_hourly_data(168)
X = data[['detected_count']].values
model = IsolationForest()
anomalies = model.fit_predict(X)
```

---

## 🆘 Troubleshooting

### Auto Scan Tidak Berjalan

```bash
# Check session state
st.write(st.session_state)

# Verify URLs loaded
if not urls:
    st.error("URLs not loaded")
```

### Grafik Tidak Muncul

- Pastikan data ada: `scan_data/hourly_summary.csv`
- Check file permissions
- Refresh Streamlit: `Ctrl+R`

### Memory Issues Saat 10 Menit Scan

- Kurangi jumlah URL
- Naikkan interval (3 menit instead of 2)
- Gunakan streaming output

---

## 📚 API Usage

### Dalam Python Script:

```python
from app import DeteksiJudol
from data_storage import ScanDataStorage

# Initialize
detector = DeteksiJudol()
storage = ScanDataStorage()

# Load URLs
urls = detector.load_urls_from_file('list_web.txt')

# Scan
results = detector.scan_multiple(urls, delay=1)

# Store
storage.save_scan_session({
    'timestamp': datetime.now(),
    'total_sites': len(urls),
    'detected_count': sum(1 for r in results if r['detected']),
    'safe_count': sum(1 for r in results if not r['detected']),
    'error_count': sum(1 for r in results if r['error']),
    'results': results
})

# Analyze
stats = storage.get_statistics(24)
print(f"Total Detected (24h): {stats['total_detected']}")
```

---

**Version**: 2.0 (with Auto-Scan & Analytics)
**Last Updated**: January 2024
