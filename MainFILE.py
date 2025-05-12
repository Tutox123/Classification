import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
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
                margin-bottom: 20px;
                height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 2.5em; margin-bottom: 10px;">{config['icon']}</div>
                <h3 style="margin: 0;">{name}</h3>
            </div>
            """, unsafe_allow_html=True)

# Page Marché avec effets
def market_page():
    st.markdown("<div class='section-header'>Análisis del Mercado Argentino</div>", unsafe_allow_html=True)
    
    # Graphique animé
    data = pd.DataFrame({
        'Año': [2020, 2021, 2022, 2023, 2024],
        'Crecimiento (%)': [15, 22, 35, 42, 50]
    })
    
    fig = px.line(
        data, 
        x='Año', 
        y='Crecimiento (%)',
        markers=True,
        line_shape='spline',
        title='Crecimiento del mercado de salud digital en Argentina'
    )
    
    fig.update_layout(
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(size=14)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Page Aspects Légaux avec effets
def legal_page():
    st.markdown("<div class='section-header'>Aspectos Legales y Organizativos</div>", unsafe_allow_html=True)
    
    legal_aspects = [
        {"title": "Habilitación Sanitaria", "icon": "📋", "desc": "Certificaciones requeridas para operar en el sector salud."},
        {"title": "Protección de Datos", "icon": "🔒", "desc": "Cumplimiento con la ley de protección de datos personales."},
        {"title": "Convenios con Obras Sociales", "icon": "🤝", "desc": "Regulaciones para acuerdos con aseguradoras."}
    ]
    
    cols = st.columns(3)
    for i, aspect in enumerate(legal_aspects):
        with cols[i]:
            st.markdown(f"""
            <div class='feature-card' style='animation: fadeIn {0.5 + i*0.3}s ease;'>
                <div style="font-size: 2em; margin-bottom: 10px;">{aspect['icon']}</div>
                <h3>{aspect['title']}</h3>
                <p>{aspect['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# Page Durabilité avec effets
def sustainability_page():
    st.markdown("<div class='section-header'>Responsabilidad Social y Ambiental</div>", unsafe_allow_html=True)
    
    sustainability_data = {
        "Transporte Ecológico": {"value": 75, "unit": "%", "icon": "🚲"},
        "Reducción de Residuos": {"value": 40, "unit": "%", "icon": "♻️"},
        "Energías Renovables": {"value": 60, "unit": "%", "icon": "☀️"}
    }
    
    cols = st.columns(3)
    for i, (name, data) in enumerate(sustainability_data.items()):
        with cols[i]:
            st.markdown(f"""
            <div class='feature-card' style='text-align: center; animation: slideIn {0.5 + i*0.3}s ease;'>
                <div style="font-size: 2.5em;">{data['icon']}</div>
                <h3>{name}</h3>
                <div style="font-size: 2em; font-weight: bold; color: #0083B8;">
                    {data['value']}{data['unit']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Page Contact avec effets
def contact_page():
    st.markdown("<div class='section-header'>Contacto</div>", unsafe_allow_html=True)
    
    with st.form(key="contact_form"):
        cols = st.columns(2)
        with cols[0]:
            st.text_input("Nombre completo", key="contact_name")
            st.text_input("Correo electrónico", key="contact_email")
        with cols[1]:
            st.selectbox("Tema", ["Consulta general", "Soporte técnico"], key="contact_topic")
            st.text_area("Mensaje", height=100, key="contact_message")
        
        if st.form_submit_button("Enviar mensaje", type="primary"):
            st.success("¡Gracias por contactarnos!")
            st.balloons()

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
