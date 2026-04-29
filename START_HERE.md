# ✅ Setup Checklist & Getting Started

## 📋 Project Status

**Version**: 2.0
**Status**: ✅ Ready for Testing
**Files Created**: 19 files
**Total Size**: ~100KB

---

## 📁 Files Summary

### ✅ Core App (3 files)
- [x] `app.py` - Main Streamlit app with Auto Scan 10 min
- [x] `deteksi_judol.py` - Website scanner
- [x] `data_storage.py` - Historical data storage

### ✅ Analytics & Utilities (3 files)
- [x] `pages_analytics.py` - Analytics dashboard
- [x] `utils.py` - Logging & reporting
- [x] `test_detection.py` - Tests

### ✅ Configuration (5 files)
- [x] `requirements.txt` - Dependencies
- [x] `Dockerfile` - Container config
- [x] `docker-compose.yml` - Orchestration
- [x] `.streamlit/config.toml` - Streamlit theme
- [x] `.env.example` - Environment template

### ✅ Documentation (6 files)
- [x] `README.md` - Main documentation
- [x] `QUICK_START.md` - 5-minute setup
- [x] `AUTO_SCAN_GUIDE.md` - Auto scan guide
- [x] `CHANGELOG.md` - Version history
- [x] `v2.0_SUMMARY.md` - Feature summary
- [x] `FILE_REFERENCE.md` - File reference

### ✅ Setup Helpers (2 files)
- [x] `setup.bat` - Windows setup
- [x] `setup.sh` - Linux/Mac setup

### ✅ Data Files (1 file)
- [x] `list_web.txt` - Website list

---

## 🚀 Getting Started (Choose One)

### Option 1: Quick Start (Recommended)

```bash
# Windows
cd "c:\Users\Yusuf\Documents\Kerja\Kementan\Projek\Deteksi Judol Real Time"
setup.bat

# Then run app
streamlit run app.py
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Option 3: Docker (Production)

```bash
# Build & run
docker-compose up

# Access
http://localhost:8501
```

---

## 📝 First Time (Step by Step)

### Step 1: Run Setup ✨
```bash
cd "Deteksi Judol Real Time"
setup.bat         # Follow prompts
```

### Step 2: Start App
```bash
streamlit run app.py
```
Browser akan auto-open ke `http://localhost:8501`

### Step 3: Load URLs
- Sidebar → "Load dari file"
- Pilih `list_web.txt`
- Tunggu URL loaded

### Step 4: Run Auto Scan
```
Sidebar:
1. Mode: "Auto Scan (10 Menit)"
2. URLs: "Load dari file"
3. Click: "▶️ Mulai Auto Scan"
4. Monitor dashboard (10 min)
5. View results
```

### Step 5: Check Analytics (Optional)
```bash
streamlit run pages_analytics.py
```
View historical data & trends

---

## ⚙️ Configuration

### URL List
Edit `list_web.txt`:
```
https://website1.com
https://website2.com
https://website3.com
```

### Keywords
Edit `deteksi_judol.py`, find:
```python
JUDOL_KEYWORDS = [
    'togel', 'slot', 'casino', ...
]
```

### Timeout/Delay
In app → Sidebar Sliders:
- Timeout: 5-30 detik (default 10)
- Delay: 0-5 detik (default 1)

### Auto Scan Timing
Edit `app.py`, find:
```python
total_duration = 600    # 10 minutes
scan_interval = 120     # 2 minutes
max_scans = 6           # 6 scans total
```

---

## 🎯 Feature Highlights

### ✅ Auto Scan 10 Menit
- Otomatis 6 scan dalam 10 menit
- Real-time metrics & countdown
- Time series graph
- Hourly summary

### ✅ Real-time Dashboard
- Live metrics display
- Progress tracking
- Detection counter
- Visual graphs

### ✅ Historical Analytics
- 24-hour trends
- Per-hour breakdown
- Report generation
- CSV export

### ✅ Production Ready
- Docker containerization
- Health checks
- Error handling
- Logging system

---

## 📊 Workflow Examples

### Scenario A: Quick Check (5 min)
```
1. Open app
2. Load URLs
3. Manual Scan
4. View results (1-2 min)
```

### Scenario B: Monitoring (10+ min)
```
1. Select Auto Scan
2. Mulai Auto Scan
3. Monitor dashboard (10 min)
4. View analytics
5. Export report
```

### Scenario C: Production Monitoring
```
1. Deploy with Docker
2. Auto scan setiap jam
3. Data accumulates
4. View trends daily
5. Generate weekly report
```

---

## 🧪 Testing

### Run Tests
```bash
python test_detection.py
```

Checks:
- URL loading
- Dependencies installed
- File structure
- Basic scanning

### Manual Test
```bash
python deteksi_judol.py
```

Scans URLs dari `list_web.txt` satu kali

---

## 📁 Project Structure

```
Deteksi Judol Real Time/
├── 📱 App Core
│   ├── app.py ⭐
│   ├── deteksi_judol.py 🔍
│   ├── data_storage.py 💾
│   ├── pages_analytics.py 📊
│   └── utils.py 🛠️
├── ⚙️ Config
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .streamlit/
│   └── .env.example
├── 📚 Docs
│   ├── README.md
│   ├── AUTO_SCAN_GUIDE.md ⭐
│   ├── QUICK_START.md
│   └── CHANGELOG.md
├── 🧪 Testing
│   ├── test_detection.py
│   ├── setup.bat
│   └── setup.sh
├── 📊 Data
│   ├── list_web.txt
│   ├── scan_data/ (auto-created)
│   └── scan_results/ (auto-created)
└── ✓ Git
    ├── .gitignore
    └── .dockerignore
```

---

## 💡 Tips & Tricks

### Tip 1: Bookmark Analytics
```
http://localhost:8501/pages_analytics
```

### Tip 2: Quick Export
Click download button dari Detail tab

### Tip 3: Check Logs
```bash
cat scan_results/app.log
cat scan_data/scan_history.json
```

### Tip 4: Docker Clean
```bash
docker-compose down
docker system prune -a
```

### Tip 5: Multi-window Monitoring
- Window 1: `streamlit run app.py` (Scanning)
- Window 2: `streamlit run pages_analytics.py` (Analytics)

---

## 🔗 Quick Links

| Purpose | File/Command |
|---------|--------------|
| Main App | `streamlit run app.py` |
| Analytics | `streamlit run pages_analytics.py` |
| Quick Start | `QUICK_START.md` |
| Auto Scan Help | `AUTO_SCAN_GUIDE.md` |
| File Reference | `FILE_REFERENCE.md` |
| Version Info | `CHANGELOG.md` |
| Run Tests | `python test_detection.py` |
| Docker Deploy | `docker-compose up` |

---

## ✅ Pre-launch Checklist

### Before First Run
- [ ] Python 3.7+ installed
- [ ] Read QUICK_START.md
- [ ] Have list of URLs ready (list_web.txt)
- [ ] At least 200MB free disk
- [ ] Port 8501 available

### Before Production
- [ ] Tested all features
- [ ] Verified data storage
- [ ] Checked Docker setup
- [ ] Reviewed log files
- [ ] Configured keywords
- [ ] Set up alerts (optional)

### Before Deployment
- [ ] Docker image built
- [ ] Environment variables set (.env)
- [ ] Volume mounting verified
- [ ] Health checks tested
- [ ] Database persistence checked
- [ ] Team training completed

---

## 🆘 Troubleshooting

### Port 8501 Already in Use
```bash
# Find & kill process
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Dependencies Failed
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Docker Issues
```bash
docker-compose down
docker system prune -a
docker-compose build --no-cache
docker-compose up
```

### Permission Errors
```bash
# Windows: Run as Administrator
# Linux: sudo docker-compose up
chmod +x setup.sh
```

---

## 📞 Support Resources

1. **Quick Questions** → Check QUICK_START.md
2. **Auto Scan Issues** → Check AUTO_SCAN_GUIDE.md
3. **File Questions** → Check FILE_REFERENCE.md
4. **Version Info** → Check CHANGELOG.md
5. **Code Issues** → Check test_detection.py
6. **Docker Issues** → Check docker-compose.yml

---

## 🎉 You're All Set!

**What's Next?**

1. Run setup.bat / setup.sh
2. Start app: `streamlit run app.py`
3. Load URLs: list_web.txt
4. Try Auto Scan 10 menit
5. Check results
6. View analytics

**Ready? Let's go! 🚀**

```bash
cd "Deteksi Judol Real Time"
streamlit run app.py
```

---

**Version**: 2.0
**Release**: January 2024
**Status**: ✅ Production Ready

