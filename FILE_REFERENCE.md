# 📁 Project File Reference

## 🎯 Core Application Files

### `app.py` ⭐ MAIN APP
**Purpose**: Streamlit main application dengan UI dashboard
**Size**: ~700 lines
**Features**:
- Auto Scan 10 Menit mode
- Manual Scan mode
- Real-time metrics display
- Time series graph
- Results tabs & export
- Session state management

**When to use**: Main interface untuk end-users

---

### `deteksi_judol.py` 🔍 SCANNER
**Purpose**: Core website scanning & detection logic
**Size**: ~150 lines
**Class**: `DeteksiJudol`
**Methods**:
- `__init__()` - Initialize dengan timeout
- `scan_website(url)` - Scan satu website
- `scan_multiple(urls)` - Scan multiple websites
- `load_urls_from_file()` - Load URL list
- `_extract_suspicious_urls()` - Extract judol URLs
- `_error_result()` - Create error result

**When to use**: Standalone scanning, batch processing

---

### `data_storage.py` 💾 DATA PERSISTENCE
**Purpose**: Historical data storage & analytics
**Size**: ~250 lines
**Classes**:
- `ScanDataStorage` - Persistent data management
  - `save_scan_session()` - Save session to JSON
  - `save_hourly_summary()` - Save hourly aggregation
  - `get_hourly_data()` - Retrieve hourly stats
  - `get_statistics()` - Calculate statistics
  - `generate_trend_report()` - Create text report
  
- `RealTimeMonitor` - Session monitoring
  - `start_session()` - Begin monitoring
  - `add_scan()` - Add scan result
  - `get_session_summary()` - Get session data
  - `is_active()` - Check if active
  - `get_remaining_time()` - Get time remaining

**When to use**: Data persistence, reporting, analytics

---

### `pages_analytics.py` 📊 ANALYTICS DASHBOARD
**Purpose**: Historical data visualization & reporting
**Size**: ~300 lines
**Tabs**:
- **Trend** - 24-hour trend line chart
- **Detail** - Per-hour breakdown table
- **Report** - Trend analysis report
- **Raw Data** - Full scan history explorer

**When to use**: View historical trends, generate reports

---

### `utils.py` 🛠️ UTILITIES
**Purpose**: Logging & report generation
**Size**: ~150 lines
**Classes**:
- `ScanLogger` - Logging & file saving
  - `save_scan_results()` - Save results
  - `save_summary()` - Save summary
  - `get_report()` - Generate text report
  - `log_info/warning/error()` - Logging
  
- `ReportGenerator` - Report generation
  - `generate_html_report()` - Create HTML report

**When to use**: Logging, report generation, debugging

---

## 📋 Configuration Files

### `requirements.txt` 📦 DEPENDENCIES
**Purpose**: Python package dependencies
**Content**:
- requests==2.31.0
- beautifulsoup4==4.12.2
- streamlit==1.28.1
- pandas==2.1.1
- plotly==5.17.0
- lxml==4.9.3
- python-dateutil==2.8.2

**When to use**: Install: `pip install -r requirements.txt`

---

### `Dockerfile` 🐳 CONTAINER
**Purpose**: Docker image definition
**Base**: python:3.11-slim
**Includes**:
- System dependencies (gcc)
- Python packages from requirements.txt
- App files copy
- Port 8501 expose
- Health check
- Streamlit run command

**When to use**: Docker build: `docker build -t judol-detector .`

---

### `docker-compose.yml` 🎼 ORCHESTRATION
**Purpose**: Multi-container orchestration
**Services**: judol_detector
**Includes**:
- Port mapping: 8501:8501
- Volume mounting
- Environment variables
- Restart policy
- Network configuration
- Health check

**When to use**: `docker-compose up` untuk full stack

---

### `.streamlit/config.toml` 🎨 STREAMLIT CONFIG
**Purpose**: Streamlit theme & server settings
**Settings**:
- primaryColor: #d32f2f (red)
- Font & background colors
- XSRF protection
- Max message size

**When to use**: Customize UI theme

---

### `.env.example` 📋 ENVIRONMENT TEMPLATE
**Purpose**: Example environment variables
**Variables**:
- STREAMLIT_SERVER_* settings
- SCANNER_* settings
- LOG_LEVEL
- ENABLE_XSRF_PROTECTION

**When to use**: Copy to `.env` untuk production

---

### `.gitignore` 🚫 GIT IGNORE
**Purpose**: Exclude files from git
**Ignores**: `__pycache__`, `*.pyc`, `.venv`, `scan_data/`, `.streamlit`

---

### `.dockerignore` 🚫 DOCKER IGNORE
**Purpose**: Exclude files from Docker build
**Ignores**: `.git`, `.gitignore`, `.env`

---

## 📚 Documentation Files

### `README.md` 📖 MAIN DOCS
**Purpose**: Comprehensive project documentation
**Sections**:
- Features overview
- Setup instructions (local & Docker)
- Project structure
- Configuration guide
- Deployment options
- Troubleshooting
- Dependencies
- License

**When to use**: Reference guide

---

### `QUICK_START.md` ⚡ QUICK START
**Purpose**: 5-minute setup guide
**Sections**:
- Installation & running
- Docker quick setup
- Web list editing
- Basic configuration
- Quick troubleshooting

**When to use**: First-time setup

---

### `AUTO_SCAN_GUIDE.md` 🎯 AUTO SCAN DOCS
**Purpose**: Detailed auto-scan feature documentation
**Sections**:
- Feature explanation
- Usage instructions
- Auto scan timeline
- Dashboard metrics
- Historical data explanation
- Export & reporting
- Troubleshooting auto scan
- Advanced usage

**When to use**: Auto scan feature reference

---

### `CHANGELOG.md` 📝 VERSION HISTORY
**Purpose**: Version changes & improvements
**Content**:
- v2.0 features
- Modified files
- Technical details
- Usage examples
- Data model
- Future enhancements

**When to use**: Track version changes

---

### `v2.0_SUMMARY.md` 🎉 FEATURE SUMMARY
**Purpose**: v2.0 feature overview
**Content**:
- Feature explanation
- Usage examples
- Workflows
- Comparison table
- Documentation files reference

**When to use**: Overview of v2.0 features

---

## 🧪 Testing & Setup Files

### `test_detection.py` ✅ TESTS
**Purpose**: Unit & integration tests
**Classes**:
- `TestDeteksiJudol` - Scanner tests
- `TestScanLogger` - Logger tests
- `TestReportGenerator` - Report tests
- `run_basic_tests()` - Integration tests

**When to use**: `python test_detection.py`

---

### `setup.bat` 🪟 WINDOWS SETUP
**Purpose**: Automated Windows setup
**Does**:
- Check Python & Docker
- Create virtual environment
- Install dependencies
- Create folders
- Run tests
- Optional Docker setup

**When to use**: Windows: `setup.bat`

---

### `setup.sh` 🐧 LINUX/MAC SETUP
**Purpose**: Automated Linux/Mac setup
**Does**: Same as setup.bat for Unix systems

**When to use**: Linux/Mac: `bash setup.sh`

---

## 📊 Data Files

### `list_web.txt` 📝 URL LIST
**Purpose**: List of websites to scan
**Format**: One URL per line
**Example**:
```
https://www.pertanian.go.id/
https://csirt.pertanian.go.id/
https://ditjenpkh.pertanian.go.id/
```

**When to use**: Edit to change scan targets

---

## 📁 Auto-Created Directories

### `scan_data/` (Auto-created)
**Purpose**: Historical scan data storage
**Files**:
- `scan_history.json` - All scan sessions
- `hourly_summary.csv` - Hourly aggregation

**Location**: Auto-created saat pertama kali scan

---

### `scan_results/` (Auto-created)
**Purpose**: Manual scan reports storage
**Files**:
- `scan_*.json` - Session results
- `summary_*.json` - Session summary
- `app.log` - Application log

**Location**: Created by setup script

---

### `.streamlit/` (Auto-created)
**Purpose**: Streamlit secrets & cache
**Files**:
- `config.toml` - Configuration (we provide)
- Secrets cache (auto-managed)

---

## 🔗 File Relationships

```
UI Layer:
  app.py ←→ pages_analytics.py
    ↓
  Scanning Layer:
  deteksi_judol.py
    ↓
  Storage Layer:
  data_storage.py → scan_data/ (JSON/CSV)
    ↓
  Utilities:
  utils.py (logging, reporting)
```

---

## 💾 File Size Reference

| File | Size | Importance |
|------|------|-----------|
| app.py | ~7KB | 🔴 Critical |
| deteksi_judol.py | ~4KB | 🔴 Critical |
| data_storage.py | ~6KB | 🟠 Important |
| pages_analytics.py | ~8KB | 🟠 Important |
| utils.py | ~4KB | 🟡 Optional |
| requirements.txt | <1KB | 🔴 Critical |
| Dockerfile | <1KB | 🟠 Important |
| docker-compose.yml | <2KB | 🟠 Important |
| Documentation | ~50KB | 🟡 Reference |

---

## 🚀 Typical Usage Files

### Untuk Development
- app.py (edit UI)
- deteksi_judol.py (edit scanner logic)
- test_detection.py (run tests)

### Untuk Deployment
- requirements.txt
- Dockerfile
- docker-compose.yml
- list_web.txt

### Untuk Documentation
- README.md
- AUTO_SCAN_GUIDE.md
- CHANGELOG.md

### Untuk Data
- scan_data/ (automatically managed)
- scan_results/ (check reports)

---

## 📖 Which File to Edit?

| Need | Edit File |
|------|-----------|
| Add keywords | deteksi_judol.py (JUDOL_KEYWORDS) |
| Change UI | app.py |
| Add logging | utils.py |
| Change theme | .streamlit/config.toml |
| Add URLs | list_web.txt |
| Docker setup | docker-compose.yml |
| Auto scan interval | app.py (timing constants) |
| Report format | utils.py (ReportGenerator) |

---

## ✅ Checklist for Production

- [ ] Review list_web.txt (correct URLs?)
- [ ] Test with setup.bat/setup.sh
- [ ] Run test_detection.py
- [ ] Change .env.example → .env
- [ ] Configure .streamlit/config.toml
- [ ] Test Auto Scan 10 minutes
- [ ] Check scan_data/ storage
- [ ] Test Analytics dashboard
- [ ] Docker build & test
- [ ] Deploy docker-compose

---

**Last Updated**: January 2024
**Version**: 2.0
**Total Files**: 20+

