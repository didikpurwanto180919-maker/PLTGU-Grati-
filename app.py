import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="PLTGU Grati Blok 1 - Monitoring Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stAlert {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("⚡ PLTGU Grati Blok 1 - Operational Dashboard")
st.markdown("Real-time monitoring and data visualization dashboard for Start & Operational parameters.")

# Sidebar Configuration
st.sidebar.header("📁 Data Source Settings")
st.sidebar.info(
    "Catatan Akses SharePoint:\n\n"
    "Link SharePoint pribadi memerlukan autentikasi khusus. "
    "Untuk kemudahan pengoperasian langsung, Anda dapat mengunggah file data Excel/CSV ekspor dari folder tersebut di bawah ini, atau menggunakan mode Demo."
)

data_source = st.sidebar.radio("Pilih Sumber Data:", ["Gunakan Data Demo (Simulasi)", "Upload File Excel/CSV (SharePoint Export)"])

# Function to generate realistic dummy data for PLTGU Grati Blok 1
@st.cache_data
def load_demo_data():
    np.random.seed(42)
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='H')
    n = len(dates)
    
    df = pd.DataFrame({
        'Timestamp': dates,
        'Gas_Turbine_MW': np.random.normal(110, 5, n).clip(90, 130),
        'Steam_Turbine_MW': np.random.normal(55, 3, n).clip(45, 65),
        'Exhaust_Temp_C': np.random.normal(540, 10, n).clip(510, 570),
        'Fuel_Gas_Flow_Nm3h': np.random.normal(25000, 1200, n).clip(20000, 28000),
        'Vibration_MM_s': np.random.normal(1.8, 0.3, n).clip(0.5, 3.5),
        'Status': np.random.choice(['Normal', 'Warning', 'Standby'], size=n, p=[0.85, 0.10, 0.05])
    })
    return df

# Handle Data Loading
df = None

if data_source == "Gunakan Data Demo (Simulasi)":
    df = load_demo_data()
    st.sidebar.success("Berhasil memuat data simulasi PLTGU Grati Blok 1!")
else:
    uploaded_file = st.sidebar.file_uploader("Upload file Excel atau CSV dari SharePoint", type=['xlsx', 'csv'])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.success("File berhasil diunggah!")
        except Exception as e:
            st.sidebar.error(f"Gagal membaca file: {e}")
    else:
        st.warning("Silakan unggah file data melalui sidebar atau pilih 'Gunakan Data Demo' untuk melihat tampilan dashboard.")
        df = load_demo_data() # Fallback to demo so app doesn't break on first load

if df is not None and not df.empty:
    # Ensure Timestamp column exists and is datetime
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Sidebar Filters
    st.sidebar.header("🔍 Filter Parameter")
    if 'Timestamp' in df.columns and pd.api.types.is_datetime64_any_dtype(df['Timestamp']):
        min_date = df['Timestamp'].min().date()
        max_date = df['Timestamp'].max().date()
        date_range = st.sidebar.date_input("Rentang Tanggal", [min_date, max_date])
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            mask = (df['Timestamp'].dt.date >= start_date) & (df['Timestamp'].dt.date <= end_date)
            df_filtered = df.loc[mask]
        else:
            df_filtered = df
    else:
        df_filtered = df

    # Top KPI Metrics Cards
    st.subheader("📊 Key Performance Indicators (KPI)")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_gt = df_filtered['Gas_Turbine_MW'].mean() if 'Gas_Turbine_MW' in df_filtered.columns else 0
        st.metric(label="Rata-rata Daya GT", value=f"{avg_gt:.2f} MW", delta="+1.2% dari target")

    with col2:
        avg_st = df_filtered['Steam_Turbine_MW'].mean() if 'Steam_Turbine_MW' in df_filtered.columns else 0
        st.metric(label="Rata-rata Daya ST", value=f"{avg_st:.2f} MW", delta="+0.8%")

    with col3:
        avg_temp = df_filtered['Exhaust_Temp_C'].mean() if 'Exhaust_Temp_C' in df_filtered.columns else 0
        st.metric(label="Temperatur Gas Buang", value=f"{avg_temp:.1f} °C", delta="-0.5 °C")

    with col4:
        total_flow = df_filtered['Fuel_Gas_Flow_Nm3h'].mean() if 'Fuel_Gas_Flow_Nm3h' in df_filtered.columns else 0
        st.metric(label="Konsumsi Gas Rata-rata", value=f"{total_flow:,.0f} Nm³/h")

    st.markdown("---")

    # Interactive Charts Section
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📈 Tren Beban Pembangkit (GT & ST)")
        if 'Timestamp' in df_filtered.columns and 'Gas_Turbine_MW' in df_filtered.columns:
            fig_power = px.line(
                df_filtered, 
                x='Timestamp', 
                y=['Gas_Turbine_MW', 'Steam_Turbine_MW'],
                labels={'value': 'Daya (MW)', 'Timestamp': 'Waktu', 'variable': 'Unit'},
                title="Daya Gas Turbine & Steam Turbine"
            )
            fig_power.update_layout(template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_power, use_container_width=True)
        else:
            st.info("Kolom Timestamp atau Gas_Turbine_MW tidak ditemukan dalam data.")

    with col_chart2:
        st.subheader("🌡️ Temperatur Gas Buang & Getaran")
        if 'Timestamp' in df_filtered.columns and 'Exhaust_Temp_C' in df_filtered.columns:
            fig_temp = px.scatter(
                df_filtered, 
                x='Timestamp', 
                y='Exhaust_Temp_C', 
                color='Vibration_MM_s' if 'Vibration_MM_s' in df_filtered.columns else None,
                color_continuous_scale='Viridis',
                title="Korelasi Temperatur Gas Buang & Getaran"
            )
            fig_temp.update_layout(template="plotly_white")
            st.plotly_chart(fig_temp, use_container_width=True)
        else:
            st.info("Data temperatur tidak tersedia.")

    # Advanced Data Display & Search
    st.subheader("📋 Tabel Data Detail Operasional")
    
    with st.expander("🔍 Filter Kolom & Pencarian Data Mentah"):
        search_term = st.text_input("Cari Status atau Catatan:", "")
        if search_term and 'Status' in df_filtered.columns:
            df_display = df_filtered[df_filtered['Status'].str.contains(search_term, case=False, na=False)]
        else:
            df_display = df_filtered
        
        st.dataframe(df_display, use_container_width=True, height=300)

    # Download Button for Processed Data
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data Terfilter sebagai CSV",
        data=csv_data,
        file_name='pltgu_grati_blok1_report.csv',
        mime='text/csv'
    )

else:
    st.info("Silakan masukkan data atau aktifkan mode demo untuk menampilkan dashboard.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>PLTGU Grati Blok 1 - Monitoring & Analytics System © 2026</div>", unsafe_allow_html=True)