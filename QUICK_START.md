# 🚀 Quick Start Guide

## 📦 Instalasi & Menjalankan

### Windows
```bash
# 1. Jalankan setup script
setup.bat

# 2. Jalankan scanner
python deteksi_judol.py

# 3. Buka Streamlit app
streamlit run app.py
```

### Linux/macOS
```bash
# 1. Jalankan setup script
bash setup.sh

# 2. Jalankan scanner
python3 deteksi_judol.py

# 3. Buka Streamlit app
streamlit run app.py
```

## 🐳 Docker Setup

### Option 1: Docker CLI
```bash
# Build image
docker build -t judol-detector .

# Run container
docker run -p 8501:8501 -v ./list_web.txt:/app/list_web.txt judol-detector
```

### Option 2: Docker Compose (Recommended)
```bash
# Start all services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

**Akses aplikasi di:** http://localhost:8501

## 📝 Edit Web List

Ubah `list_web.txt` untuk menambah/mengurangi website:

```
https://website1.com
https://website2.com
https://website3.com
```

## ⚙️ Konfigurasi Streamlit

Edit `.streamlit/config.toml` untuk customize:
- Theme colors
- Font
- Server settings

## 📊 Hasil Scan

Hasil tersimpan di folder `scan_results/`:
- JSON format (results)
- CSV format (data)
- Summary file
- Log files

## 🔍 Keywords Judol

Default keywords dalam `deteksi_judol.py`:
```python
JUDOL_KEYWORDS = [
    'togel', 'slot', 'casino', 'betting', 'taruhan', 'judi', ...
]
```

Edit list ini sesuai kebutuhan.

## ⚠️ Troubleshooting

### Port 8501 sudah digunakan
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9

# Atau gunakan port berbeda
docker run -p 8502:8501 judol-detector
```

### Memory issue
Kurangi jumlah URL atau tambah timeout:
- Edit `list_web.txt`
- Naikkan slider timeout di Streamlit UI

### Connection timeout
- Check internet connection
- Naikkan timeout di sidebar (15-20 detik)

## 📚 Dokumentasi Lengkap

Lihat `README.md` untuk dokumentasi lengkap.

## 🆘 Help

```bash
# Test dependencies
python test_detection.py

# Scan single URL
python deteksi_judol.py

# Run with debug
streamlit run app.py --logger.level=debug
```

---

**Happy Scanning! 🛡️**
