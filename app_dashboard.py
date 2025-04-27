import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import json

# ==== Conexión a Google Sheets ====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_dict = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(credentials)

# ==== Configuración inicial ====
SHEET_NAME = "respuestas_facilitadores"  # Cambia si tu Sheet se llama diferente
sheet = client.open(SHEET_NAME).sheet1

# ==== Cargar datos del Google Sheet ====
data = pd.DataFrame(sheet.get_all_records())

# ==== Estilo Streamlit oscuro =====
st.set_page_config(page_title="Dashboard Evaluación Facilitadores", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #3399FF;
    }
    label {
        color: #B3B3B3;
    }
    </style>
""", unsafe_allow_html=True)

# ==== Título ====
st.title("📊 Dashboard Evaluación Facilitadores")

# ==== Filtro por Facilitador ====
facilitadores = ["Todos"] + sorted(data["Facilitador Evaluado"].unique().tolist())
facilitador_seleccionado = st.selectbox("🔎 Selecciona un Facilitador", facilitadores)

if facilitador_seleccionado != "Todos":
    data = data[data["Facilitador Evaluado"] == facilitador_seleccionado]

# ==== Tabla editable (con AgGrid) ====
st.subheader("📝 Respuestas Registradas")
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_selection('multiple', use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    theme='dark',
    height=350,
    width='100%'
)

# ==== Gráficos de Evaluación ====
st.subheader("📈 Análisis de Evaluación")

preguntas = [
    "Dominio del Tema",
    "Claridad de Exposición",
    "Organización de Contenidos",
    "Uso de PowerPoint",
    "Promoción de Participación",
    "Aclaración de Dudas",
    "Metodología Empleada",
    "Actitud Motivadora",
    "Duración Adecuada",
    "Cumplimiento de Objetivos"
]

for pregunta in preguntas:
    st.markdown(f"### {pregunta}")
    fig = px.histogram(
        data,
        x=pregunta,
        color=pregunta,
        color_discrete_sequence=px.colors.qualitative.Safe,
        title=f"Distribución de respuestas en: {pregunta}"
    )
    fig.update_layout(
        xaxis_title=pregunta,
        yaxis_title="Cantidad de Respuestas",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==== Eliminar duplicados (por ahora localmente) ====
st.warning("⚠️ Por ahora la eliminación de respuestas en Google Sheets no es automática. Puedes gestionar limpieza manualmente.")
