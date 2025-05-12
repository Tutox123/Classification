import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configuration de la page
st.set_page_config(
    page_title="MediPedido - Medicina a domicilio",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
def load_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 3em;
            font-weight: bold;
            color: #0083B8;
            text-align: center;
            margin-bottom: 30px;
        }
        .section-header {
            font-size: 2em;
            color: #0083B8;
            border-bottom: 2px solid #0083B8;
            padding-bottom: 10px;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .sub-header {
            font-size: 1.5em;
            color: #00506E;
            margin-top: 15px;
            margin-bottom: 15px;
        }
        .info-box {
            background-color: #e6f7ff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .feature-card {
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }
        .highlight {
            color: #0083B8;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

# En-tête
def show_header():
    st.markdown("<div class='main-header'>MediPedido</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 1.5em;'>La medicina que llega a tu puerta</div>", unsafe_allow_html=True)

# Navigation
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
            "container": {"padding": "0!important", "background-color": "#f0f0f0"},
            "icon": {"color": "#0083B8", "font-size": "14px"}, 
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#e6f7ff"},
            "nav-link-selected": {"background-color": "#0083B8"},
        }
    )

# Page d'accueil
def home_page():
    st.markdown("<div class='section-header'>Bienvenido a MediPedido</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        st.markdown("""
        <div class='info-box'>
            <div class='sub-header'>Quiénes Somos</div>
            <p>MediPedido es una innovadora aplicación de medicina a domicilio que conecta a profesionales de la salud con pacientes que necesitan atención médica en la comodidad de su hogar.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>💉 Consultas médicas</h3>
            <p>Atención profesional en la comodidad de tu hogar</p>
        </div>
        """, unsafe_allow_html=True)

# Page Services
def services_page():
    st.markdown("<div class='section-header'>Nuestros Servicios</div>", unsafe_allow_html=True)
    
    # Solution optimisée pour les tabs
    tab_names = ["Consultas a Domicilio", "Telemedicina", "Servicios Especializados", "Modelo de Negocio"]
    selected_tab = st.radio(
        "Seleccione un servicio",
        tab_names,
        horizontal=True,
        label_visibility="collapsed",
        key="services_tabs_radio"
    )
    
    if selected_tab == tab_names[0]:
        st.markdown("""
        <div class='sub-header'>Consultas Médicas a Domicilio</div>
        <p>Nuestros profesionales de la salud acuden directamente a tu hogar.</p>
        """, unsafe_allow_html=True)
        
    elif selected_tab == tab_names[1]:
        st.markdown("""
        <div class='sub-header'>Servicios de Telemedicina</div>
        <p>Conectamos a pacientes con médicos mediante videoconsultas.</p>
        """, unsafe_allow_html=True)
        
    elif selected_tab == tab_names[2]:
        st.markdown("""
        <div class='sub-header'>Servicios Médicos Especializados</div>
        """, unsafe_allow_html=True)
        
    elif selected_tab == tab_names[3]:
        st.markdown("""
        <div class='sub-header'>Modelo de Negocio</div>
        """, unsafe_allow_html=True)

# Page Marché
def market_page():
    st.markdown("<div class='section-header'>Análisis del Mercado Argentino</div>", unsafe_allow_html=True)
    
    datos = pd.DataFrame({
        'Año': [2020, 2021, 2022, 2023, 2024],
        'Penetración (%)': [55, 58, 62, 67, 70]
    })
    
    fig = px.line(datos, x='Año', y='Penetración (%)', markers=True)
    st.plotly_chart(fig, use_container_width=True, key="market_penetration_chart")

# Page Aspects Légaux
def legal_page():
    st.markdown("<div class='section-header'>Aspectos Legales y Organizativos</div>", unsafe_allow_html=True)
    
    cols = st.columns(2, gap="large")
    
    with cols[0]:
        st.markdown("""
        <div class='feature-card'>
            <h3>📋 Habilitación Sanitaria</h3>
            <p>Registro como prestadora de salud con profesionales habilitados.</p>
        </div>
        """, unsafe_allow_html=True)

# Page Durabilité
def sustainability_page():
    st.markdown("<div class='section-header'>Responsabilidad Social y Ambiental</div>", unsafe_allow_html=True)
    
    # Solution alternative aux tabs
    sustainability_options = ["Movilidad Sostenible", "Gestión de Residuos", "Compromiso Social", "Transparencia"]
    selected_option = st.radio(
        "Seleccione un tema",
        sustainability_options,
        horizontal=True,
        label_visibility="collapsed",
        key="sustainability_radio"
    )
    
    if selected_option == sustainability_options[0]:
        st.markdown("""
        <div class='sub-header'>Transporte Sostenible</div>
        <p>Incentivamos medios de transporte sostenibles.</p>
        """, unsafe_allow_html=True)

# Page Contact
def contact_page():
    st.markdown("<div class='section-header'>Contacto</div>", unsafe_allow_html=True)
    
    with st.form(key="contact_form"):
        st.text_input("Nombre completo", key="contact_name")
        st.text_input("Correo electrónico", key="contact_email")
        st.selectbox("Tema", ["Consulta general", "Soporte técnico"], key="contact_topic")
        st.text_area("Mensaje", key="contact_message")
        
        if st.form_submit_button("Enviar mensaje", type="primary"):
            st.success("¡Gracias por contactarnos!")

# Application principale
def main():
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
