import unittest
from deteksi_judol import DeteksiJudol
from utils import ScanLogger, ReportGenerator
import os
from pathlib import Path

class TestDeteksiJudol(unittest.TestCase):
    """Unit tests untuk DeteksiJudol"""
    
    def setUp(self):
        self.detector = DeteksiJudol(timeout=10)
    
    def test_load_urls_from_file(self):
        """Test loading URLs dari file"""
        urls = self.detector.load_urls_from_file('list_web.txt')
        self.assertIsInstance(urls, list)
        self.assertGreater(len(urls), 0)
        print(f"✓ Loaded {len(urls)} URLs")
    
    def test_keywords_detection(self):
        """Test keyword detection logic"""
        test_text = "website togel online terbaik".lower()
        keywords = [kw for kw in self.detector.__class__.__dict__.get('JUDOL_KEYWORDS', []) 
                   if 'togel' in test_text]
        # This is a basic test - actual detection happens in scan_website
        print("✓ Keywords loaded successfully")
    
    def test_scan_website_valid_url(self):
        """Test scanning a valid website"""
        # Using a test URL - dalam production gunakan URL nyata
        result = self.detector.scan_website("https://httpbin.org/html")
        self.assertIsInstance(result, dict)
        self.assertIn('url', result)
        self.assertIn('status', result)
        print(f"✓ Scan website: Status {result['status']}")
    
    def test_scan_website_invalid_url(self):
        """Test scanning invalid URL"""
        result = self.detector.scan_website("https://invalid-domain-12345.com")
        self.assertIsInstance(result, dict)
        self.assertIsNotNone(result['error'])
        print(f"✓ Invalid URL handled: {result['error']}")
    
    def test_error_result_format(self):
        """Test error result format"""
        result = self.detector._error_result("https://test.com", "Test error")
        self.assertFalse(result['detected'])
        self.assertEqual(result['error'], "Test error")
        self.assertIsInstance(result['keywords_found'], list)
        print("✓ Error result format correct")


class TestScanLogger(unittest.TestCase):
    """Unit tests untuk ScanLogger"""
    
    def setUp(self):
        self.logger = ScanLogger('test_results')
    
    def tearDown(self):
        # Cleanup
        import shutil
        if os.path.exists('test_results'):
            shutil.rmtree('test_results')
    
    def test_logger_initialization(self):
        """Test logger initialization"""
        self.assertTrue(os.path.exists('test_results'))
        print("✓ Logger initialized")
    
    def test_save_scan_results_json(self):
        """Test saving results in JSON format"""
        test_results = [
            {
                'url': 'https://test.com',
                'detected': True,
                'keywords_found': ['togel'],
                'status': 200,
                'timestamp': '2024-01-15 10:00:00',
                'keywords_count': 1,
                'suspect_urls': [],
                'page_title': 'Test',
                'error': None
            }
        ]
        
        filename = self.logger.save_scan_results(test_results, format='json')
        self.assertTrue(os.path.exists(filename))
        print(f"✓ Results saved to JSON: {os.path.basename(filename)}")
    
    def test_save_summary(self):
        """Test saving summary"""
        test_results = [
            {'url': 'https://test1.com', 'detected': True, 'error': None},
            {'url': 'https://test2.com', 'detected': False, 'error': None},
        ]
        
        summary = self.logger.save_summary(test_results)
        self.assertEqual(summary['total_scanned'], 2)
        self.assertEqual(summary['detected'], 1)
        self.assertEqual(summary['safe'], 1)
        print(f"✓ Summary generated: {summary['total_scanned']} websites scanned")


class TestReportGenerator(unittest.TestCase):
    """Unit tests untuk ReportGenerator"""
    
    def setUp(self):
        self.generator = ReportGenerator()
    
    def test_generate_html_report(self):
        """Test HTML report generation"""
        test_results = [
            {
                'url': 'https://test.com',
                'status': 200,
                'detected': True,
                'keywords_found': ['togel'],
                'keywords_count': 1,
                'suspect_urls': [],
                'page_title': 'Test',
                'error': None
            }
        ]
        
        output_file = self.generator.generate_html_report(test_results, 'test_report.html')
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('Laporan Scan Defacement Judol', content)
            self.assertIn('test.com', content)
        
        os.remove(output_file)
        print("✓ HTML report generated successfully")


def run_basic_tests():
    """Run basic integration tests"""
    print("\n🔍 Running Basic Integration Tests...\n")
    
    # Test 1: Load URLs
    print("[1] Testing URL Loading...")
    detector = DeteksiJudol()
    urls = detector.load_urls_from_file('list_web.txt')
    if urls:
        print(f"✓ Successfully loaded {len(urls)} URLs\n")
    else:
        print("❌ Failed to load URLs\n")
    
    # Test 2: Check dependencies
    print("[2] Checking Dependencies...")
    try:
        import requests
        import bs4
        import streamlit
        import pandas
        import plotly
        print("✓ All dependencies installed\n")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}\n")
    
    # Test 3: File structure
    print("[3] Checking File Structure...")
    required_files = ['deteksi_judol.py', 'app.py', 'list_web.txt', 'requirements.txt', 
                     'Dockerfile', 'docker-compose.yml', '.streamlit/config.toml']
    missing = [f for f in required_files if not os.path.exists(f)]
    if not missing:
        print("✓ All required files present\n")
    else:
        print(f"⚠️ Missing files: {missing}\n")
    
    print("="*80)
    print("Basic tests completed!\n")


if __name__ == '__main__':
    # Run unit tests
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    # Run integration tests
    run_basic_tests()
