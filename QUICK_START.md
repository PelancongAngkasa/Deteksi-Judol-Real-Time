# ⚡ Quick Start Guide - 5 Menit Setup

Panduan cepat untuk mulai menggunakan Deteksi Judol dalam 5 menit!

---

## 🚀 Step 1: Start System (2 menit)

```bash
cd "Deteksi Judol Real Time"
docker-compose up -d
```

✅ System ready! Tunggu 30 detik untuk semua services stabilisasi.

---

## 🎨 Step 2: Buka Dashboard (30 detik)

**Browser**: http://localhost:8501

Akan melihat:
- Dashboard kosong (belum ada URLs)
- Sidebar dengan kontrol

---

## 📝 Step 3: Add URLs (1 menit)

### Cara Tercepat:

1. **Edit file**: `list_web.txt`
   ```
   https://www.pertanian.go.id/
   https://csirt.pertanian.go.id/
   https://example.com/
   ```

2. **Di Dashboard Sidebar**: Klik **"🔄 Refresh & Clear Cache"**

3. **Tunggu**: Sistem akan scan semua URLs (~10-30 detik)

---

## ✅ Step 4: View Results (1 menit 30 detik)

### Dashboard Tab:
- 📊 **Dashboard** - Lihat metrics & charts
- 🚨 **Recent Threats** - Lihat detections terbaru
- 📈 **Analytics** - Trend 24 jam

### Metrics:
- **🌐 Websites** - Total URLs di-monitor
- **⚠️ Threats** - Total detections hari ini
- **📊 Detection Rate** - Persentase threats

---

## 🎯 Common Tasks

### ➕ Add More URLs

**Di Dashboard → Sidebar → "📤 Load dari list_web.txt"**
- Edit list_web.txt
- Klik button
- Scan otomatis dimulai

### 🔍 Manual Scan URL Tertentu

**Di Dashboard → "⚙️ Settings" Tab**
- Paste URL
- Klik "📁 Manual Scan"
- Lihat results di "Recent Threats"

### 🔄 Toggle Auto-Scan

**Di Dashboard → Sidebar**
- Click "🟢 Auto ON" untuk enable
- Click "🔴 Auto OFF" untuk disable
- Scan otomatis setiap 10 menit

### 🗑️ Stop System

```bash
docker-compose down
```

---

## 📊 Interpretasi Results

| Status | Arti |
|--------|------|
| 🟢 ✅ Safe | Tidak ada keywords judol |
| 🟠 ⚠️ MEDIUM | Ada 3-5 keywords |
| 🔴 🚨 HIGH | Ada 6+ keywords = confirmed judol |

---

## 🔌 API Testing (Bonus)

```bash
# Get dashboard data
curl http://localhost:8000/api/v1/dashboard

# Get websites list
curl http://localhost:8000/api/v1/websites

# Manual scan via API
curl -X POST http://localhost:8000/api/v1/scan/manual \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com"]}'

# API Interactive Docs
# Browser: http://localhost:8000/docs
```

---

## ⚠️ Troubleshooting

**"Connection refused to API"**
```bash
docker ps  # Check if containers running
docker-compose restart judol_api
```

**"URLs tidak muncul"**
```bash
# Edit list_web.txt (satu URL per baris)
# Klik "🔄 Refresh & Clear Cache" di sidebar
# Tunggu 30 detik
```

**"Container exit/crash"**
```bash
docker-compose logs judol_api --tail 50  # Check errors
docker-compose down
docker-compose up --build  # Rebuild
```

---

## 📖 Next Steps

Untuk panduan lebih detail:
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Dokumentasi lengkap
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design details
- **API Docs**: http://localhost:8000/docs

---

**Happy Scanning! 🛡️**
