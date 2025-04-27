import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
import os

# ==== Leer Credenciales desde Secrets ====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_dict = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(credentials)

# Abre el Google Sheet
SHEET_NAME = "respuestas_facilitadores"  # Cambia si tu Sheet tiene otro nombre
sheet = client.open(SHEET_NAME).sheet1

# ==== CSS Personalizado ====
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
st.title("📝 Evaluación de Facilitadores - Estrategia Sembremos Seguridad")

# ==== Formulario ====
with st.form("formulario_evaluacion"):

    st.subheader("🔹 Datos Generales")
    nombre_persona = st.text_input("Nombre de quien llena la encuesta")
    puesto_persona = st.text_input("Puesto que desempeña")
    delegacion = st.text_input("Delegación")
    facilitador = st.selectbox(
        "Nombre del Facilitador",
        [
            "Esteban Cordero Solórzano",
            "Pamela Montero Pérez",
            "Jannia Valles Brizuela",
            "Manfred Rivera Meneses",
            "Carlos Castro Loaiciga",
            "Adrián Alvarado García",
            "Luis Vásquez Solís"
        ]
    )
    fecha_encuesta = st.date_input("Fecha")

    st.subheader("🔹 Evaluación de Facilitadores")
    opciones = ["Excelente", "Muy Bueno", "Bueno", "Regular", "Deficiente"]

    q1 = st.selectbox("¿El facilitador demostró dominio del tema tratado?", opciones)
    q2 = st.selectbox("¿La exposición del facilitador fue clara y comprensible?", opciones)
    q3 = st.selectbox("¿El facilitador organizó de manera adecuada los contenidos del taller?", opciones)
    q4 = st.selectbox("¿El facilitador utilizó adecuadamente la presentación en PowerPoint como apoyo?", opciones)
    q5 = st.selectbox("¿El facilitador promovió la participación activa de los asistentes?", opciones)
    q6 = st.selectbox("¿El facilitador aclaró dudas y consultas de manera efectiva?", opciones)
    q7 = st.selectbox("¿La metodología empleada fue adecuada para alcanzar los objetivos del taller?", opciones)
    q8 = st.selectbox("¿El facilitador mantuvo una actitud respetuosa y motivadora?", opciones)
    q9 = st.selectbox("¿La duración de las actividades fue adecuada?", opciones)
    q10 = st.selectbox("¿Se cumplieron los objetivos planteados al inicio del taller?", opciones)

    st.subheader("🔹 Retroalimentación Abierta")
    aspecto_positivo = st.text_area("¿Qué aspectos positivos destaca del desempeño del facilitador?")
    sugerencia_mejora = st.text_area("¿Qué sugerencias haría para mejorar futuras sesiones?")

    enviar = st.form_submit_button("📤 Enviar Evaluación")

# ==== Guardar Datos en Google Sheets ====
if enviar:
    nueva_fila = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        nombre_persona,
        puesto_persona,
        delegacion,
        facilitador,
        fecha_encuesta.strftime("%Y-%m-%d"),
        q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
        aspecto_positivo,
        sugerencia_mejora
    ]

    sheet.append_row(nueva_fila)
    st.success("✅ Evaluación enviada exitosamente a Google Sheets.")
