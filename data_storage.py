import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

class ScanDataStorage:
    """Menyimpan dan manage data scan historis untuk analisis"""
    
    def __init__(self, storage_dir='scan_data'):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.history_file = self.storage_dir / 'scan_history.json'
        self.hourly_file = self.storage_dir / 'hourly_summary.csv'
    
    def save_scan_session(self, session_data):
        """Simpan session scan ke JSON"""
        try:
            history = []
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            history.append({
                'timestamp': session_data['timestamp'].isoformat(),
                'total_sites': session_data['total_sites'],
                'detected_count': session_data['detected_count'],
                'safe_count': session_data['safe_count'],
                'error_count': session_data['error_count'],
                'duration_seconds': session_data.get('duration_seconds', 0),
                'scan_results': session_data.get('results', [])
            })
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving scan session: {e}")
            return False
    
    def save_hourly_summary(self, hour, detected_count, total_count):
        """Simpan ringkasan per jam"""
        try:
            data = []
            if self.hourly_file.exists():
                data = pd.read_csv(self.hourly_file).to_dict('records')
            
            # Check if hour already exists and update or add
            hour_exists = False
            for entry in data:
                if entry['jam'] == hour:
                    entry['detected_count'] = max(entry['detected_count'], detected_count)
                    entry['total_count'] = max(entry['total_count'], total_count)
                    entry['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    hour_exists = True
                    break
            
            if not hour_exists:
                data.append({
                    'jam': hour,
                    'detected_count': detected_count,
                    'total_count': total_count,
                    'detection_rate': f"{(detected_count/total_count*100):.1f}%" if total_count > 0 else "0%",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            df = pd.DataFrame(data)
            df.to_csv(self.hourly_file, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error saving hourly summary: {e}")
            return False
    
    def get_hourly_data(self, hours_lookback=24):
        """Ambil data deteksi per jam untuk N jam terakhir"""
        try:
            if not self.hourly_file.exists():
                return pd.DataFrame()
            
            df = pd.read_csv(self.hourly_file)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filter untuk N jam terakhir
            cutoff_time = datetime.now() - timedelta(hours=hours_lookback)
            df_filtered = df[df['timestamp'] >= cutoff_time]
            
            return df_filtered.sort_values('jam')
        except Exception as e:
            print(f"Error reading hourly data: {e}")
            return pd.DataFrame()
    
    def get_scan_history(self, limit=100):
        """Ambil N scan terakhir"""
        try:
            if not self.history_file.exists():
                return []
            
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            return history[-limit:]
        except Exception as e:
            print(f"Error reading scan history: {e}")
            return []
    
    def get_statistics(self, hours_lookback=24):
        """Dapatkan statistik keseluruhan"""
        try:
            hourly_data = self.get_hourly_data(hours_lookback)
            
            if hourly_data.empty:
                return {
                    'total_scans': 0,
                    'total_detected': 0,
                    'average_detection_rate': 0,
                    'highest_detection_hour': None,
                    'highest_detection_count': 0
                }
            
            stats = {
                'total_scans': len(hourly_data),
                'total_detected': int(hourly_data['detected_count'].sum()),
                'average_detection_rate': f"{hourly_data['detected_count'].sum() / hourly_data['total_count'].sum() * 100:.1f}%" 
                    if hourly_data['total_count'].sum() > 0 else "0%",
                'highest_detection_hour': hourly_data.loc[hourly_data['detected_count'].idxmax()]['jam']
                    if not hourly_data.empty else None,
                'highest_detection_count': int(hourly_data['detected_count'].max()) if not hourly_data.empty else 0
            }
            
            return stats
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return {}
    
    def generate_trend_report(self):
        """Generate laporan trend"""
        try:
            hourly_data = self.get_hourly_data(24)
            
            if hourly_data.empty:
                return "Tidak ada data untuk dianalisis"
            
            report = []
            report.append("=" * 60)
            report.append("LAPORAN TREND DETEKSI JUDOL (24 JAM TERAKHIR)")
            report.append("=" * 60)
            
            for idx, row in hourly_data.iterrows():
                report.append(f"\n{row['jam']}")
                report.append(f"  Terdeteksi: {row['detected_count']} website")
                report.append(f"  Total: {row['total_count']} website")
                report.append(f"  Rate: {row['detection_rate']}")
            
            stats = self.get_statistics(24)
            report.append("\n" + "=" * 60)
            report.append("RINGKASAN")
            report.append("=" * 60)
            report.append(f"Total Deteksi (24 jam): {stats['total_detected']}")
            report.append(f"Rata-rata Detection Rate: {stats['average_detection_rate']}")
            report.append(f"Jam Tertinggi: {stats['highest_detection_hour']} ({stats['highest_detection_count']} website)")
            
            return "\n".join(report)
        except Exception as e:
            return f"Error generating report: {e}"


class RealTimeMonitor:
    """Monitor real-time untuk sesion scan 10 menit"""
    
    def __init__(self):
        self.scan_history = []
        self.start_time = None
        self.end_time = None
    
    def start_session(self):
        """Mulai monitoring session"""
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=10)
        self.scan_history = []
    
    def add_scan(self, detected_count, total_count):
        """Tambah scan result"""
        entry = {
            'timestamp': datetime.now(),
            'detected_count': detected_count,
            'total_count': total_count,
            'detection_rate': (detected_count / total_count * 100) if total_count > 0 else 0
        }
        self.scan_history.append(entry)
    
    def get_session_summary(self):
        """Dapatkan summary sesion"""
        if not self.scan_history:
            return {}
        
        total_detected = sum(s['detected_count'] for s in self.scan_history)
        total_scanned = sum(s['total_count'] for s in self.scan_history)
        
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_scans': len(self.scan_history),
            'total_detected': total_detected,
            'total_scanned': total_scanned,
            'average_detection_rate': (total_detected / total_scanned * 100) if total_scanned > 0 else 0,
            'scan_history': self.scan_history
        }
    
    def is_active(self):
        """Check apakah session masih aktif"""
        return datetime.now() < self.end_time if self.end_time else False
    
    def get_remaining_time(self):
        """Dapatkan sisa waktu monitoring"""
        if not self.end_time:
            return 0
        
        remaining = (self.end_time - datetime.now()).total_seconds()
        return max(0, remaining)
