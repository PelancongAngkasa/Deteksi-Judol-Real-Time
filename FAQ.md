# ❓ FAQ - Frequently Asked Questions

Jawaban untuk pertanyaan yang sering diajukan tentang Deteksi Judol.

---

## 🎨 Dashboard

### Q: Dashboard tidak menampilkan data?

**A:** Kemungkinan penyebab:

1. **Belum ada URLs yang di-scan**
   - Dashboard → Sidebar → "📁 Manual Scan"
   - Paste URL(s) dan klik "Scan"
   - Atau: Settings tab → Add Website
   - Tunggu 30 detik

2. **API tidak terkoneksi**
   - Check: http://localhost:8000/health
   - Restart: `docker-compose restart judol_api`

3. **Streamlit cache error**
   - Clear cache di sidebar
   - Refresh page (F5)

---

### Q: Berapa lama scan setiap website?

**A:** Tergantung:
- **Per-URL**: 5-15 detik (timeout 10s)
- **5 URLs**: ~30-60 detik
- **15 URLs**: ~2-3 menit
- Auto-scan: Setiap 10 menit (background task)

---

### Q: Apakah auto-scan mengganggu dashboard?

**A:** **Tidak!** 
- Auto-scan berjalan di background (APScheduler)
- Dashboard tetap responsive
- Scanning tidak memblokir UI
- Data di-cache untuk performance

---

### Q: Bagaimana cara export data?

**A:** Data tersimpan di database PostgreSQL.

**Opsi export:**

1. **CSV via SQL**
   ```bash
   docker-compose exec judol_postgres psql -U judol_user -d judol_db \
     -c "\COPY (SELECT * FROM detection) TO '/tmp/detections.csv' CSV HEADER"
   ```

2. **JSON via API**
   ```bash
   curl http://localhost:8000/api/v1/dashboard > dashboard_data.json
   ```

3. **PostgreSQL Tools**
   - pgAdmin
   - DBeaver
   - Custom scripts

---

## 🔍 Scanning & Detection

### Q: Apa saja keywords yang di-deteksi?

**A:** 25+ keywords judol termasuk:

| Kategori | Keywords |
|----------|----------|
| Togel | togel, toto, lotto, lottery |
| Slot | slot, machine, gacor, maxwin |
| Casino | casino, baccarat, roulette, blackjack |
| Betting | betting, taruhan, sportsbook, bookie |
| General | judi, gambling, wager, stakes |
| Regional | qq, jp, rungkad |

Edit lengkap di `deteksi_judol.py` line 19.

---

### Q: Bagaimana sistem mendeteksi judol?

**A:** 2-level detection:

1. **URL-Level (Fast)**
   ```
   "https://example.com/togel" → detected ✅
   ```

2. **Content-Level (Deep)**
   ```
   Check keywords dalam page content dengan regex
   "Join our togel community" → detected ✅
   ```

**Result**: Detected jika ANY level match

---

### Q: Kenapa website dengan SSL error tetap ter-scan?

**A:** 
- SSL verification di-bypass dengan `verify=False`
- Allows scanning suspicious sites
- URL-level detection tetap bekerja
- Content detection jika bypass berhasil

**Ini fitur, bukan bug!** Memungkinkan scan sites mencurigakan dengan SSL invalid.

---

### Q: Bagaimana handling false positives?

**A:** 
- Deteksi berbasis keywords → minimal false positives
- Word boundaries regex mengurangi matching palsu
- Manual review di dashboard

**Jika ada false positive:**
- Add whitelist keywords di `deteksi_judol.py`
- Or delete website: API DELETE endpoint

---

### Q: Bisa scan HTTPS?

**A:** **Yes!** 
- Supports both HTTP & HTTPS
- SSL verification disabled by default
- Safe untuk scan sites dengan invalid certs

---

## 🗄️ Database

### Q: Berapa lama data tersimpan?

**A:** **Unlimited** (sampai manual delete)

Data yang tersimpan:
- Website URLs & metadata
- Scan history (semua scan results)
- Detections (all threats found)
- Hourly statistics (24-month default)

**Untuk reduce disk:**
- Archive old scans
- Delete websites: `DELETE FROM website WHERE id = X`

---

### Q: Bagaimana backup database?

**A:** PostgreSQL dalam Docker

```bash
# Backup
docker-compose exec judol_postgres pg_dump -U judol_user judol_db > backup.sql

# Restore
docker-compose exec judol_postgres psql -U judol_user judol_db < backup.sql

# Atau gunakan volume
# Docker automatically persists: postgres_data:/var/lib/postgresql/data
```

---

### Q: Bisa akses database langsung?

**A:** **Yes!**

```bash
# Connect ke PostgreSQL
docker-compose exec judol_postgres psql -U judol_user -d judol_db

# Common queries:
SELECT COUNT(*) FROM website;              # Total URLs
SELECT COUNT(*) FROM detection;            # Total threats
SELECT * FROM detection LIMIT 10;          # Recent threats
SELECT * FROM hourly_statistic ORDER BY hour DESC;  # Analytics
```

---

## 🔌 API

### Q: Dimana API documentation?

**A:** Swagger UI Interactive di: **http://localhost:8000/docs**

Atau read: **[USAGE_GUIDE.md - REST API Section](USAGE_GUIDE.md#-rest-api-documentation)**

---

### Q: Bagaimana authenticate API requests?

**A:** **No authentication needed** (localhost development)

Untuk production, add:
- API key authentication
- JWT tokens
- OAuth2

---

### Q: Bisa scale ke multiple API servers?

**A:** 

**Current**: Single instance

**Untuk scale:**

1. **Load balancer** (nginx/HAProxy)
2. **Multiple API containers**
3. **Shared PostgreSQL database**
4. **Redis untuk distributed caching**

Example docker-compose:
```yaml
services:
  api_1:
    # ... api config
  api_2:
    # ... api config
  loadbalancer:
    image: nginx:latest
    ports:
      - "8000:8000"
    # ... nginx config untuk balance
```

---

## 🐳 Docker

### Q: Container crash setelah start?

**A:** Check logs:

```bash
docker-compose logs judol_api --tail 50
docker-compose logs judol_postgres --tail 50
docker-compose logs judol_streamlit --tail 50
```

**Common issues:**

1. **Port already in use**
   ```bash
   # Edit docker-compose.yml ports
   ports:
     - "8502:8501"  # Change 8501 to 8502
   ```

2. **Not enough resources**
   ```bash
   # Restart with more resources
   docker-compose down
   docker-compose up --build
   ```

3. **Database not ready**
   ```bash
   # Wait for postgres healthcheck
   docker-compose logs judol_postgres | grep "ready"
   ```

---

### Q: Bagaimana update kode tanpa rebuild?

**A:** Untuk local development:

```bash
# Edit file (contoh: deteksi_judol.py)

# Restart container (auto-reload)
docker-compose restart judol_api

# Or full rebuild
docker-compose up --build -d
```

---

### Q: Berapa disk space yang dibutuhkan?

**A:** 
- **Images**: ~2GB (Python, PostgreSQL base)
- **Data per 10K scans**: ~100-500MB (depends on content)
- **Typical setup**: 5-10GB recommended

---

## ⚡ Performance

### Q: Dashboard lambat saat banyak data?

**A:** Multi-level optimization:

1. **Streamlit cache** (5 seconds)
2. **API cache** (5 minutes)
3. **Database indexes** (scan_time, detected, website_id)

**Untuk optimize:**

```python
# Increase cache TTL
@st.cache_data(ttl=300)  # 5 minutes default

# Or archive old data
DELETE FROM scan WHERE scan_time < NOW() - INTERVAL '30 days'
```

---

### Q: Auto-scan menggunakan banyak CPU?

**A:** Normal behavior

**Untuk reduce:**

1. **Increase scan interval** (default 10 min)
   ```python
   # Edit api.py line 62
   minutes=30  # Change from 10
   ```

2. **Reduce website count**

3. **Limit concurrent scans**

---

### Q: Memory usage naik terus?

**A:** Possible memory leak

**Debug:**
```bash
docker stats judol_api

# Restart container
docker-compose restart judol_api

# Check logs for error messages
docker-compose logs judol_api
```

---

## 🚀 Deployment

### Q: Bisa deploy ke cloud?

**A:** **Yes!**

**Options:**

1. **Heroku**
   - Add Procfile
   - Add buildpacks

2. **Railway**
   - Connect GitHub
   - Auto-deploy

3. **Docker Hub / GitHub Container Registry**
   - Push images
   - Deploy anywhere

4. **Kubernetes**
   - Create manifests
   - Use Helm charts

---

### Q: Bagaimana setup untuk production?

**A:** Checklist:

- [ ] Change default PostgreSQL password
- [ ] Add API authentication (JWT/OAuth)
- [ ] Enable HTTPS/TLS
- [ ] Setup logging aggregation
- [ ] Configure auto-backups
- [ ] Setup monitoring/alerts
- [ ] Rate limiting for API
- [ ] WAF/DDoS protection
- [ ] Regular security audits

---

## 📚 Documentation

### Q: Dimana dokumentasi lengkap?

**A:** 
1. **[QUICK_START.md](QUICK_START.md)** - Setup 5 menit
2. **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Panduan lengkap (⭐ recommended)
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
4. **[README.md](README.md)** - Overview & references

---

### Q: Bagaimana contribute?

**A:** 
1. Fork repository
2. Create feature branch
3. Submit PR
4. Documentation updates welcome!

---

## 🆘 Support

### Q: Masih ada yang tidak clear?

**A:** 
- Read: [USAGE_GUIDE.md](USAGE_GUIDE.md) (recommended first resource)
- Check: API docs http://localhost:8000/docs
- Review: ARCHITECTURE.md for technical details
- Create: GitHub issue

---

**Last Updated**: May 4, 2026

**Have more questions? [Create an issue!](https://github.com/PelancongAngkasa/Deteksi-Judol-Real-Time/issues)**
