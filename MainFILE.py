import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from PIL import Image
import requests
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Medipedido - Servicios Médicos a Domicilio",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para crear un placeholder de imagen
def get_placeholder_image(width, height, color="#E0E0E0", text="Imagen"):
    return f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'%3E%3Crect width='{width}' height='{height}' fill='{color}'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%23888888' font-size='24'%3E{text}%3C/text%3E%3C/svg%3E"

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
    }
    .subheader {
        font-size: 1.8rem;
        color: #0D47A1;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .highlight {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .button-blue {
        background-color: #1E88E5;
        color: white;
        padding: 10px 24px;
        border-radius: 4px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    .top-buffer {
        margin-top: 2rem;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 14px;
        color: #757575;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image(get_placeholder_image(200, 80, text="Logo Medipedido"), caption="", width=200)
    st.header("Navegación")
    page = st.radio("", ["Inicio", "Sobre Nosotros", "Servicios", "Expansión a Argentina", "Contacto"])
    
    st.markdown("---")
    st.markdown("### Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    st.button("Entrar")
    
    st.markdown("---")
    st.markdown("### Descarga nuestra app")
    col1, col2 = st.columns(2)
    with col1:
        st.image(get_placeholder_image(100, 30, text="App Store"), width=100)
    with col2:
        st.image(get_placeholder_image(100, 30, text="Google Play"), width=100)

# Contenido principal
if page == "Inicio":
    st.markdown("<h1 class='main-header'>Bienvenido a Medipedido</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Su salud, a un click de distancia</h3>", unsafe_allow_html=True)
    
    # Hero image
    st.image(get_placeholder_image(800, 300, text="Médicos a domicilio"), width=800)
    
    st.markdown("<div class='highlight'>",
