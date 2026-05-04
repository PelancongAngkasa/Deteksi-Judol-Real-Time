# 📚 Documentation Index

Central hub untuk semua dokumentasi Deteksi Judol Real-Time.

---

## 📖 Main Documentation

### 1. **[README.md](README.md)** 
**Durasi**: 5-10 menit | **Tipe**: Overview

Dokumentasi utama project yang mencakup:
- Fitur-fitur sistem
- Quickstart options (Docker, Local, Standalone)
- Struktur project & database schema
- Konfigurasi environment
- Deployment options
- License & credits

**Mulai dari sini untuk overview umum!**

---

### 2. **[QUICK_START.md](QUICK_START.md)** ⚡
**Durasi**: 5 menit | **Tipe**: Getting Started

Setup dan jalankan sistem dalam 5 menit!

**Cocok untuk:**
- First-time users yang ingin langsung coba
- Demo/POC
- Testing setup

**Isi:**
- Step-by-step 5 menit setup
- Add URLs quickly
- View basic results
- Common tasks
- Troubleshooting cepat

**👉 START HERE jika new to system!**

---

### 3. **[USAGE_GUIDE.md](USAGE_GUIDE.md)** 📖
**Durasi**: 20+ menit | **Tipe**: Comprehensive

Panduan lengkap dan detail untuk menggunakan semua fitur sistem.

**Cocok untuk:**
- Pengguna yang ingin explore semua fitur
- Integrator yang ingin gunakan API
- Administrator sistem

**Isi (9 sections):**

| Section | Content |
|---------|---------|
| 🎨 Dashboard | Cara menggunakan UI, tab-tab, metrics |
| 🔌 API | Semua 9 endpoints dengan examples |
| 📝 Manage URLs | 3 metode add/manage URLs |
| 🔍 Results | Severity levels, metrics explanation |
| ⚡ Advanced | Auto-scan, caching, SSL handling |
| 🔧 Troubleshooting | 7 common problems & solutions |
| 📞 Support | Logging, debug, resources |

**Referensi ini saat ada pertanyaan spesifik!**

---

### 4. **[FAQ.md](FAQ.md)** ❓
**Durasi**: 5-10 menit | **Tipe**: Q&A

Kumpulan pertanyaan dan jawaban yang sering diajukan.

**Cocok untuk:**
- Pengguna dengan pertanyaan spesifik
- Troubleshooting masalah tertentu
- Understanding system behavior

**Isi (7 categories):**
- 🎨 Dashboard - 6 questions
- 🔍 Scanning & Detection - 7 questions
- 🗄️ Database - 4 questions
- 🔌 API - 3 questions
- 🐳 Docker - 4 questions
- ⚡ Performance - 3 questions
- 🚀 Deployment & Production - 2 questions
- 📚 Documentation - 1 question

**Cari jawaban di sini untuk common issues!**

---

### 5. **[ARCHITECTURE.md](ARCHITECTURE.md)** 🏗️
**Durasi**: 15+ menit | **Tipe**: Technical

Detailed system architecture dan design documentation.

**Cocok untuk:**
- Developers yang ingin understand codebase
- DevOps engineers
- Contributors & maintainers

**Isi (expected):**
- System architecture diagram
- Component relationships
- Data flow
- Database schema details
- API design
- Deployment architecture
- Performance considerations
- Security considerations

---

## 🎯 Quick Navigation by Use Case

### 👤 "I'm new, where do I start?"
1. Start → **[QUICK_START.md](QUICK_START.md)** (5 min)
2. Then → **[USAGE_GUIDE.md](USAGE_GUIDE.md)** (20 min) for deeper dive
3. Reference → **[FAQ.md](FAQ.md)** for Q&A

---

### 🎨 "Cara menggunakan Dashboard?"
- **[USAGE_GUIDE.md - Dashboard Section](USAGE_GUIDE.md#-dashboard-web-interface)**
- **[FAQ.md - Dashboard Category](FAQ.md#-dashboard)**

---

### 🔌 "Bagaimana gunakan REST API?"
- **[USAGE_GUIDE.md - API Section](USAGE_GUIDE.md#-rest-api-documentation)** (recommended)
- **Interactive API Docs**: http://localhost:8000/docs (saat system running)
- **[FAQ.md - API Category](FAQ.md#-api)**

---

### 📝 "Cara add/manage URLs?"
- **[USAGE_GUIDE.md - Manage URLs](USAGE_GUIDE.md#-mengelola-url-website)**
- **[QUICK_START.md - Step 3](QUICK_START.md#-step-3-add-urls-1-menit)**

---

### 🔍 "Bagaimana interpret scan results?"
- **[USAGE_GUIDE.md - Interpretasi Hasil](USAGE_GUIDE.md#-interpretasi-hasil-scan)**
- **[FAQ.md - Detection Q&A](FAQ.md#-scanning--detection)**

---

### 🐳 "Docker-related questions?"
- **[FAQ.md - Docker Category](FAQ.md#-docker)**
- **[QUICK_START.md - Troubleshooting](QUICK_START.md#-troubleshooting)**

---

### 🚀 "Production deployment?"
- **[README.md - Deployment Options](README.md#-deployment-options)**
- **[FAQ.md - Deployment](FAQ.md#-deployment)**
- **[ARCHITECTURE.md](ARCHITECTURE.md)** for technical details

---

### 🔧 "Ada error/issue?"
1. Check → **[QUICK_START.md - Troubleshooting](QUICK_START.md#-troubleshooting)**
2. Then → **[USAGE_GUIDE.md - Troubleshooting](USAGE_GUIDE.md#-troubleshooting)**
3. Search → **[FAQ.md](FAQ.md)** for your specific issue

---

### 💻 "Developer/Contributor?"
- **[README.md - Structure](README.md#-struktur-project)**
- **[ARCHITECTURE.md](ARCHITECTURE.md)** for design
- **[FAQ.md - Database](FAQ.md#-database)** for DB access

---

## 📊 Documentation Statistics

| Document | Size | Sections | Estimated Read Time |
|----------|------|----------|---------------------|
| README.md | 12KB | 10 | 5-10 min |
| USAGE_GUIDE.md | 16KB | 9 | 20+ min |
| QUICK_START.md | 3KB | 4 | 5 min |
| FAQ.md | 9KB | 8 | 10-15 min |
| **TOTAL** | **40KB** | **31** | **50+ min** |

---

## 🔗 External Resources

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/docs
- Available when system is running
- Test endpoints directly

### Dashboard
- **URL**: http://localhost:8501
- Available when system is running
- Real-time monitoring

---

## 📞 Support & Help

### Self-Help Resources
1. **[QUICK_START.md](QUICK_START.md)** - 5-minute setup
2. **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed guide
3. **[FAQ.md](FAQ.md)** - Common questions

### Get Help
- Search in **[FAQ.md](FAQ.md)** for your question
- Check **[USAGE_GUIDE.md - Troubleshooting](USAGE_GUIDE.md#-troubleshooting)** section
- Review system logs: `docker-compose logs -f`

---

## 🎓 Learning Path

### Beginner Path (30 minutes total)
```
1. README.md (5 min) → Understand what system does
   ↓
2. QUICK_START.md (5 min) → Setup & run system
   ↓
3. USAGE_GUIDE.md Dashboard (10 min) → Learn UI
   ↓
4. Try manually (10 min) → Hands-on exploration
```

### Intermediate Path (60 minutes total)
```
Beginner Path (30 min)
   ↓
5. USAGE_GUIDE.md API (15 min) → Learn API
   ↓
6. FAQ.md (10 min) → Answer specific questions
   ↓
7. Integrate API (5 min) → Test endpoints
```

### Advanced Path (90+ minutes total)
```
Intermediate Path (60 min)
   ↓
8. ARCHITECTURE.md (15 min) → Understand design
   ↓
9. Code review (15+ min) → Explore codebase
   ↓
10. Deployment (15+ min) → Setup production
```

---

## 📝 Version History

| Version | Date | Docs Status |
|---------|------|-------------|
| 2.0.0 | May 2026 | ✅ Complete |
| 1.0.0 | Earlier | Archived |

---

## ✅ Documentation Checklist

- ✅ README.md - Project overview
- ✅ QUICK_START.md - 5-minute setup
- ✅ USAGE_GUIDE.md - Comprehensive guide
- ✅ FAQ.md - Common Q&A
- ✅ ARCHITECTURE.md - Technical design
- ✅ This file - Documentation index

---

**Last Updated**: May 4, 2026  
**Maintained by**: PelancongAngkasa  
**Status**: ✅ Up-to-date

---

**Happy Learning! 📚**

For questions or suggestions about documentation, please create an issue!
