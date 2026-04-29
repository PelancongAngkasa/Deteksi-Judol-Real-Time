# 🏗️ Architecture & System Design

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│               END USER INTERFACE                         │
│                  Streamlit UI                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │  DASHBOARD LAYER                                   │ │
│  │  ┌──────────┬──────────┬──────────┬──────────────┐ │ │
│  │  │ Scan Tab │ Results  │ Analytics│ Export/Tools│ │ │
│  │  └──────────┴──────────┴──────────┴──────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↑↓
┌─────────────────────────────────────────────────────────┐
│            APPLICATION LAYER (app.py)                   │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Auto Scan Controller        │ Manual Scan          │ │
│  │ - 10min timer              │ - Single run         │ │
│  │ - 6 scans/2min interval    │ - URL input          │ │
│  │ - Session state management  │ - Direct results     │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Real-time Dashboard                                 │ │
│  │ - Countdown timer          - Metrics display        │ │
│  │ - Progress tracking        - Time series graph      │ │
│  │ - Session statistics       - Hourly summary         │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↑↓
┌─────────────────────────────────────────────────────────┐
│          SCANNING ENGINE (deteksi_judol.py)             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ DeteksiJudol Class                                 │ │
│  │ - HTTP requests (requests lib)                     │ │
│  │ - HTML parsing (BeautifulSoup)                     │ │
│  │ - Keyword detection (regex)                        │ │
│  │ - URL extraction & analysis                        │ │
│  │ - Error handling & logging                         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Input: URL list → Process: Scan → Output: Results     │
└─────────────────────────────────────────────────────────┘
                            ↑↓
┌─────────────────────────────────────────────────────────┐
│            DATA RETENTION LAYER                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Session State (Streamlit)                         │ │
│  │ - scan_history (in-memory)                        │ │
│  │ - detected_by_hour (aggregation)                  │ │
│  │ - total_scans, total_detected counters            │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Persistent Storage (data_storage.py)              │ │
│  │ - JSON: scan_history.json (sessions)              │ │
│  │ - CSV: hourly_summary.csv (aggregated data)       │ │
│  │ - Filesystem: scan_data/ directory                │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↑↓
┌─────────────────────────────────────────────────────────┐
│         ANALYTICS & REPORTING (pages_analytics.py)      │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Analytics Processor                               │ │
│  │ - Retrieve hourly data (24h, 48h, 72h)           │ │
│  │ - Calculate statistics                           │ │
│  │ - Generate trend reports                         │ │
│  │ - Create visualizations (Plotly)                 │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Report Generator (utils.py)                       │ │
│  │ - Text reports                                    │ │
│  │ - HTML reports                                    │ │
│  │ - CSV exports                                     │ │
│  │ - JSON serialization                              │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Auto Scan 10-Minute Flow

```
START AUTO SCAN
      ↓
  [Loop 6x]
  (every 10 minutes)
      ↓
  ┌─ Scan #1 at 0:00 ──┐
  │ Load URLs          │
  │ Call DeteksiJudol  → Process each URL → Extract results
  │ Get detected_count │
  │ Store in history   │
  │ Update display     │
  └────────────────────┘
      ↓ [Wait 2 min]
  ┌─ Scan #2 at 2:00 ──┐
  │ [Same process]     │
  └────────────────────┘
      ↓ [Pattern repeats]
  
  After Scan #6:
      ↓
  [ALL DATA]
  ├─ Session history (list)
  ├─ Detected by hour (dict)
  └─ Hourly summary (dict)
      ↓
  SAVE TO PERSISTENT STORAGE
  ├─ scan_history.json
  ├─ hourly_summary.csv
  └─ scan_results/ files
      ↓
  DISPLAY DASHBOARD
  ├─ Time series graph
  ├─ Hourly summary chart
  ├─ Session statistics
  └─ Real-time metrics
      ↓
  END AUTO SCAN
```

---

## Manual Scan Flow

```
LOAD URLs (list_web.txt)
      ↓
CLICK "MULAI SCAN"
      ↓
  [For each URL]
  - Make HTTP request
  - Parse HTML content
  - Extract text
  - Search for keywords
  - Extract suspicious URLs
  - Create result object
      ↓
COLLECT ALL RESULTS
      ↓
CALCULATE STATISTICS
  - Total websites
  - Detected count
  - Safe count
  - Error count
  - Keyword frequency
      ↓
DISPLAY RESULTS
  - Summary metrics
  - Tabbed results view
  - Charts & graphs
  - Download button
      ↓
END SCAN
```

---

## Data Model

### Scan Result Object
```python
{
    'url': str,                    # https://example.com
    'status': int,                 # 200, 404, 500, etc
    'timestamp': str,              # YYYY-MM-DD HH:MM:SS
    'detected': bool,              # True/False
    'keywords_found': [str],       # ['togel', 'slot']
    'keywords_count': int,         # 2
    'suspect_urls': [str],         # ['https://...']
    'page_title': str,             # Website title
    'error': str or None           # Error message if any
}
```

### Session Data Structure
```python
st.session_state = {
    'scan_history': [
        {
            'timestamp': datetime,
            'detected_count': int,
            'total_count': int,
            'hour': str
        },
        ...
    ],
    'detected_by_hour': {
        '10:00': 5,
        '11:00': 3,
        ...
    },
    'total_scans': int,
    'total_detected': int,
    'auto_scan_running': bool
}
```

### Hourly Summary
```csv
jam,detected_count,total_count,detection_rate,timestamp
10:00,5,20,25%,2024-01-15 10:30:00
11:00,3,20,15%,2024-01-15 11:30:00
12:00,7,20,35%,2024-01-15 12:30:00
```

---

## Module Dependencies

```
app.py (Main)
├── Imports deteksi_judol
├── Imports data_storage
├── Uses streamlit
├── Uses pandas
├── Uses plotly
└── Session state management

deteksi_judol.py (Scanner)
├── requests (HTTP)
├── BeautifulSoup (HTML parsing)
├── re (Regex)
└── datetime

data_storage.py (Storage)
├── json (Serialization)
├── csv (Export)
├── pandas (Data manipulation)
├── pathlib (File operations)
└── datetime

pages_analytics.py (Analytics)
├── Imports data_storage
├── Uses streamlit
├── Uses pandas
├── Uses plotly
└── datetime

utils.py (Utilities)
├── json (Serialization)
├── csv (Export)
├── logging (Logging)
└── datetime
```

---

## Request/Response Flow

### Single URL Scan

```
URL: https://example.com
  ↓
requests.get(url, headers, timeout)
  ↓
Response received
  ↓
Check status code
  ├─ 200 → Parse & analyze
  ├─ 404 → Error result
  └─ 5xx → Error result
  ↓
BeautifulSoup parse HTML
  ↓
Remove script & style tags
  ↓
Extract text content
  ↓
Search keywords (15 patterns)
  ├─ Find matches
  └─ Count occurrences
  ↓
Extract suspicious URLs
  ├─ Find all links
  └─ Filter by keyword
  ↓
Return result object
```

---

## Session State Lifecycle

```
┌─ Page Load ──────────────────────┐
│ If 'scan_history' not in state   │
│   → Initialize empty list        │
│ If 'detected_by_hour' not in state
│   → Initialize empty dict        │
│ ... (repeat for all keys)        │
└──────────────────────────────────┘
          ↓
┌─ During Auto Scan ───────────────┐
│ Loop 6 times:                    │
│   1. Perform scan                │
│   2. Update session_state        │
│   3. Update detected_by_hour     │
│   4. Display metrics             │
│   5. Sleep 2 minutes             │
└──────────────────────────────────┘
          ↓
┌─ On Completion ──────────────────┐
│ 1. Save to persistent storage    │
│ 2. Display dashboard             │
│ 3. Show analytics graphs         │
│ 4. Enable export buttons         │
└──────────────────────────────────┘
          ↓
┌─ Page Refresh ───────────────────┐
│ Streamlit reruns                 │
│ Session state persists           │
│ Data available for next scan     │
│ Or page exit                     │
└──────────────────────────────────┘
```

---

## Storage Architecture

### In-Memory (Session)
```
Streamlit Session
├─ scan_history: []
├─ detected_by_hour: {}
└─ Counters
    ├─ total_scans
    ├─ total_detected
    └─ last_scan_time
    
Duration: Until page refresh
Scope: Single browser session
```

### On-Disk (Persistent)
```
scan_data/
├─ scan_history.json
│  └─ [session1, session2, ...]
│     └─ {timestamp, total_sites, detected_count, ...}
│
└─ hourly_summary.csv
   └─ [hour1, hour2, ...]
      └─ {jam, detected_count, total_count, ...}

Duration: Permanent
Scope: All sessions
```

---

## UI Component Hierarchy

```
Streamlit App
├─ Header
│  ├─ Logo
│  ├─ Title
│  └─ Description
│
├─ Sidebar
│  ├─ Mode Selection
│  │  ├─ Manual Scan
│  │  └─ Auto Scan (10 Min)
│  ├─ URL Source
│  │  ├─ Load from file
│  │  └─ Upload file
│  ├─ Settings
│  │  ├─ Timeout slider
│  │  └─ Delay slider
│  ├─ Action Buttons
│  │  ├─ Start button
│  │  └─ Stop button (Auto)
│  └─ Statistics
│     ├─ Total scans
│     ├─ Total detected
│     └─ Last scan time
│
└─ Main Content
   ├─ Mode: Auto Scan
   │  ├─ Countdown display
   │  ├─ Progress tracking
   │  ├─ Real-time metrics
   │  ├─ Time series graph
   │  └─ Hourly summary
   │
   └─ Mode: Manual Scan
      ├─ Progress bar
      ├─ Results tabs
      │  ├─ Detected
      │  ├─ Safe
      │  ├─ Error
      │  └─ Detail
      ├─ Charts
      │  ├─ Pie chart
      │  └─ Bar chart
      └─ Export button
```

---

## Security Considerations

```
Input Validation
├─ URL format check (http/https)
├─ Timeout enforcement
└─ Request size limits

HTML Sanitization
├─ Remove script tags
├─ Remove style tags
└─ Text extraction only

Error Handling
├─ Try-except blocks
├─ Graceful degradation
└─ Error logging

Data Privacy
├─ No credentials stored
├─ No sensitive data exposed
└─ Local storage only
```

---

## Performance Metrics

```
Single URL Scan
├─ HTTP request: ~500ms-2s (depends on server)
├─ HTML parsing: ~10-50ms
├─ Keyword search: ~5-20ms
├─ Total per URL: ~600ms-2100ms
└─ Timeout: 10s (configurable)

10-Minute Auto Scan (5 URLs)
├─ 6 scans × 5 URLs = 30 URL scans
├─ Estimated time: 3-7 minutes (with 2-sec delays)
├─ Memory usage: ~50-100MB
└─ Data storage: ~50-100KB

Hourly Analytics Query
├─ Read CSV: ~10ms
├─ Parse data: ~5ms
├─ Generate charts: ~50-100ms
└─ Display: ~100-200ms
```

---

## Scalability Plan

### Current (Single Instance)
```
1 Streamlit app + 1 scanner + 1 storage
├─ Max URLs per scan: ~50
├─ Max concurrent users: 1 (Streamlit limitation)
└─ Storage: Local filesystem
```

### Future (Multi-instance)
```
Load Balancer
├─ Streamlit instances (horizontal scale)
└─ Shared storage
    ├─ Database (PostgreSQL/MongoDB)
    └─ Distributed cache (Redis)
```

---

## Disaster Recovery

```
Data Loss Prevention
├─ Regular backups of scan_data/
├─ Version control (git)
└─ Docker volume persistence

Failure Recovery
├─ Health checks in docker-compose
├─ Auto-restart policy
└─ Graceful degradation

Monitoring & Alerts
├─ Error logging
├─ Performance metrics
└─ Status dashboard
```

---

**Architecture Version**: 2.0
**Last Updated**: January 2024
**Status**: ✅ Production Ready

