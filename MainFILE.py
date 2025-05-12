import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import base64
import time

# Configuration de la page
st.set_page_config(
    page_title="MediPedido - Medicina a domicilio",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Animation de fond
def add_bg_animation():
    st.markdown("""
    <style>
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .stApp {
        background: linear-gradient(270deg, #e6f7ff, #ffffff, #f0f9ff);
        background-size: 300% 300%;
        animation: gradientBG 15s ease infinite;
    }
    </style>
    """, unsafe_allow_html=True)

# Style CSS amélioré avec animations
def load_css():
    st.markdown("""
    <style>
        /* Animation des cartes */
        .feature-card {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 5px solid #0083B8;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        /* Animation des titres */
        .main-header {
            font-size: 3.5em;
            font-weight: 800;
            background: linear-gradient(90deg, #0083B8, #00B4DB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 30px;
            animation: fadeIn 1.5s ease;
        }
        
        .section-header {
            font-size: 2.5em;
            color: #0083B8;
            border-bottom: 3px solid #0083B8;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 30px;
            animation: slideIn 1s ease;
        }
        
        /* Effet de flottement pour les icônes */
        .floating-icon {
            animation: floating 3s ease-in-out infinite;
        }
        
        @keyframes floating {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        /* Bouton animé */
        .stButton>button {
            border: 2px solid #0083B8;
            color: white;
            background-color: #0083B8;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            background-color: white;
            color: #0083B8;
            transform: scale(1.05);
        }
    </style>
    """, unsafe_allow_html=True)

# En-tête animé
def show_header():
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 class="main-header">MediPedido</h1>
            <p style="font-size: 1.5em; animation: fadeIn 2s ease;">La medicina que llega a tu puerta</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Effet de vague décoratif
        st.markdown("""
        <svg viewBox="0 0 1200 120" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: -10px;">
            <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" fill="#0083B8"></path>
            <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" fill="#0083B8"></path>
            <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" fill="#0083B8"></path>
        </svg>
        """, unsafe_allow_html=True)

# Navigation stylisée
def create_navigation():
    return option_menu(
        menu_title=None,
        options=["Inicio", "Servicios", "Mercado", "Aspectos Legales", "Sostenibilidad", "Contacto"],
        icons=["house", "clipboard-pulse", "graph-up", "shield-check", "tree", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        key="main_navigation",
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": "rgba(255,255,255,0.7)",
                "backdrop-filter": "blur(10px)",
                "border-radius": "10px",
                "box-shadow": "0 4px 10px rgba(0,0,0,0.1)"
            },
            "icon": {"color": "#0083B8", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "center",
                "margin": "0px",
                "padding": "10px 20px",
                "--hover-color": "rgba(0,131,184,0.1)"
            },
            "nav-link-selected": {
                "background-color": "#0083B8",
                "font-weight": "bold",
                "border-radius": "10px"
            },
        }
    )

# Page d'accueil avec effets
def home_page():
    st.markdown("<div class='section-header'>Bienvenido a MediPedido</div>", unsafe_allow_html=True)
    
    # Animation de texte
    with st.empty():
        for i in range(3):
            st.markdown(f"<div style='font-size: 1.2em; animation: fadeIn 1s ease;'>🚀 {'Transformando' + '.'*i} la atención médica</div>", unsafe_allow_html=True)
            time.sleep(0.5)
        st.markdown("<div style='font-size: 1.2em;'>🚀 Transformando la atención médica con tecnología</div>", unsafe_allow_html=True)
    
    cols = st.columns([3, 2], gap="large")
    
    with cols[0]:
        st.markdown("""
        <div class='info-box' style='animation: slideIn 1s ease;'>
            <div class='sub-header'>Quiénes Somos</div>
            <p>MediPedido revoluciona el acceso a servicios médicos en Argentina mediante una plataforma digital innovadora.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[1]:
        st.markdown("""
        <div class='feature-card' style='animation: fadeIn 1.5s ease;'>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div class="floating-icon">💉</div>
                <div>
                    <h3 style="margin: 0;">Consultas médicas</h3>
                    <p style="margin: 5px 0 0;">Atención profesional en tu hogar</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Page Services avec effets
def services_page():
    st.markdown("<div class='section-header'>Nuestros Servicios</div>", unsafe_allow_html=True)
    
    # Solution visuelle améliorée pour les services
    service_options = {
        "Consultas a Domicilio": {"icon": "🏠", "color": "#0088cc"},
        "Telemedicina": {"icon": "📱", "color": "#00aa88"},
        "Servicios Especializados": {"icon": "⭐", "color": "#cc8800"},
        "Modelo de Negocio": {"icon": "💼", "color": "#8800cc"}
    }
    
    cols = st.columns(len(service_options))
    for i, (name, config) in enumerate(service_options.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: {config['color']};
                color: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transition: all 0.3s;
                cursor: pointer;
                margin-bottom: 20px;
                height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 2.5em; margin-bottom: 10px;">{config['icon']}</div>
                <h3 style="margin: 0;">{name}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # Contenu qui apparaît progressivement
    with st.expander("Ver detalles de servicios", expanded=True):
        st.markdown("""
        <div style="animation: fadeIn 2s ease;">
            <p>Descubre nuestra gama completa de servicios médicos innovadores:</p>
            <ul>
                <li>Consultas las 24 horas</li>
                <li>Especialistas certificados</li>
                <li>Cobertura con obras sociales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Page Contact avec effets
def contact_page():
    st.markdown("<div class='section-header'>Contacto</div>", unsafe_allow_html=True)
    
    # Formulaire stylisé
    with st.container():
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.9);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            animation: slideIn 1s ease;
        ">
        """, unsafe_allow_html=True)
        
        with st.form(key="contact_form"):
            cols = st.columns(2)
            with cols[0]:
                st.text_input("Nombre completo", key="contact_name")
                st.text_input("Correo electrónico", key="contact_email")
            with cols[1]:
                st.selectbox("Tema", ["Consulta general", "Soporte técnico"], key="contact_topic")
                st.text_area("Mensaje", height=100, key="contact_message")
            
            # Bouton animé
            if st.form_submit_button("Enviar mensaje ✉️", type="primary"):
                st.balloons()
                st.success("¡Mensaje enviado con éxito!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Application principale
def main():
    add_bg_animation()
    load_css()
    show_header()
    selected_page = create_navigation()
    
    if selected_page == "Inicio":
        home_page()
    elif selected_page == "Servicios":
        services_page()
    elif selected_page == "Mercado":
        market_page()
    elif selected_page == "Aspectos Legales":
        legal_page()
    elif selected_page == "Sostenibilidad":
        sustainability_page()
    elif selected_page == "Contacto":
        contact_page()

if __name__ == "__main__":
    main()
