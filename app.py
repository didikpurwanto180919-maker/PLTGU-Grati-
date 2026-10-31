import streamlit as st

# Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="PLTGU Grati Blok 1 - SharePoint Access",
    page_icon="⚡",
    layout="centered",
)

# Tampilan Utama Dashboard
st.title("⚡ PLTGU Grati Blok 1")
st.markdown("### Akses Repository Dokumen & Data Operasional")

st.markdown("---")

# Kotak Informasi/Tautan Menarik
st.info(
    "Silakan klik tombol di bawah ini untuk langsung mengakses folder penyimpanan resmi di SharePoint."
)

# Tombol Tautan Langsung ke SharePoint
st.markdown(
    """
    <div style="text-align: center; padding: 30px;">
        <a href="https://indonesiapower-my.sharepoint.com/:f:/r/personal/didik_purwanto_plnindonesiapower_co_id/Documents/START%20PLTGU%20GRATI%20BLOK%201?d=wedb662df387b4f0eb14c4f78639482fd&csf=1&web=1&e=izzQI6" target="_blank">
            <button style="background-color: #0078D4; color: white; padding: 15px 30px; font-size: 18px; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
                📂 Buka Folder SharePoint START PLTGU GRATI BLOK 1
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.caption(
    "PLTGU Grati UBP Grati • PT PLN Indonesia Power © 2026"
)
