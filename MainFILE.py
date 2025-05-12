import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import datetime
from PIL import Image
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="MediPedido - Medicina a domicilio",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------
# FUNCIONES DE DISEÑO Y ANIMACIONES
# --------------------------------------------

def add_bg_animation():
    st.markdown("""
    <style>
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .stApp {
        background: linear-gradient(270deg, #f8f9fa, #e9f5ff, #f0f9ff);
        background-size: 300% 300%;
        animation: gradientBG 15s ease infinite;
    }
    
    .blog-card {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        transition: all 0.3s cubic-bezier(.25,.8,.25,1);
        margin-bottom: 30px;
        background: white;
    }
    
    .blog-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
    }
    
    .blog-header-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    .tag {
        display: inline-block;
        background: #0083B8;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8em;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated-entry {
        animation: fadeIn 0.8s ease-out forwards;
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------------------------
# COMPONENTES REUTILIZABLES
# --------------------------------------------

def doctor_card(name, specialty, experience, img_url):
    return f"""
    <div style="
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 10px;
        text-align: center;
        transition: all 0.3s;
    ">
        <img src="{img_url}" style="
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 15px;
            border: 4px solid #0083B8;
        ">
        <h3 style="margin: 0; color: #00506E;">Dr. {name}</h3>
        <p style="color: #0083B8; font-weight: 500;">{specialty}</p>
        <p style="font-size: 0.9em;">{experience} años de experiencia</p>
        <button style="
            background: #0083B8;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 20px;
            cursor: pointer;
            margin-top: 10px;
        ">Ver disponibilidad</button>
    </div>
    """

# --------------------------------------------
# PÁGINAS
# --------------------------------------------

def home_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #0083B8; font-size: 2.5em;">Bienvenido a MediPedido</h1>
        <p style="font-size: 1.2em;">La revolución en atención médica domiciliaria en Argentina</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estadísticas destacadas
    cols = st.columns(4)
    stats = [
        {"value": "10,000+", "label": "Pacientes atendidos"},
        {"value": "200+", "label": "Profesionales médicos"},
        {"value": "24/7", "label": "Disponibilidad"},
        {"value": "95%", "label": "Satisfacción del paciente"}
    ]
    
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <h2 style="color: #0083B8; margin: 0;">{stat['value']}</h2>
                <p>{stat['label']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Testimonios
    st.markdown("""
    <div style="margin: 40px 0;">
        <h2 style="color: #0083B8; border-bottom: 2px solid #0083B8; padding-bottom: 10px;">Testimonios de nuestros pacientes</h2>
    </div>
    """, unsafe_allow_html=True)
    
    testimonios = [
        {
            "nombre": "Carlos Gutiérrez",
            "edad": "68 años",
            "texto": "Desde que descubrí MediPedido, ya no necesito moverme para mis controles de diabetes. El servicio es excelente y los doctores muy profesionales.",
            "img": "https://randomuser.me/api/portraits/men/22.jpg"
        },
        {
            "nombre": "María López",
            "edad": "35 años",
            "texto": "Como madre de dos niños, el servicio de pediatría a domicilio ha sido un salvavidas. Rápido, eficiente y con un trato maravilloso.",
            "img": "https://randomuser.me/api/portraits/women/44.jpg"
        }
    ]
    
    for testimonio in testimonios:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
        ">
            <img src="{testimonio['img']}" style="
                width: 80px;
                height: 80px;
                border-radius: 50%;
                object-fit: cover;
                margin-right: 20px;
            ">
            <div>
                <h4 style="margin: 0 0 5px 0; color: #00506E;">{testimonio['nombre']} ({testimonio['edad']})</h4>
                <p style="margin: 0; font-style: italic;">"{testimonio['texto']}"</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def blog_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #0083B8; font-size: 2.5em;">Blog de Salud MediPedido</h1>
        <p style="font-size: 1.2em;">Consejos médicos, novedades y artículos de interés para tu bienestar</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de búsqueda y filtros
    with st.expander("🔍 Buscar artículos", expanded=False):
        col1, col2 = st.columns([3,1])
        with col1:
            search_query = st.text_input("Buscar por palabras clave")
        with col2:
            category = st.selectbox("Categoría", ["Todas", "Cardiología", "Pediatría", "Nutrición", "Prevención"])
    
    # Artículos del blog
    articulos = [
        {
            "titulo": "Cómo controlar la presión arterial en casa",
            "autor": "Dr. Javier Mendoza",
            "fecha": "15 Mayo 2023",
            "categoria": "Cardiología",
            "resumen": "Aprende técnicas efectivas para monitorear tu presión arterial y prevenir complicaciones cardiovasculares.",
            "imagen": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "tags": ["hipertensión", "salud cardiovascular", "prevención"]
        },
        {
            "titulo": "Alimentación saludable para niños en crecimiento",
            "autor": "Dra. Laura Fernández",
            "fecha": "2 Junio 2023",
            "categoria": "Pediatría",
            "resumen": "Guía completa de nutrición infantil con recomendaciones por edades y necesidades especiales.",
            "imagen": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "tags": ["nutrición infantil", "crecimiento", "alimentación"]
        },
        {
            "titulo": "Señales de alerta de la diabetes tipo 2",
            "autor": "Dra. Ana Rodríguez",
            "fecha": "28 Abril 2023",
            "categoria": "Prevención",
            "resumen": "Identifica los síntomas tempranos de la diabetes y cómo actuar para prevenir su desarrollo.",
            "imagen": "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "tags": ["diabetes", "prevención", "salud"]
        }
    ]
    
    for articulo in articulos:
        # Filtrado (simulado)
        if search_query and search_query.lower() not in articulo["titulo"].lower() and search_query.lower() not in articulo["resumen"].lower():
            continue
        if category != "Todas" and category != articulo["categoria"]:
            continue
        
        st.markdown(f"""
        <div class="blog-card animated-entry">
            <img src="{articulo['imagen']}" class="blog-header-img">
            <div style="padding: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="color: #0083B8; font-weight: 500;">{articulo['categoria']}</span>
                    <span style="color: #666; font-size: 0.9em;">{articulo['fecha']}</span>
                </div>
                <h3 style="margin: 0 0 10px 0; color: #00506E;">{articulo['titulo']}</h3>
                <p style="color: #666; margin-bottom: 15px;">{articulo['resumen']}</p>
                <div style="margin-bottom: 15px;">
                    {"".join([f'<span class="tag">{tag}</span>' for tag in articulo["tags"]])}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #666; font-size: 0.9em;">Por {articulo['autor']}</span>
                    <button style="
                        background: #0083B8;
                        color: white;
                        border: none;
                        padding: 8px 20px;
                        border-radius: 20px;
                        cursor: pointer;
                    ">Leer artículo completo</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------
# CONFIGURACIÓN PRINCIPAL
# --------------------------------------------

def main():
    add_bg_animation()
    
    # Barra de navegación superior
    selected = option_menu(
        menu_title=None,
        options=["Inicio", "Servicios", "Blog", "Profesionales", "Contacto"],
        icons=["house", "clipboard-pulse", "journal-text", "people", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "white", "box-shadow": "0 2px 10px rgba(0,0,0,0.1)"},
            "icon": {"color": "#0083B8", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "center",
                "margin": "0px",
                "padding": "10px 20px",
                "--hover-color": "#e6f7ff"
            },
            "nav-link-selected": {"background-color": "#0083B8"},
        }
    )
    
    # Mostrar página seleccionada
    if selected == "Inicio":
        home_page()
    elif selected == "Blog":
        blog_page()

if __name__ == "__main__":
    main()
