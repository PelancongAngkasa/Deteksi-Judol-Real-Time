"""
Module untuk mengirim notifikasi (Telegram)
"""
import os
import requests
import logging
from datetime import datetime
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Mengirim notifikasi via Telegram Bot API"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram credentials not configured. Telegram notifications disabled.")
    
    def is_configured(self) -> bool:
        """Check if Telegram is properly configured"""
        return bool(self.bot_token and self.chat_id)
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Kirim message ke Telegram chat
        
        Args:
            message: Pesan dengan format HTML atau Markdown
            parse_mode: "HTML" atau "Markdown"
        
        Returns:
            True jika berhasil, False jika gagal
        """
        if not self.is_configured():
            logger.error("Telegram not configured. Cannot send message.")
            return False
        
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            
            response = requests.post(self.api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Telegram message sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def send_alert_critical(self, title: str, details: Dict) -> bool:
        """Kirim CRITICAL alert"""
        message = f"""
🚨 <b>CRITICAL ALERT</b>

<b>{title}</b>

<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{self._format_details(details)}

⚠️ Immediate action required!
"""
        return self.send_message(message)
    
    def send_alert_warning(self, title: str, details: Dict) -> bool:
        """Kirim WARNING alert"""
        message = f"""
⚠️ <b>WARNING</b>

<b>{title}</b>

<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{self._format_details(details)}
"""
        return self.send_message(message)
    
    def send_alert_info(self, title: str, details: Dict) -> bool:
        """Kirim INFO notification"""
        message = f"""
ℹ️ <b>Information</b>

<b>{title}</b>

<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{self._format_details(details)}
"""
        return self.send_message(message)
    
    def send_threat_detection(self, url: str, keywords: List[str], severity: str, suspect_urls: Optional[List[str]] = None) -> bool:
        """Kirim notifikasi deteksi threat"""
        severity_emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }
        
        emoji = severity_emoji.get(severity, "⚠️")
        
        message = f"""
{emoji} <b>THREAT DETECTED</b>

<b>Website:</b> <code>{url}</code>

<b>Severity:</b> <b>{severity}</b>

<b>Keywords Found:</b>
"""
        # Add keywords as bullet list
        for keyword in keywords[:10]:  # Max 10 keywords shown
            message += f"\n  • <code>{keyword}</code>"
        
        if len(keywords) > 10:
            message += f"\n  ... and {len(keywords) - 10} more"
        
        if suspect_urls:
            message += f"\n\n<b>Suspect URLs:</b>"
            for sus_url in suspect_urls[:5]:  # Max 5 suspect URLs
                message += f"\n  🔗 <code>{sus_url}</code>"
            if len(suspect_urls) > 5:
                message += f"\n  ... and {len(suspect_urls) - 5} more"
        
        message += f"\n\n<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_threat_resolved(self, url: str) -> bool:
        """Kirim notifikasi website sudah bersih (tidak lagi terdeteksi)"""
        message = f"""
✅ <b>THREAT RESOLVED</b>

<b>Website:</b> <code>{url}</code>

Website ini <b>tidak lagi terdeteksi</b> mengandung konten judol.

<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return self.send_message(message)

    def send_scan_summary(self, total: int, detected: int, errors: int) -> bool:
        """Kirim ringkasan scan results"""
        detection_rate = (detected / total * 100) if total > 0 else 0
        
        message = f"""
📊 <b>Scan Summary</b>

<b>Total Websites Scanned:</b> {total}
<b>Threats Detected:</b> {detected} ({detection_rate:.1f}%)
<b>Scan Errors:</b> {errors}

<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return self.send_message(message)
    
    def send_system_status(self, status: str, components: Dict) -> bool:
        """Kirim status sistem"""
        status_emoji = {
            "UP": "🟢",
            "DEGRADED": "🟡",
            "DOWN": "🔴"
        }
        
        emoji = status_emoji.get(status, "❓")
        
        message = f"""
{emoji} <b>System Status: {status}</b>

<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>Components:</b>
"""
        for component, state in components.items():
            component_emoji = "✅" if state == "UP" else "❌"
            message += f"\n  {component_emoji} {component}: {state}"
        
        return self.send_message(message)
    
    def send_daily_report(self, stats: Dict) -> bool:
        """Kirim laporan harian"""
        message = f"""
📈 <b>Daily Report</b>

<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}

<b>Metrics:</b>
• Total Websites: {stats.get('total_websites', 0)}
• Scans Performed: {stats.get('total_scans', 0)}
• Threats Detected: {stats.get('threats_detected', 0)}
• Detection Rate: {stats.get('detection_rate', '0')}%
• Peak Hour: {stats.get('peak_hour', 'N/A')}

<b>Top Keywords:</b>
"""
        if stats.get('top_keywords'):
            for i, (kw, count) in enumerate(stats['top_keywords'][:5], 1):
                message += f"\n  {i}. {kw} ({count}x)"
        
        message += f"\n\n<b>Most Threatened Sites:</b>"
        if stats.get('threatened_sites'):
            for i, (site, count) in enumerate(stats['threatened_sites'][:3], 1):
                message += f"\n  {i}. {site} ({count} detections)"
        
        return self.send_message(message)
    
    @staticmethod
    def _format_details(details: Dict) -> str:
        """Format details dict menjadi readable text"""
        formatted = ""
        for key, value in details.items():
            # Convert snake_case ke Title Case
            display_key = key.replace('_', ' ').title()
            
            if isinstance(value, list):
                formatted += f"\n<b>{display_key}:</b>"
                for item in value[:10]:
                    formatted += f"\n  • {item}"
                if len(value) > 10:
                    formatted += f"\n  ... and {len(value) - 10} more"
            elif isinstance(value, dict):
                formatted += f"\n<b>{display_key}:</b>"
                for k, v in value.items():
                    formatted += f"\n  {k}: {v}"
            else:
                formatted += f"\n<b>{display_key}:</b> <code>{value}</code>"
        
        return formatted


class NotificationManager:
    """Manager untuk multi-channel notifications"""
    
    def __init__(self):
        self.telegram = TelegramNotifier()
    
    def send_alert(self, level: str, title: str, details: Dict) -> bool:
        """
        Send alert ke semua configured channels
        
        Args:
            level: "CRITICAL", "WARNING", "INFO"
            title: Alert title
            details: Dictionary with alert details
        """
        results = []
        
        # Send to Telegram
        if self.telegram.is_configured():
            if level == "CRITICAL":
                results.append(self.telegram.send_alert_critical(title, details))
            elif level == "WARNING":
                results.append(self.telegram.send_alert_warning(title, details))
            else:
                results.append(self.telegram.send_alert_info(title, details))
        
        # Log result
        success = any(results) if results else False
        logger.info(f"Alert sent: {level} - {title} (Success: {success})")
        
        return success
    
    def send_threat_detection(self, url: str, keywords: List[str], severity: str, suspect_urls: Optional[List[str]] = None) -> bool:
        """Send threat detection notification"""
        results = []

        if self.telegram.is_configured():
            results.append(self.telegram.send_threat_detection(url, keywords, severity, suspect_urls))

        success = any(results) if results else False
        logger.info(f"Threat detection notification sent for {url} (Success: {success})")

        return success

    def send_threat_resolved(self, url: str) -> bool:
        """Send threat resolved notification"""
        results = []

        if self.telegram.is_configured():
            results.append(self.telegram.send_threat_resolved(url))

        success = any(results) if results else False
        logger.info(f"Threat resolved notification sent for {url} (Success: {success})")

        return success


# Global notification manager
notification_manager = NotificationManager()
