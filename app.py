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

# Ajuste limpio de márgenes en Streamlit sin recortar la parte superior
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 1180px !important;
        }
        header[data-testid="stHeader"] {
            height: 1.5rem !important;
            background: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_WORD_PATH = os.path.join(BASE_DIR, "Protocolo_Unificado_SCA_CHGUV_2026.pdf")
PDF_PPT_PATH = os.path.join(BASE_DIR, "Presentacion_Protocolo_SCA_CHGUV_2026.pdf")
HTML_APP_PATH = os.path.join(BASE_DIR, "App_Interactiva_Protocolo_SCA_CHGUV.html")

if os.path.exists(HTML_APP_PATH):
    with open(HTML_APP_PATH, "r", encoding="utf-8") as f_html:
        html_content = f_html.read()

    b64_w = ""
    b64_p = ""
    if os.path.exists(PDF_WORD_PATH):
        with open(PDF_WORD_PATH, "rb") as fw:
            b64_w = base64.b64encode(fw.read()).decode("utf-8")

    if os.path.exists(PDF_PPT_PATH):
        with open(PDF_PPT_PATH, "rb") as fp:
            b64_p = base64.b64encode(fp.read()).decode("utf-8")

    # Inyectar descarga mediante Blob en la Pestaña 4 para que funcione dentro del contenedor de Streamlit
    blob_script = f"""
    <script>
      const B64_WORD_PDF = "{b64_w}";
      const B64_PPT_PDF = "{b64_p}";

      function downloadBase64Pdf(b64Data, fileName) {{
        if (!b64Data) return true;
        const byteCharacters = atob(b64Data);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {{
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }}
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], {{ type: "application/pdf" }});
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        return false;
      }}

      window.addEventListener("DOMContentLoaded", () => {{
        const btnWord = document.getElementById("link-dl-word-pdf");
        if (btnWord && B64_WORD_PDF) {{
          btnWord.onclick = (e) => {{
            e.preventDefault();
            downloadBase64Pdf(B64_WORD_PDF, "Protocolo_Unificado_SCA_CHGUV_2026.pdf");
          }};
        }}
        const btnPpt = document.getElementById("link-dl-ppt-pdf");
        if (btnPpt && B64_PPT_PDF) {{
          btnPpt.onclick = (e) => {{
            e.preventDefault();
            downloadBase64Pdf(B64_PPT_PDF, "Presentacion_Protocolo_SCA_CHGUV_2026.pdf");
          }};
        }}
      }});
    </script>
    """
    html_content = html_content.replace("</body>", blob_script + "
</body>")

    components.html(html_content, height=1120, scrolling=True)
else:
    st.error("No se encontró el archivo App_Interactiva_Protocolo_SCA_CHGUV.html en el directorio.")
