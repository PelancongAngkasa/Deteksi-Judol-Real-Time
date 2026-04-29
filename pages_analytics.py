import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_storage import ScanDataStorage
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Analytics - Deteksi Judol",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Analytics & Historical Data")
st.markdown("Analisis trend dan riwayat deteksi judol")

st.divider()

# Initialize storage
storage = ScanDataStorage()

# Sidebar for date range
with st.sidebar:
    st.header("Filter")
    lookback_hours = st.select_slider(
        "Lihat data terakhir:",
        options=[1, 3, 6, 12, 24, 48, 72],
        value=24
    )

# Get data
hourly_data = storage.get_hourly_data(lookback_hours)
stats = storage.get_statistics(lookback_hours)

# Main dashboard
if not hourly_data.empty:
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Deteksi", stats.get('total_detected', 0), delta=None, delta_color="inverse")
    
    with col2:
        st.metric("Total Scan", stats.get('total_scans', 0))
    
    with col3:
        st.metric("Detection Rate", stats.get('average_detection_rate', '0%'))
    
    with col4:
        st.metric("Peak Hour", stats.get('highest_detection_hour', '-'), 
                 delta=f"{stats.get('highest_detection_count', 0)} detected")
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Trend", "Detail", "Report", "Raw Data"])
    
    with tab1:
        # Trend line chart
        st.subheader("📊 Trend Deteksi Per Jam")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=hourly_data['jam'],
            y=hourly_data['detected_count'],
            mode='lines+markers',
            name='Terdeteksi',
            line=dict(color='#d32f2f', width=3),
            marker=dict(size=8, symbol='circle')
        ))
        
        fig.add_trace(go.Scatter(
            x=hourly_data['jam'],
            y=hourly_data['total_count'],
            mode='lines+markers',
            name='Total',
            line=dict(color='#1976d2', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=f"Trend Deteksi Judol ({lookback_hours} Jam Terakhir)",
            xaxis_title="Jam",
            yaxis_title="Jumlah Website",
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart
        st.subheader("🎯 Perbandingan Terdeteksi vs Aman Per Jam")
        
        hourly_data['aman'] = hourly_data['total_count'] - hourly_data['detected_count']
        
        fig_bar = go.Figure(data=[
            go.Bar(name='Terdeteksi', x=hourly_data['jam'], y=hourly_data['detected_count'], 
                  marker=dict(color='#d32f2f')),
            go.Bar(name='Aman', x=hourly_data['jam'], y=hourly_data['aman'], 
                  marker=dict(color='#388e3c'))
        ])
        
        fig_bar.update_layout(
            barmode='stack',
            title='Stacked Bar Chart - Deteksi vs Aman',
            xaxis_title='Jam',
            yaxis_title='Jumlah Website',
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.subheader("📋 Detail Per Jam")
        
        # Create detail dataframe
        detail_df = hourly_data[['jam', 'detected_count', 'total_count', 'detection_rate', 'timestamp']].copy()
        detail_df.columns = ['Jam', 'Terdeteksi', 'Total', 'Detection Rate', 'Update Terakhir']
        
        st.dataframe(detail_df, use_container_width=True)
        
        # Download button
        csv = detail_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data CSV",
            data=csv,
            file_name=f"judol_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with tab3:
        st.subheader("📄 Laporan Analisis")
        
        report = storage.generate_trend_report()
        
        st.code(report)
        
        # Copy button (simulated with text area)
        st.text_area("Laporan Lengkap:", value=report, height=300)
    
    with tab4:
        st.subheader("🗂️ Raw Data")
        
        st.write("Scan History (100 terakhir):")
        
        history = storage.get_scan_history(100)
        
        if history:
            history_df = pd.DataFrame([
                {
                    'Timestamp': h['timestamp'],
                    'Total Sites': h['total_sites'],
                    'Detected': h['detected_count'],
                    'Safe': h['safe_count'],
                    'Error': h['error_count'],
                    'Duration (s)': h.get('duration_seconds', '-')
                }
                for h in history
            ])
            
            st.dataframe(history_df, use_container_width=True, height=400)
            
            # Statistics
            st.subheader("Statistik Raw Data")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Sessions", len(history))
            
            with col2:
                avg_detected = history_df['Detected'].mean() if len(history) > 0 else 0
                st.metric("Rata-rata Terdeteksi/Session", f"{avg_detected:.1f}")
            
            with col3:
                avg_errors = history_df['Error'].mean() if len(history) > 0 else 0
                st.metric("Rata-rata Errors/Session", f"{avg_errors:.1f}")
        else:
            st.info("Tidak ada data scan history")

else:
    st.info("📊 Tidak ada data untuk ditampilkan. Jalankan scan terlebih dahulu untuk mengumpulkan data historis.")
    
    st.markdown("""
    **Tips:**
    1. Jalankan scan sesering mungkin untuk mengumpulkan data
    2. Gunakan fitur "Auto Scan 10 Menit" untuk monitoring berkelanjutan
    3. Data historis akan terakumulasi seiring waktu
    4. Gunakan filter di sidebar untuk melihat timerange yang berbeda
    """)

st.divider()
st.caption("📈 Analytics Dashboard | Last Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
