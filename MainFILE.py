import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import base64

# --------------------------------------------
# CONFIGURACIÓN INICIAL
# --------------------------------------------

# Instale estos paquetes si no los tiene:
# pip install streamlit plotly-express pillow

st.set_page_config(
    page_title="MediPedido - Medicina a domicilio",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------
# DISEÑO Y ANIMACIONES
# --------------------------------------------

def setup_design():
    st.markdown("""
    <style>
    :root {
        --primary: #0083B8;
        --secondary: #00B4DB;
    }
    
    .stApp {
        background: #f9f9f9;
    }
    
    .card {
        border-radius: 15px;
        padding: 20px;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        margin-bottom: 20px;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .service-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        color: var(--primary);
    }
    
    .doctor-card {
        text-align: center;
        padding: 20px;
    }
    
    .doctor-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 auto 15px;
        border: 3px solid var(--primary);
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------------------------
# PÁGINA DE SERVICIOS
# --------------------------------------------

def servicios_page():
    st.title("📋 Nuestros Servicios Médicos")
    st.markdown("---")
    
    servicios = [
        {
            "icon": "🏠",
            "title": "Consultas a Domicilio",
            "desc": "Médicos generales y especialistas que acuden a tu hogar u oficina.",
            "details": ["Exámenes físicos", "Diagnósticos", "Recetas médicas", "Atención preventiva"]
        },
        {
            "icon": "💻",
            "title": "Telemedicina",
            "desc": "Consultas virtuales con especialistas desde la comodidad de tu casa.",
            "details": ["Videollamadas seguras", "Segundas opiniones", "Control de tratamientos"]
        },
        {
            "icon": "🩺",
            "title": "Servicios Especializados",
            "desc": "Atención de especialidades médicas en tu domicilio.",
            "details": ["Pediatría", "Geriatría", "Cardiología", "Neurología"]
        }
    ]
    
    cols = st.columns(3)
    for i, servicio in enumerate(servicios):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <div class="service-icon">{servicio['icon']}</div>
                <h3>{servicio['title']}</h3>
                <p>{servicio['desc']}</p>
                <ul>
                    {''.join([f'<li>{item}</li>' for item in servicio['details']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📌 ¿Cómo funciona?")
    
    pasos = [
        {"nro": 1, "desc": "Solicita una cita por app o llamada"},
        {"nro": 2, "desc": "Recibe confirmación con horario"},
        {"nro": 3, "desc": "El médico llega a tu domicilio"},
        {"nro": 4, "desc": "Recibe atención profesional"}
    ]
    
    cols = st.columns(4)
    for i, paso in enumerate(pasos):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="
                    width: 50px;
                    height: 50px;
                    background: var(--primary);
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 10px;
                    font-weight: bold;
                ">{paso['nro']}</div>
                <p>{paso['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# --------------------------------------------
# PÁGINA DE PROFESIONALES
# --------------------------------------------

def profesionales_page():
    st.title("👨‍⚕️ Nuestro Equipo Médico")
    st.markdown("---")
    
    st.subheader("Especialistas destacados")
    
    doctores = [
        {
            "nombre": "Dra. Laura Méndez",
            "especialidad": "Pediatría",
            "exp": "12 años",
            "img": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80"
        },
        {
            "nombre": "Dr. Carlos Rodríguez",
            "especialidad": "Cardiología",
            "exp": "18 años",
            "img": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80"
        },
        {
            "nombre": "Dra. Ana García",
            "especialidad": "Geriatría",
            "exp": "15 años",
            "img": "https://images.unsplash.com/photo-1594824476967-48c8b964273f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80"
        }
    ]
    
    cols = st.columns(3)
    for i, doctor in enumerate(doctores):
        with cols[i]:
            st.markdown(f"""
            <div class="card doctor-card">
                <img src="{doctor['img']}" class="doctor-img">
                <h3>{doctor['nombre']}</h3>
                <p style="color: var(--primary); font-weight: 500;">{doctor['especialidad']}</p>
                <p>Experiencia: {doctor['exp']}</p>
                <button style="
                    background: var(--primary);
                    color: white;
                    border: none;
                    padding: 8px 20px;
                    border-radius: 20px;
                    cursor: pointer;
                    margin-top: 10px;
                ">Ver disponibilidad</button>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏆 Certificaciones y convenios")
    
    st.markdown("""
    <div class="card">
        <p>Nuestros profesionales cuentan con:</p>
        <ul>
            <li>Certificación del Ministerio de Salud</li>
            <li>Matrícula profesional vigente</li>
            <li>Seguro de mala praxis</li>
            <li>Convenios con las principales obras sociales</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------
# APLICACIÓN PRINCIPAL
# --------------------------------------------

def main():
    setup_design()
    
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=MediPedido", width=150)
        st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["Inicio", "Servicios", "Profesionales", "Blog", "Contacto"],
        icons=["house", "clipboard-pulse", "people", "journal-text", "envelope"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"font-size": "16px"}
        }
    )
    
    if selected == "Servicios":
        servicios_page()
    elif selected == "Profesionales":
        profesionales_page()

if __name__ == "__main__":
    main()
