import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re
import urllib3

# Suppress SSL warnings (we need to scan sites with invalid certs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Keywords untuk deteksi judi online
JUDOL_KEYWORDS = [
    'togel', 'slot', 'casino', 'betting', 'taruhan', 'judi', 'sportsbook',
    'poker', 'blackjack', 'roulette', 'toto', 'lotere', 'lotto',
    'perjudian', 'baccarat', 'bookie', 'gambling', 'wager', 'stakes','qq','jackpot',
    'gacor', 'jp', 'maxwin', 'rungkad'
]

class DeteksiJudol:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.results = []

    def scan_website(self, url):
        """Scan website untuk mendeteksi konten judol"""
        try:
            # First, check URL itself for keywords (fast detection)
            url_keywords = []
            url_lower = url.lower()
            for keyword in JUDOL_KEYWORDS:
                if keyword in url_lower:
                    url_keywords.append(keyword)
            
            # Try to get page content with SSL verification disabled
            response = requests.get(url, headers=self.headers, timeout=self.timeout, verify=False)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Hapus script dan style
                for script in soup(['script', 'style']):
                    script.decompose()
                
                text = soup.get_text().lower()
                html = response.text.lower()
                
                # Deteksi kata kunci
                found_keywords = []
                for keyword in JUDOL_KEYWORDS:
                    if re.search(r'\b' + keyword + r'\b', text):
                        found_keywords.append(keyword)
                
                # Combine with URL keywords
                all_keywords = list(set(url_keywords + found_keywords))
                
                # Deteksi URL mencurigakan di HTML
                suspect_urls = self._extract_suspicious_urls(html)
                
                result = {
                    'url': url,
                    'status': response.status_code,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'detected': len(all_keywords) > 0,
                    'keywords_found': all_keywords,
                    'keywords_count': len(all_keywords),
                    'suspect_urls': suspect_urls,
                    'page_title': soup.title.string if soup.title else 'N/A',
                    'error': None
                }
                return result
            else:
                return {
                    'url': url,
                    'status': response.status_code,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'detected': False,
                    'keywords_found': [],
                    'keywords_count': 0,
                    'suspect_urls': [],
                    'page_title': 'N/A',
                    'error': f'HTTP {response.status_code}'
                }
        except requests.exceptions.Timeout:
            return self._error_result(url, f'Timeout ({self.timeout}s)')
        except requests.exceptions.ConnectionError:
            return self._error_result(url, 'Connection Error')
        except requests.exceptions.SSLError:
            # SSL error - still check URL for keywords
            url_keywords = []
            url_lower = url.lower()
            for keyword in JUDOL_KEYWORDS:
                if keyword in url_lower:
                    url_keywords.append(keyword)
            
            return {
                'url': url,
                'status': 0,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'detected': len(url_keywords) > 0,
                'keywords_found': url_keywords,
                'keywords_count': len(url_keywords),
                'suspect_urls': [],
                'page_title': 'N/A',
                'error': 'SSL Certificate Error (detected from URL)'
            }
        except Exception as e:
            return self._error_result(url, str(e))
    
    def _extract_suspicious_urls(self, html):
        """Extract URLs yang mencurigakan dari HTML"""
        url_pattern = r'(?:href|src)=["\']([^"\']+)["\']'
        urls = re.findall(url_pattern, html)
        suspicious = []
        
        for url in urls:
            for keyword in JUDOL_KEYWORDS:
                if keyword in url.lower():
                    suspicious.append(url)
                    break
        
        return suspicious[:10]  # Limit 10 URLs
    
    def _error_result(self, url, error_msg):
        """Create error result"""
        return {
            'url': url,
            'status': 0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'detected': False,
            'keywords_found': [],
            'keywords_count': 0,
            'suspect_urls': [],
            'page_title': 'N/A',
            'error': error_msg
        }
    
    def scan_multiple(self, urls, delay=1):
        """Scan multiple websites dengan delay"""
        results = []
        for i, url in enumerate(urls, 1):
            try:
                print(f'[{i}/{len(urls)}] Scanning: {url}')
                result = self.scan_website(url)
                results.append(result)
                
                if i < len(urls):
                    time.sleep(delay)
            except Exception as e:
                print(f'Error scanning {url}: {e}')
        
        return results
    
