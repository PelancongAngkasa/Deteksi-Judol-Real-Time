# 📱 Telegram Notifications Setup Guide

## Cara Setup Telegram Bot untuk Alerts

### 1. **Buat Telegram Bot (via BotFather)**

1. Buka Telegram dan search untuk [@BotFather](https://t.me/botfather)
2. Klik Start atau ketik `/start`
3. Ketik `/newbot`
4. Ikuti instruksi untuk membuat bot baru:
   - Enter bot name (misal: "Judol Detection Bot")
   - Enter bot username (misal: @judol_detection_bot)
5. **BotFather akan memberikan TOKEN** (simpan token ini!)
   
   Contoh token:
   ```
   123456789:ABCDefGHIjklmNOPqrsTUVwxyzABCDefGHIj
   ```

### 2. **Dapatkan Chat ID**

#### Opsi A: Create Private Group/Channel
1. Create Group atau Channel di Telegram
2. Add bot ke group/channel
3. Kirim message apapun ke group
4. Buka browser dan kunjungi:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   Ganti `<YOUR_BOT_TOKEN>` dengan token dari step 1
5. Cari `"chat":{"id":` di response
   - Contoh: `"chat":{"id":-1001234567890}`
   - Copy chat ID (termasuk tanda minus jika ada)

#### Opsi B: Direct Message (DM)
1. DM bot yang sudah dibuat
2. Kirim message apapun
3. Kunjungi URL sama seperti di atas
4. Cari `"from":{"id":` - ini adalah personal chat ID

### 3. **Setup Environment Variables**

Copy file `.env.example` ke `.env`:
```bash
cp .env.example .env
```

Edit `.env` dan tambahkan:
```bash
# Telegram Notifications
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIjklmNOPqrsTUVwxyzABCDefGHIj
TELEGRAM_CHAT_ID=-1001234567890
```

### 4. **Restart Docker**

```bash
docker-compose down
docker-compose up -d
```

### 5. **Test Telegram Connection**

Buka Python shell di container API:
```bash
docker-compose exec judol_api python
```

Jalankan:
```python
from notifications import TelegramNotifier

notifier = TelegramNotifier()

# Test 1: Simple message
notifier.send_message("🧪 Test message from Judol Detection System")

# Test 2: Threat detection
notifier.send_threat_detection(
    url="https://example.com",
    keywords=["togel", "slot"],
    severity="HIGH",
    suspect_urls=["http://malicious-site.com"]
)

# Test 3: Scan summary
notifier.send_scan_summary(total=10, detected=2, errors=0)

# Test 4: Check if configured
print(notifier.is_configured())
```

Jika berhasil, akan ada pesan di Telegram bot/group/channel.

---

## 🚀 Fitur Notifikasi

### 1. **Threat Detection**
Otomatis dikirim saat detektor menemukan keywords judol:
- URL yang terdeteksi
- Keywords yang ditemukan
- Severity level (CRITICAL, HIGH, MEDIUM, LOW)
- Suspect URLs di dalam content
- Timestamp

Contoh:
```
🔴 THREAT DETECTED

Website: https://example.com
Severity: HIGH
Keywords Found:
  • togel
  • slot
  • jackpot

Suspect URLs:
  🔗 http://malicious-site.com/togel

Time: 2026-06-18 15:30:45
```

### 2. **System Alerts**
Dikirim untuk kondisi sistem:
- ✅ Database connected/disconnected
- ✅ API up/down
- ✅ High detection rate (mass defacement)
- ✅ Auto-scan delayed
- ✅ Scan errors

### 3. **Daily Reports** (optional)
Dapat diatur untuk kirim daily summary:
- Total websites scanned
- Threats detected
- Detection rate
- Top keywords
- Most threatened sites

---

## 📝 Konfigurasi Berbeda per Environment

### Development (`.env.local`)
```bash
TELEGRAM_BOT_TOKEN=dev_token_here
TELEGRAM_CHAT_ID=your_personal_chat_id
```

### Production (`.env.prod`)
```bash
TELEGRAM_BOT_TOKEN=prod_token_here
TELEGRAM_CHAT_ID=-1001234567890  # Group/Channel ID
```

### Disable Notifications (untuk testing)
```bash
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

---

## 🔧 Troubleshooting

### Bot tidak mengirim message

1. **Check token & chat ID**
   ```python
   from notifications import TelegramNotifier
   n = TelegramNotifier()
   print(f"Bot token: {n.bot_token}")
   print(f"Chat ID: {n.chat_id}")
   print(f"Configured: {n.is_configured()}")
   ```

2. **Check network connectivity**
   ```bash
   docker-compose exec judol_api curl -I https://api.telegram.org
   ```

3. **Check logs**
   ```bash
   docker-compose logs judol_api | grep -i telegram
   ```

4. **Verify bot has access**
   - Bot harus added ke group/channel sebagai Admin (jika private)
   - Bot harus di-DM-kan minimal 1 pesan sebelumnya

### Bot di-block / Rate limited

- Telegram membatasi ~30 message/detik per bot
- Jika terlalu banyak alerts, groupkan atau delay notifications
- Cek [Telegram Bot API limits](https://core.telegram.org/bots/faq#how-can-i-make-sure-that-my-bot-doesn-t-get-rate-limited)

### Pesan garbled / encoding issues

- Notifier menggunakan HTML parsing dengan UTF-8
- Jika ada masalah, check encoding di `.env` file

---

## 📚 Referensi

- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [BotFather Guide](https://core.telegram.org/bots#botfather)
- [Telegram Bot Limits](https://core.telegram.org/bots/faq)
- [Python requests library](https://docs.python-requests.org/)

---

## ⚠️ Security Notes

- **Bot Token**: Keep secure, jangan commit ke repo
- **Chat ID**: Relatif aman untuk share (tidak bisa execute commands)
- Gunakan `.env` file yang di-gitignore
- Jangan hardcode credentials di code
- Rotate token jika ter-leak

---

## 🎯 Advanced: Custom Notifications

Buat custom alert message:

```python
from notifications import notification_manager

# Custom message
notification_manager.send_alert(
    level="CRITICAL",
    title="Custom Alert Title",
    details={
        "issue": "Something went wrong",
        "affected_sites": ["site1.com", "site2.com"],
        "action_taken": "Auto-mitigation started"
    }
)

# Custom threat detection
notification_manager.send_threat_detection(
    url="https://custom-url.com",
    keywords=["custom", "keywords"],
    severity="CRITICAL",
    suspect_urls=["http://sus1.com", "http://sus2.com"]
)
```

---

## ✅ Checklist

- [ ] Create bot via @BotFather
- [ ] Get bot token
- [ ] Get chat ID (DM atau Group/Channel)
- [ ] Update `.env` dengan credentials
- [ ] Restart Docker containers
- [ ] Test notifications
- [ ] Verify messages di Telegram
- [ ] Monitor logs untuk errors
