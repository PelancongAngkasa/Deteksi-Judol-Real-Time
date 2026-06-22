"""
Deteksi Judol Real-Time Dashboard - Cortex XDR Style
Enterprise-grade security monitoring dashboard v2.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Deteksi Judol - Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Deteksi Judol v2.0 Enterprise Edition"}
)

# ==================== CONFIGURATION ====================
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ==================== CORTEX XDR THEME ====================
st.markdown("""
<style>
    :root {
        --primary-color: #d32f2f;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --background: #0f172a;
        --surface: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
    }
    
    .main { background-color: #0f172a; }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    
    .threat-card {
        background: linear-gradient(135deg, rgba(211,47,47,0.1) 0%, rgba(31,41,55,0.5) 100%);
        border-left: 4px solid #d32f2f;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .safe-card {
        background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(31,41,55,0.5) 100%);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .stButton > button {
        background-color: #d32f2f;
        color: white;
        border-radius: 6px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background-color: #b71c1c;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# ==================== API FUNCTIONS ====================
@st.cache_data(ttl=5)
def fetch_dashboard_data():
    """Fetch dashboard data dari API"""
    try:
        response = requests.get(f"{API_URL}/api/v1/dashboard", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

@st.cache_data(ttl=5)
def fetch_scan_status():
    """Fetch scan status"""
    try:
        response = requests.get(f"{API_URL}/api/v1/scan-status", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

@st.cache_data(ttl=5)
def fetch_websites():
    """Fetch all monitored websites (targets) from API"""
    try:
        response = requests.get(f"{API_URL}/api/v1/websites", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def trigger_manual_scan(urls):
    """Trigger manual scan"""
    try:
        payload = {"urls": urls, "priority": "urgent"}
        response = requests.post(
            f"{API_URL}/api/v1/scan/manual",
            json=payload,
            timeout=30
        )
        return response.json() if response.status_code == 200 else {"status": "error"}
    except Exception as e:
        return {"status": "error"}

def toggle_auto_scan(enabled):
    """Toggle auto-scan"""
    try:
        response = requests.post(
            f"{API_URL}/api/v1/scan/toggle-auto",
            params={"enabled": enabled},
            timeout=10
        )
        return response.json() if response.status_code == 200 else {"status": "error"}
    except Exception as e:
        return {"status": "error"}

# ==================== HELPER FUNCTIONS ====================
def format_large_number(num):
    """Format angka besar"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

def get_threat_color(rate):
    """Get color based on threat rate"""
    if rate >= 50:
        return "#d32f2f"
    elif rate >= 25:
        return "#f59e0b"
    elif rate >= 10:
        return "#3b82f6"
    else:
        return "#10b981"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("⚙️ Kontrol & Konfigurasi")
    
    scan_status = fetch_scan_status()
    
    if scan_status:
        is_auto = scan_status.get('auto_scan_enabled', False)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"{'🔴 Auto OFF' if not is_auto else '🟢 Auto ON'}", 
                        use_container_width=True):
                toggle_auto_scan(not is_auto)
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🔍 Scan Semua", use_container_width=True):
                ws = fetch_websites()
                active_urls = [w['url'] for w in ws if w.get('status') == 'active']
                if active_urls:
                    with st.spinner(f"Scanning {len(active_urls)} website..."):
                        result = trigger_manual_scan(active_urls)
                    if result.get('status') == 'success':
                        st.success(result.get('message', 'Selesai'))
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Scan gagal")
                else:
                    st.warning("Tidak ada website aktif")
    
    st.divider()
    
    st.subheader("📊 Status Sistem")
    if scan_status:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Websites", scan_status.get('total_websites', 0))
        with col2:
            st.metric("Threats", scan_status.get('total_detected_today', 0))
        
        if scan_status.get('last_scan_time'):
            last = datetime.fromisoformat(scan_status['last_scan_time'])
            diff = datetime.now() - last
            mins = int(diff.total_seconds() / 60)
            st.caption(f"⏱️ Last: {mins} min ago")

# ==================== MAIN DASHBOARD ====================
st.title("🛡️ Deteksi Defacement Judol Online")
st.markdown("Enterprise-grade Security Monitoring Dashboard")

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    status_text = "🟢 ONLINE" if scan_status and not scan_status.get('is_scanning') else "🟡 SCANNING"
    st.markdown(f"<div style='font-size: 20px; font-weight: bold;'>{status_text}</div>", unsafe_allow_html=True)
with col3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.divider()

dashboard_data = fetch_dashboard_data()

if not dashboard_data or dashboard_data.get('status') == 'error':
    st.error("❌ Gagal koneksi ke API Server")
    st.info("Pastikan FastAPI backend berjalan di http://localhost:8000")
else:
    data = dashboard_data.get('data', {})
    
    # ==================== TOP METRICS ====================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🌐 Websites",
            format_large_number(data.get('total_websites', 0)),
            delta="Monitoring"
        )
    
    with col2:
        detected = data.get('total_detected_today', 0)
        st.metric(
            "⚠️ Threats",
            format_large_number(detected),
            delta=f"{data.get('detection_rate', 0):.1f}% rate"
        )
    
    with col3:
        st.metric(
            "🔴 This Hour",
            data.get('total_detected_this_hour', 0),
            delta="60 min"
        )
    
    with col4:
        auto_status = "✅ ON" if data.get('auto_scan_enabled') else "⏸️ OFF"
        st.metric(
            "🔄 Auto-Scan",
            auto_status,
            delta="10 min"
        )
    
    st.divider()
    
    # ==================== TABS ====================
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Dashboard", "🚨 Recent Threats", "📈 Analytics", "⚙️ Settings"]
    )
    
    # ========== TAB 1: DASHBOARD ==========
    with tab1:
        hourly_data = data.get('hourly_data', [])
        if hourly_data and any(h.get('total_detected', 0) > 0 for h in hourly_data):
            df_hourly = pd.DataFrame(hourly_data)
            df_hourly['hour'] = pd.to_datetime(df_hourly['hour'])
            df_hourly = df_hourly.sort_values('hour')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_hourly['hour'],
                y=df_hourly['total_detected'],
                name='Threats',
                fill='tozeroy',
                line=dict(color='#d32f2f', width=3),
                fillcolor='rgba(211,47,47,0.2)'
            ))
            
            fig.update_layout(
                title="🎯 24-Hour Threat Timeline",
                xaxis_title="Time",
                yaxis_title="Count",
                template='plotly_dark',
                plot_bgcolor='rgba(31,41,55,0.5)',
                paper_bgcolor='#0f172a',
                font=dict(color='#f1f5f9'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Belum ada data scan. Dashboard akan menampilkan data setelah scan pertama.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            detection_rate = data.get('detection_rate', 0)
            fig_gauge = go.Figure(data=[go.Indicator(
                mode="gauge+number",
                value=detection_rate,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Detection Rate (%)"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': get_threat_color(detection_rate)},
                    'steps': [
                        {'range': [0, 25], 'color': "rgba(16,185,129,0.3)"},
                        {'range': [25, 50], 'color': "rgba(59,130,246,0.3)"},
                        {'range': [50, 75], 'color': "rgba(245,158,11,0.3)"},
                        {'range': [75, 100], 'color': "rgba(211,47,47,0.3)"}
                    ]
                }
            )])
            fig_gauge.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(31,41,55,0.5)',
                paper_bgcolor='#0f172a',
                font=dict(color='#f1f5f9'),
                height=400
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Statistics")
            
            stats_col1, stats_col2 = st.columns(2)
            with stats_col1:
                st.info(f"✅ Safe\n# {max(0, data.get('total_websites', 0) - data.get('total_detected_today', 0))}")
            with stats_col2:
                st.warning(f"🚨 Threats\n# {data.get('total_detected_today', 0)}")
            
            threat_level = ['🟢 Low', '🔵 Medium', '🟠 High', '🔴 Critical'][min(3, int(data.get('detection_rate', 0) / 25))]
            st.markdown(f"**Threat Level:** {threat_level}")
    
    # ========== TAB 2: RECENT THREATS ==========
    with tab2:
        st.subheader("🚨 Recent Detections")
        
        recent = data.get('recent_detections', [])
        
        if recent:
            for detection in recent[:10]:
                col_url, col_keywords, col_severity, col_action = st.columns([3, 2, 1, 1.5])
                
                # Get website URL if available
                website_id = detection['website_id']
                website_url = detection.get('website_url', f"ID: {website_id}")
                det_time = datetime.fromisoformat(detection['created_at']).strftime("%Y-%m-%d %H:%M:%S")
                
                with col_url:
                    st.markdown(f"**🌐 [{website_url}]({website_url})**")
                    st.caption(f"🕐 {det_time}")
                with col_keywords:
                    keywords = detection.get('keywords_found', [])
                    if keywords:
                        st.caption(f"🔍 {', '.join(keywords[:3])}")
                with col_severity:
                    severity = detection.get('severity', 'medium')
                    severity_icons = {'low': '🟡', 'medium': '🟠', 'high': '🔴'}
                    st.caption(f"{severity_icons.get(severity, '❓')} {severity.upper()}")
                with col_action:
                    if st.button("🔍 Details", key=f"det_{website_id}_{det_time}"):
                        st.info(f"**Website ID:** {website_id}\n**URL:** {website_url}\n**Keywords:** {', '.join(keywords)}")
                st.divider()
        else:
            st.info("✨ No threats detected. System running normally.")
    
    # ========== TAB 3: ANALYTICS ==========
    with tab3:
        st.subheader("📈 Defacement Detection Trends")
        
        hourly_data = data.get('hourly_data', [])
        if hourly_data:
            df = pd.DataFrame(hourly_data)
            df['hour'] = pd.to_datetime(df['hour'])
            df = df.sort_values('hour')
            
            # Chart 1: Detections over time
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['hour'],
                y=df['total_detected'],
                name='Defacement Detected',
                fill='tozeroy',
                line=dict(color='#d32f2f', width=3),
                fillcolor='rgba(211,47,47,0.2)',
                mode='lines+markers'
            ))
            
            fig.update_layout(
                title="📊 Website Defacement Detections (24H)",
                xaxis_title="Time",
                yaxis_title="Number of Websites Detected",
                template='plotly_dark',
                plot_bgcolor='rgba(31,41,55,0.5)',
                paper_bgcolor='#0f172a',
                font=dict(color='#f1f5f9'),
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                total_detected = df['total_detected'].sum()
                st.metric("Total Detected (24H)", total_detected)
            with col2:
                max_detected = df['total_detected'].max()
                st.metric("Peak Hour", max_detected)
            with col3:
                avg_detected = round(df['total_detected'].mean(), 2)
                st.metric("Average per Hour", avg_detected)
        else:
            st.info("📊 Waiting for scan data...")
    
    # ========== TAB 4: SETTINGS ==========
    with tab4:
        st.subheader("⚙️ System Settings")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Auto-Scan")
            current_auto = data.get('auto_scan_enabled', False)
            btn_auto_label = "⏸️ Nonaktifkan Auto-Scan" if current_auto else "▶️ Aktifkan Auto-Scan"
            if st.button(btn_auto_label, use_container_width=True):
                toggle_auto_scan(not current_auto)
                st.cache_data.clear()
                st.rerun()

        with col2:
            st.markdown("### Manual Scan")
            if st.button("🔍 Scan Semua Website", use_container_width=True):
                all_websites = fetch_websites()
                active_urls = [w['url'] for w in all_websites if w.get('status') == 'active']
                if active_urls:
                    with st.spinner(f"⏳ Scanning {len(active_urls)} website..."):
                        result = trigger_manual_scan(active_urls)
                    if result.get('status') == 'success':
                        st.success(result.get('message', 'Scan selesai'))
                        st.cache_data.clear()
                    else:
                        st.error(f"Gagal: {result.get('message', 'Unknown')}")
                else:
                    st.warning("Tidak ada website aktif untuk di-scan")

        st.divider()

        with st.expander("🔍 Scan URL Custom", expanded=False):
            manual_urls = st.text_area(
                "Masukkan URL (satu per baris):",
                height=150,
                placeholder="https://example.com\nhttps://example2.com"
            )
            if st.button("▶️ Mulai Scan", use_container_width=True):
                if manual_urls.strip():
                    urls_list = [u.strip() for u in manual_urls.split('\n') if u.strip()]
                    with st.spinner("⏳ Scanning..."):
                        result = trigger_manual_scan(urls_list)
                    if result.get('status') == 'success':
                        st.success(result.get('message', 'Scan selesai'))
                        st.cache_data.clear()
                    else:
                        st.error(f"Gagal: {result.get('message', 'Unknown')}")
                else:
                    st.warning("Masukkan minimal 1 URL")

        with st.expander("🎯 URL Targets (CRUD)", expanded=False):
            websites = fetch_websites()
            if not websites:
                st.info("Belum ada URL yang terdaftar.")
            else:
                df_sites = pd.DataFrame(websites)
                cols = [c for c in ['id', 'url', 'page_title', 'status', 'last_scan_time', 'created_at'] if c in df_sites.columns]
                st.dataframe(df_sites[cols], use_container_width=True, height=260)

                site_by_id = {s['id']: s for s in websites if 'id' in s}
                site_ids = list(site_by_id.keys())
                site_ids.sort()

                # Add
                with st.form("add_website_form", clear_on_submit=True):
                    st.markdown("### Tambah URL")
                    new_url = st.text_input("URL baru", placeholder="https://example.com")
                    new_page_title = st.text_input("Page Title (opsional)")
                    new_status = st.selectbox("Status", ["active", "inactive", "removed"], index=0)
                    add_submit = st.form_submit_button("Tambah URL")

                    if add_submit:
                        if not new_url.strip():
                            st.warning("URL wajib diisi.")
                            st.stop()

                        payload = {
                            "url": new_url.strip(),
                            "page_title": new_page_title.strip() or None,
                            "status": new_status,
                        }
                        try:
                            resp = requests.post(f"{API_URL}/api/v1/websites", json=payload, timeout=15)
                            if resp.status_code == 200:
                                st.success("URL berhasil ditambahkan.")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                detail = None
                                try:
                                    detail = resp.json().get("detail")
                                except Exception:
                                    pass
                                st.error(detail or f"Failed: {resp.text}")
                        except Exception as e:
                            st.error(f"Request error: {str(e)}")

                # Edit
                with st.form("edit_website_form"):
                    st.markdown("### Edit URL")
                    selected_edit_id = st.selectbox(
                        "Pilih target",
                        options=site_ids,
                        format_func=lambda sid: f"{sid} - {site_by_id[sid].get('url', '')}",
                    )
                    selected_site = site_by_id[selected_edit_id]

                    edit_url = st.text_input("URL", value=selected_site.get('url', ''), key=f"edit_url_{selected_edit_id}")
                    edit_page_title = st.text_input(
                        "Page Title",
                        value=selected_site.get('page_title') or '',
                        key=f"edit_title_{selected_edit_id}",
                    )
                    status_options = ["active", "inactive"]
                    current_status = selected_site.get("status") or "active"
                    edit_status_index = status_options.index(current_status) if current_status in status_options else 0
                    edit_status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=edit_status_index,
                        key=f"edit_status_{selected_edit_id}",
                    )

                    edit_submit = st.form_submit_button("Simpan perubahan")
                    if edit_submit:
                        payload = {
                            "url": edit_url.strip(),
                            "page_title": edit_page_title.strip() or None,
                            "status": edit_status,
                        }
                        if not payload["url"]:
                            st.warning("URL tidak boleh kosong.")
                            st.stop()

                        try:
                            resp = requests.put(
                                f"{API_URL}/api/v1/websites/{selected_edit_id}",
                                json=payload,
                                timeout=15,
                            )
                            if resp.status_code == 200:
                                st.success("URL berhasil diupdate.")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                detail = None
                                try:
                                    detail = resp.json().get("detail")
                                except Exception:
                                    pass
                                st.error(detail or f"Failed: {resp.text}")
                        except Exception as e:
                            st.error(f"Request error: {str(e)}")

                # Delete (soft)
                with st.form("delete_website_form"):
                    st.markdown("### Remove Website")
                    selected_del_id = st.selectbox(
                        "Pilih target",
                        options=site_ids,
                        format_func=lambda sid: f"{sid} - {site_by_id[sid].get('url', '')}",
                        key="del_target_select",
                    )
                    confirm = st.checkbox("Konfirmasi Delete")
                    del_submit = st.form_submit_button("Remove")

                    if del_submit:
                        if not confirm:
                            st.warning("Centang konfirmasi dulu.")
                            st.stop()
                        try:
                            resp = requests.delete(f"{API_URL}/api/v1/websites/{selected_del_id}", timeout=15)
                            if resp.status_code == 200:
                                st.success("Target berhasil di-remove.")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error(f"Failed: {resp.text}")
                        except Exception as e:
                            st.error(f"Request error: {str(e)}")

st.divider()
st.caption("🔐 Deteksi Judol v0.2")
