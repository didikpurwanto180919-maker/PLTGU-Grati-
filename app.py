from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="PLTGU Grati Blok 1 - Operational Dashboard",
    page_icon="⚡",
    layout="wide",
)

# Judul Utama Dashboard
st.title("⚡ PLTGU Grati Blok 1 - Operational Dashboard")
st.markdown(
    "Dashboard pemantauan parameter operasional Start & Unit PLTGU Grati Blok 1."
)

# Sidebar untuk Pengaturan Data Source
st.sidebar.header("📁 Data Source Settings")
st.sidebar.markdown(
    """
**Akses SharePoint:**
Tautan folder SharePoint Anda memerlukan autentikasi login akun perusahaan. 
Untuk pengoperasian cepat, silakan **unduh file Excel/CSV** dari folder SharePoint berikut:
[Buka Folder SharePoint START PLTGU GRATI BLOK 1](https://indonesiapower-my.sharepoint.com/:f:/r/personal/didik_purwanto_plnindonesiapower_co_id/Documents/START%20PLTGU%20GRATI%20BLOK%201?d=wedb662df387b4f0eb14c4f78639482fd&csf=1&web=1&e=izzQI6)
kemudian unggah file tersebut di bawah ini.
"""
)

data_source = st.sidebar.radio(
    "Pilih Sumber Data:",
    ["Gunakan Data Demo (Simulasi)", "Upload File Excel/CSV dari SharePoint"],
)


@st.cache_data
def load_demo_data():
  # Perbaikan frekuensi waktu menggunakan 'h' kecil agar kompatibel dengan pandas versi terbaru
  dates = pd.date_range(
      start=datetime.now() - timedelta(days=7),
      end=datetime.now(),
      freq="h",
  )
  np.random.seed(42)
  df_demo = pd.DataFrame({
      "Timestamp": dates,
      "GT_Load_MW": np.random.uniform(100, 150, len(dates)),
      "ST_Load_MW": np.random.uniform(50, 75, len(dates)),
      "Condenser_Vacuum_barg": np.random.uniform(0.80, 0.95, len(dates)),
      "Exhaust_Gas_Temp_C": np.random.uniform(520, 560, len(dates)),
  })
  return df_demo


df = None

if data_source == "Gunakan Data Demo (Simulasi)":
  df = load_demo_data()
  st.sidebar.success("Menggunakan mode data simulasi operasional.")
else:
  uploaded_file = st.sidebar.file_uploader(
      "Upload file Excel (.xlsx) atau CSV", type=["xlsx", "csv"]
  )
  if uploaded_file is not None:
    try:
      if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
      else:
        df = pd.read_excel(uploaded_file)
      st.sidebar.success("File berhasil dimuat!")
    except Exception as e:
      st.sidebar.error(f"Gagal membaca file: {e}")
  else:
      st.sidebar.info(
          "Silakan unggah file Excel/CSV hasil ekspor dari SharePoint."
      )
      df = load_demo_data()  # Fallback ke demo jika belum upload

if df is not None and not df.empty:
  # Tampilkan Ringkasan Metrik Utama di Bagian Atas
  st.subheader("📊 Ringkasan Parameter Operasional")

  # Cari kolom numerik yang tersedia untuk metrik
  numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    col1.metric("Total Record Data", f"{len(df):,} Baris")
  with col2:
    if len(numeric_cols) > 0:
      col2.metric(
          f"Rata-rata {numeric_cols[0]}",
          f"{df[numeric_cols[0]].mean():.2f}",
      )
  with col3:
    if len(numeric_cols) > 1:
      col3.metric(
          f"Rata-rata {numeric_cols[1]}",
          f"{df[numeric_cols[1]].mean():.2f}",
      )
  with col4:
    if "Condenser_Vacuum_barg" in df.columns:
      low_vacuum_count = (df["Condenser_Vacuum_barg"] < 0.85).sum()
      col4.metric(
          "Status Vacuum < 0.85 barg",
          f"{low_vacuum_count} Peringatan",
          delta_color="inverse",
      )

  st.markdown("---")

  # Bagian Visualisasi Grafik Interaktif Plotly
  st.subheader("📈 Grafik Tren Parameter")
  time_col = None
  for col in df.columns:
    if "time" in col.lower() or "date" in col.lower() or "tanggal" in col.lower():
      time_col = col
      break

  if time_col and len(numeric_cols) > 0:
    selected_metric = st.selectbox(
        "Pilih Parameter untuk Ditampilkan:", numeric_cols
    )
    fig = px.line(
        df,
        x=time_col,
        y=selected_metric,
        title=f"Tren Waktu - {selected_metric}",
        template="plotly_dark",
    )
    st.plotly_chart(fig, use_container_width=True)
  else:
    # Jika tidak ada kolom waktu khusus, plot scatter/line biasa
    selected_metric = st.selectbox(
        "Pilih Parameter:", df.select_dtypes(include=[np.number]).columns
    )
    st.line_chart(df[selected_metric])

  # Tampilkan Tabel Data Mentah
  with st.expander("🔍 Lihat Data Mentah (Raw Data Table)"):
    st.dataframe(df, use_container_width=True)
