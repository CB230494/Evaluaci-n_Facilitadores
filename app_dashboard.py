import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# ==== Estilo Oscuro =====
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

st.title("📊 Dashboard Evaluación Facilitadores")

# ==== Cargar los datos ====
try:
    data = pd.read_csv('respuestas.csv')
except FileNotFoundError:
    st.error("❌ No se encontró el archivo respuestas.csv. Llena al menos una evaluación.")
    st.stop()

# ==== Filtros ====
facilitadores = ["Todos"] + sorted(data["Facilitador Evaluado"].unique().tolist())
facilitador_seleccionado = st.selectbox("🔎 Selecciona un Facilitador", facilitadores)

if facilitador_seleccionado != "Todos":
    data = data[data["Facilitador Evaluado"] == facilitador_seleccionado]

# ==== Tabla de Respuestas (editable) ====
st.subheader("📝 Respuestas Registradas")
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_selection('multiple', use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    theme='dark',
    height=300,
    width='100%'
)

# ==== Botón para eliminar registros seleccionados ====
if st.button("🗑️ Eliminar Respuestas Seleccionadas"):
    selected = grid_response["selected_rows"]
    if selected:
        selected_indices = [row['_selectedRowNodeInfo']['nodeRowIndex'] for row in selected]
        data = data.drop(selected_indices)
        data.to_csv('respuestas.csv', index=False)
        st.success("✅ Respuestas eliminadas correctamente. Recarga el dashboard.")
    else:
        st.warning("⚠️ No seleccionaste ninguna fila para eliminar.")

# ==== Gráficos de Evaluación ====
st.subheader("📈 Gráficos de Evaluación del Facilitador")

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
        yaxis_title="Número de respuestas",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

