import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Protocolo SCA CHGUV 2026 — Urgencias y Cardiología",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Reducir márgenes superiores de Streamlit para aprovechar toda la pantalla
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 1rem !important;
            max-width: 1200px !important;
        }
        div[data-testid="stDownloadButton"] > button {
            width: 100%;
            font-weight: 700;
            border-radius: 0.5rem;
            padding: 0.55rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_WORD_PATH = os.path.join(BASE_DIR, "Protocolo_Unificado_SCA_CHGUV_2026.pdf")
PDF_PPT_PATH = os.path.join(BASE_DIR, "Presentacion_Protocolo_SCA_CHGUV_2026.pdf")
HTML_APP_PATH = os.path.join(BASE_DIR, "App_Interactiva_Protocolo_SCA_CHGUV.html")

# Barra superior de descarga directa en PDF (Documento Protocolo y Presentación PPT por separado)
col1, col2 = st.columns(2)
with col1:
    if os.path.exists(PDF_WORD_PATH):
        with open(PDF_WORD_PATH, "rb") as f_word:
            st.download_button(
                label="📄 Descargar Documento del Protocolo Completo en PDF (Word -> PDF)",
                data=f_word.read(),
                file_name="Protocolo_Unificado_SCA_CHGUV_2026.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

with col2:
    if os.path.exists(PDF_PPT_PATH):
        with open(PDF_PPT_PATH, "rb") as f_ppt:
            st.download_button(
                label="📊 Descargar Presentación de Diapositivas en PDF (PPT -> PDF)",
                data=f_ppt.read(),
                file_name="Presentacion_Protocolo_SCA_CHGUV_2026.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

# Cargar la App Interactiva HTML e inyectar los enlaces data-URI para que también funcionen dentro del iframe
if os.path.exists(HTML_APP_PATH):
    with open(HTML_APP_PATH, "r", encoding="utf-8") as f_html:
        html_content = f_html.read()

    if os.path.exists(PDF_WORD_PATH):
        with open(PDF_WORD_PATH, "rb") as fw:
            b64_w = base64.b64encode(fw.read()).decode("utf-8")
            html_content = html_content.replace(
                'href="Protocolo_Unificado_SCA_CHGUV_2026.pdf"',
                f'href="data:application/pdf;base64,{b64_w}"'
            )

    if os.path.exists(PDF_PPT_PATH):
        with open(PDF_PPT_PATH, "rb") as fp:
            b64_p = base64.b64encode(fp.read()).decode("utf-8")
            html_content = html_content.replace(
                'href="Presentacion_Protocolo_SCA_CHGUV_2026.pdf"',
                f'href="data:application/pdf;base64,{b64_p}"'
            )

    components.html(html_content, height=1080, scrolling=True)
else:
    st.error("No se encontró el archivo App_Interactiva_Protocolo_SCA_CHGUV.html en el directorio.")
