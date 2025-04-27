import streamlit as st
import pandas as pd
from datetime import datetime
import os

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
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
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

# ==== Guardar Datos en CSV ====
if enviar:
    nueva_respuesta = pd.DataFrame({
        "Fecha de Respuesta": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Nombre de quien llena": [nombre_persona],
        "Puesto": [puesto_persona],
        "Delegación": [delegacion],
        "Facilitador Evaluado": [facilitador],
        "Fecha del Taller": [fecha_encuesta.strftime("%Y-%m-%d")],
        "Dominio del Tema": [q1],
        "Claridad de Exposición": [q2],
        "Organización de Contenidos": [q3],
        "Uso de PowerPoint": [q4],
        "Promoción de Participación": [q5],
        "Aclaración de Dudas": [q6],
        "Metodología Empleada": [q7],
        "Actitud Motivadora": [q8],
        "Duración Adecuada": [q9],
        "Cumplimiento de Objetivos": [q10],
        "Aspecto Positivo": [aspecto_positivo],
        "Sugerencia de Mejora": [sugerencia_mejora]
    })

    # Si no existe el archivo, lo crea
    if not os.path.isfile('respuestas.csv'):
        nueva_respuesta.to_csv('respuestas.csv', index=False)
    else:
        respuestas = pd.read_csv('respuestas.csv')
        respuestas = pd.concat([respuestas, nueva_respuesta], ignore_index=True)
        respuestas.to_csv('respuestas.csv', index=False)

    st.success("✅ Evaluación enviada exitosamente.")
