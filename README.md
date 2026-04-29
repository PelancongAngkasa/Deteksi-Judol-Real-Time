# 🛡️ Deteksi Defacement Judol Online

Sistem monitoring real-time untuk mendeteksi website yang terkena injeksi konten judi online (judol), dibangun dengan Python, Streamlit, dan Docker.

## 📋 Fitur

- ✅ **Web Scraping Real-time** - Scan multiple website sekaligus
- ✅ **Deteksi Keyword** - Identifikasi kata kunci judi online
- ✅ **URL Mencurigakan** - Deteksi link injeksi judol
- ✅ **Interface Streamlit** - Dashboard interaktif dan user-friendly
- ✅ **Export Data** - Save hasil scan ke CSV
- ✅ **Docker Ready** - Deploy dengan mudah menggunakan Docker
- ✅ **Error Handling** - Logging dan error tracking
- ✅ **Metrics & Charts** - Visualisasi hasil scan dengan Plotly

## 🚀 Quickstart

### 1. Setup Local

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

# Run Streamlit app
streamlit run app.py
```

Akses aplikasi di: `http://localhost:8501`

### 2. Run Scanner Standalone

```bash
python deteksi_judol.py
```

### 3. Deploy dengan Docker

#### Option A: Docker CLI
```bash
# Build image
docker build -t judol-detector .

# Run container
docker run -p 8501:8501 -v $(pwd)/list_web.txt:/app/list_web.txt judol-detector
```

#### Option B: Docker Compose (Recommended)
```bash
# Build dan run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Akses aplikasi di: `http://localhost:8501`

## 📁 Struktur Project

```
Deteksi Judol Real Time/
├── deteksi_judol.py           # Core scanner module
├── app.py                       # Streamlit web interface
├── list_web.txt                # List of URLs to scan
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Orchestration
├── .streamlit/
│   └── config.toml            # Streamlit config
├── .gitignore                  # Git ignore rules
└── .dockerignore              # Docker ignore rules
```

## 🔧 Konfigurasi

### Keywords Judol

Edit JUDOL_KEYWORDS dalam `deteksi_judol.py`:

```python
JUDOL_KEYWORDS = [
    'togel', 'slot', 'casino', 'betting', 'taruhan', 'judi', ...
]
```

### List Website

Edit `list_web.txt` (satu URL per baris):

```
https://www.pertanian.go.id/
https://csirt.pertanian.go.id/
https://ditjenpkh.pertanian.go.id/
```

### Scanner Settings (dalam app Streamlit)

- **Timeout**: Batas waktu koneksi (default 10s)
- **Delay**: Jeda antar request (default 1s)

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

## 📞 Support & Contribution

- Report bugs: Create issue
- Suggest features: Create discussion
- Contributing: Fork & submit PR

## 📄 License

MIT License - Feel free to use and modify

## 👥 Credits

Developed untuk Kementerian Pertanian - Direktorat Keamanan Siber

---

**Last Updated**: January 2024
**Version**: 1.0.0
