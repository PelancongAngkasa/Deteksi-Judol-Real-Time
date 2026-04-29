import json
import csv
from datetime import datetime
from pathlib import Path
import logging

class ScanLogger:
    """Menyimpan dan manage hasil scan"""
    
    def __init__(self, log_dir='scan_results'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def save_scan_results(self, results, format='json'):
        """Save hasil scan dengan timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = self.log_dir / f'scan_{timestamp}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Hasil scan disimpan ke {filename}")
            return str(filename)
        
        elif format == 'csv':
            filename = self.log_dir / f'scan_{timestamp}.csv'
            if results:
                keys = results[0].keys()
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(results)
                self.logger.info(f"Hasil scan disimpan ke {filename}")
                return str(filename)
    
    def save_summary(self, results):
        """Save summary hasil scan"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        detected = sum(1 for r in results if r['detected'])
        safe = sum(1 for r in results if not r['detected'] and not r['error'])
        errors = sum(1 for r in results if r['error'])
        
        summary = {
            'timestamp': timestamp,
            'total_scanned': len(results),
            'detected': detected,
            'safe': safe,
            'errors': errors,
            'detection_rate': f"{(detected/len(results)*100):.1f}%" if results else "0%"
        }
        
        filename = self.log_dir / f'summary_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        return summary
    
    def get_report(self, results):
        """Generate text report"""
        report = []
        report.append("="*80)
        report.append("LAPORAN HASIL SCAN DEFACEMENT JUDOL ONLINE")
        report.append("="*80)
        report.append(f"Waktu Scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        detected = [r for r in results if r['detected']]
        safe = [r for r in results if not r['detected'] and not r['error']]
        errors = [r for r in results if r['error']]
        
        report.append("RINGKASAN:")
        report.append(f"  Total Website: {len(results)}")
        report.append(f"  ⚠️  Terdeteksi Judol: {len(detected)}")
        report.append(f"  ✓ Aman: {len(safe)}")
        report.append(f"  ❌ Error: {len(errors)}")
        report.append("")
        
        # Detected sites
        if detected:
            report.append("WEBSITE YANG TERDETEKSI JUDOL:")
            report.append("-"*80)
            for r in detected:
                report.append(f"  URL: {r['url']}")
                report.append(f"  Keywords: {', '.join(r['keywords_found'])}")
                report.append(f"  Count: {r['keywords_count']}")
                if r['suspect_urls']:
                    report.append(f"  Suspect URLs: {r['suspect_urls'][0]}")
                report.append("")
        
        # Errors
        if errors:
            report.append("WEBSITE DENGAN ERROR:")
            report.append("-"*80)
            for r in errors:
                report.append(f"  URL: {r['url']}")
                report.append(f"  Error: {r['error']}")
                report.append("")
        
        report.append("="*80)
        
        return "\n".join(report)
    
    def log_info(self, msg):
        self.logger.info(msg)
    
    def log_warning(self, msg):
        self.logger.warning(msg)
    
    def log_error(self, msg):
        self.logger.error(msg)


class ReportGenerator:
    """Generate laporan dalam berbagai format"""
    
    @staticmethod
    def generate_html_report(results, output_file='scan_report.html'):
        """Generate HTML report"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Laporan Scan Judol</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .header { background: #d32f2f; color: white; padding: 20px; border-radius: 5px; }
                .summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }
                .metric { background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .metric-value { font-size: 32px; font-weight: bold; color: #d32f2f; }
                .metric-label { color: #666; font-size: 14px; }
                table { width: 100%; border-collapse: collapse; background: white; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #f0f0f0; font-weight: bold; }
                .detected { background: #ffebee; color: #b71c1c; }
                .safe { background: #e8f5e9; color: #2e7d32; }
                .warning { background: #fff3e0; color: #e65100; }
                .footer { text-align: center; color: #666; margin-top: 40px; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🛡️ Laporan Scan Defacement Judol Online</h1>
                <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            </div>
        """
        
        # Summary metrics
        detected_count = sum(1 for r in results if r['detected'])
        safe_count = sum(1 for r in results if not r['detected'] and not r['error'])
        error_count = sum(1 for r in results if r['error'])
        
        html += f"""
            <div class="summary">
                <div class="metric">
                    <div class="metric-value">{len(results)}</div>
                    <div class="metric-label">Total Website</div>
                </div>
                <div class="metric" style="border-left: 4px solid #d32f2f;">
                    <div class="metric-value" style="color: #d32f2f;">{detected_count}</div>
                    <div class="metric-label">Terdeteksi Judol</div>
                </div>
                <div class="metric" style="border-left: 4px solid #388e3c;">
                    <div class="metric-value" style="color: #388e3c;">{safe_count}</div>
                    <div class="metric-label">Aman</div>
                </div>
                <div class="metric" style="border-left: 4px solid #f57c00;">
                    <div class="metric-value" style="color: #f57c00;">{error_count}</div>
                    <div class="metric-label">Error</div>
                </div>
            </div>
        """
        
        # Results table
        html += """
            <h2>Hasil Scan Detail</h2>
            <table>
                <tr>
                    <th>URL</th>
                    <th>Status</th>
                    <th>Terdeteksi</th>
                    <th>Keywords</th>
                    <th>Count</th>
                </tr>
        """
        
        for r in results:
            status_class = 'detected' if r['detected'] else ('safe' if not r['error'] else 'warning')
            detected_text = '⚠️ YA' if r['detected'] else ('✓ TIDAK' if not r['error'] else '❌ ERROR')
            keywords = ', '.join(r['keywords_found']) if r['keywords_found'] else ('-' if not r['error'] else r['error'])
            
            html += f"""
                <tr class="{status_class}">
                    <td><a href="{r['url']}" target="_blank">{r['url']}</a></td>
                    <td>{r['status']}</td>
                    <td>{detected_text}</td>
                    <td>{keywords}</td>
                    <td>{r['keywords_count']}</td>
                </tr>
            """
        
        html += """
            </table>
            <div class="footer">
                <p>🛡️ Sistem Monitoring Defacement Keamanan Website Kementerian Pertanian</p>
                <p>Laporan ini berisi informasi yang sensitif. Harap simpan dengan aman.</p>
            </div>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_file
