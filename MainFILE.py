import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import base64
import datetime

# =============================================
# CONFIGURATION INITIALE
# =============================================

st.set_page_config(
    page_title="MediPedido - Medicina a domicilio",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# FONCTIONS DE DESIGN
# =============================================

def setup_design():
    st.markdown("""
    <style>
    :root {
        --primary: #0083B8;
        --secondary: #00B4DB;
        --light-bg: #f8f9fa;
    }
    
    .stApp {
        background: var(--light-bg);
    }
    
    /* Cartes modernes */
    .card {
        border: none;
        border-radius: 12px;
        padding: 25px;
        background: white;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
        margin-bottom: 25px;
        height: 100%;
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.12);
    }
    
    /* Icônes de service */
    .service-icon {
        font-size: 2.8rem;
        margin-bottom: 20px;
        color: var(--primary);
        text-align: center;
    }
    
    /* Cartes docteurs */
    .doctor-card {
        text-align: center;
        padding: 25px;
        position: relative;
        overflow: hidden;
    }
    
    .doctor-img {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 auto 20px;
        border: 4px solid var(--primary);
        transition: all 0.3s;
    }
    
    .doctor-card:hover .doctor-img {
        transform: scale(1.05);
    }
    
    /* Boutons */
    .stButton>button {
        border: 2px solid var(--primary);
        background: var(--primary);
        color: white;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: white;
        color: var(--primary);
    }
    
    /* Animation d'entrée */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: fadeIn 0.8s ease-out forwards;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================
# COMPOSANTS REUTILISABLES
# =============================================

def doctor_card(name, specialty, experience, img_url, delay=0):
    return f"""
    <div class="card doctor-card animate-in" style="animation-delay: {delay}ms">
        <img src="{img_url}" class="doctor-img">
        <h3 style="margin: 0 0 5px 0; color: #00506E;">{name}</h3>
        <p style="color: var(--primary); font-weight: 600; margin: 0 0 10px 0;">{specialty}</p>
        <p style="color: #666; margin-bottom: 20px;">{experience} años de experiencia</p>
        <button style="
            background: var(--primary);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 30px;
            cursor: pointer;
            font-weight: 500;
            width: 100%;
            transition: all 0.3s;
        " onmouseover="this.style.background='white';this.style.color='var(--primary)';" 
        onmouseout="this.style.background='var(--primary)';this.style.color='white';">
            Pedir cita
        </button>
    </div>
    """

# =============================================
# PAGES
# =============================================

def home_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 50px;">
        <h1 style="color: #0083B8; font-size: 3em; margin-bottom: 20px;">Bienvenido a MediPedido</h1>
        <p style="font-size: 1.3em; color: #555;">La revolución en atención médica domiciliaria en Argentina</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estadísticas
    stats = [
        {"value": "12,500+", "label": "Pacientes atendidos", "icon": "👨‍👩‍👧‍👦"},
        {"value": "300+", "label": "Profesionales", "icon": "👨‍⚕️"},
        {"value": "24/7", "label": "Disponibilidad", "icon": "⏰"},
        {"value": "98%", "label": "Satisfacción", "icon": "⭐"}
    ]
    
    cols = st.columns(4)
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2.5em; margin-bottom: 10px;">{stat['icon']}</div>
                <h2 style="color: var(--primary); margin: 0;">{stat['value']}</h2>
                <p style="font-size: 1.1em; margin: 5px 0 0;">{stat['label']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Video promocional (placeholder)
    st.markdown("""
    <div style="margin: 50px 0; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <div style="background: #ddd; height: 400px; display: flex; align-items: center; justify-content: center;">
            <p style="font-size: 1.5em; color: #666;">[Video promocional aquí]</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def servicios_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #0083B8; font-size: 2.8em;">Nuestros Servicios Médicos</h1>
        <p style="font-size: 1.2em; color: #555;">Atención profesional cuando y donde la necesites</p>
    </div>
    """, unsafe_allow_html=True)
    
    servicios = [
        {
            "icon": "🏠",
            "title": "Consultas a Domicilio",
            "desc": "Médicos generales y especialistas que acuden a tu hogar u oficina.",
            "details": [
                "Exámenes físicos completos",
                "Diagnósticos precisos",
                "Recetas médicas electrónicas",
                "Atención preventiva"
            ]
        },
        {
            "icon": "💻",
            "title": "Telemedicina",
            "desc": "Consultas virtuales con especialistas desde cualquier lugar.",
            "details": [
                "Videollamadas HD seguras",
                "Segundas opiniones médicas",
                "Control continuo de tratamientos",
                "Resultados en línea"
            ]
        },
        {
            "icon": "🩺",
            "title": "Servicios Especializados",
            "desc": "Atención de especialidades médicas en tu domicilio.",
            "details": [
                "Pediatría y neonatología",
                "Cardiología avanzada",
                "Neurología y psiquiatría",
                "Geriatría y cuidados paliativos"
            ]
        }
    ]
    
    cols = st.columns(3)
    for i, servicio in enumerate(servicios):
        with cols[i]:
            st.markdown(f"""
            <div class="card animate-in" style="animation-delay: {i*200}ms">
                <div class="service-icon">{servicio['icon']}</div>
                <h2 style="color: #00506E; text-align: center; margin: 0 0 15px 0;">{servicio['title']}</h2>
                <p style="text-align: center; margin-bottom: 20px;">{servicio['desc']}</p>
                <ul style="padding-left: 20px;">
                    {''.join([f'<li style="margin-bottom: 8px;">{item}</li>' for item in servicio['details']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Proceso de atención
    st.markdown("""
    <div style="margin: 60px 0 30px 0;">
        <h2 style="color: #0083B8; text-align: center; margin-bottom: 30px;">¿Cómo funciona MediPedido?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    pasos = [
        {"icon": "📱", "title": "Solicita una cita", "desc": "Por app, web o llamada telefónica"},
        {"icon": "⏰", "title": "Confirma horario", "desc": "Recibe confirmación inmediata"},
        {"icon": "🚑", "title": "Médico en camino", "desc": "Profesional certificado se dirige a ti"},
        {"icon": "🏠", "title": "Atención personalizada", "desc": "Consulta completa en tu domicilio"}
    ]
    
    cols = st.columns(4)
    for i, paso in enumerate(pasos):
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="text-align: center; padding: 20px;">
                <div style="font-size: 2.5em; margin-bottom: 15px; color: var(--primary);">{paso['icon']}</div>
                <h3 style="margin: 0 0 10px 0;">{paso['title']}</h3>
                <p style="color: #666; margin: 0;">{paso['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def profesionales_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #0083B8; font-size: 2.8em;">Nuestro Equipo Médico</h1>
        <p style="font-size: 1.2em; color: #555;">Profesionales certificados y con amplia experiencia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Especialistas destacados
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h2 style="color: #00506E; border-bottom: 2px solid #0083B8; padding-bottom: 10px; display: inline-block;">
            Especialistas Destacados
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    doctores = [
        {
            "nombre": "Dra. Laura Méndez",
            "especialidad": "Pediatría",
            "exp": "12",
            "universidad": "UBA",
            "img": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80"
        },
        {
            "nombre": "Dr. Carlos Rodríguez",
            "especialidad": "Cardiología",
            "exp": "18",
            "universidad": "UNC",
            "img": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80"
        },
        {
            "nombre": "Dra. Ana García",
            "especialidad": "Geriatría",
            "exp": "15",
            "universidad": "UNLP",
            "img": "https://images.unsplash.com/photo-1594824476967-48c8b964273f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80"
        }
    ]
    
    cols = st.columns(3)
    for i, doctor in enumerate(doctores):
        with cols[i]:
            st.markdown(doctor_card(
                name=doctor['nombre'],
                specialty=doctor['especialidad'],
                experience=doctor['exp'],
                img_url=doctor['img'],
                delay=i*200
            ), unsafe_allow_html=True)
    
    # Todas las especialidades
    st.markdown("""
    <div style="margin: 60px 0 30px 0;">
        <h2 style="color: #00506E; border-bottom: 2px solid #0083B8; padding-bottom: 10px; display: inline-block;">
            Todas Nuestras Especialidades
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    especialidades = [
        {"nombre": "Medicina General", "icon": "🩺"},
        {"nombre": "Pediatría", "icon": "👶"},
        {"nombre": "Cardiología", "icon": "❤️"},
        {"nombre": "Neurología", "icon": "🧠"},
        {"nombre": "Dermatología", "icon": "🌟"},
        {"nombre": "Ginecología", "icon": "🌸"},
        {"nombre": "Traumatología", "icon": "🦴"},
        {"nombre": "Psiquiatría", "icon": "🧠"},
        {"nombre": "Nutrición", "icon": "🍎"}
    ]
    
    cols = st.columns(3)
    for i, esp in enumerate(especialidades):
        with cols[i%3]:
            st.markdown(f"""
            <div class="card" style="display: flex; align-items: center; padding: 15px;">
                <div style="font-size: 1.8em; margin-right: 15px; color: var(--primary);">{esp['icon']}</div>
                <h3 style="margin: 0; color: #00506E;">{esp['nombre']}</h3>
            </div>
            """, unsafe_allow_html=True)

def blog_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #0083B8; font-size: 2.8em;">Blog de Salud MediPedido</h1>
        <p style="font-size: 1.2em; color: #555;">Consejos médicos y novedades para tu bienestar</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de búsqueda
    with st.expander("🔍 Buscar artículos", expanded=False):
        col1, col2 = st.columns([3,1])
        with col1:
            search_query = st.text_input("Buscar por palabras clave", key="blog_search")
        with col2:
            category = st.selectbox("Categoría", ["Todas", "Prevención", "Tratamientos", "Salud Mental", "Nutrición"], key="blog_category")
    
    # Artículos del blog
    articulos = [
        {
            "titulo": "Cómo controlar la presión arterial en casa",
            "autor": "Dr. Javier Mendoza",
            "fecha": "15 Mayo 2023",
            "categoria": "Prevención",
            "resumen": "Aprende técnicas efectivas para monitorear tu presión arterial y prevenir complicaciones cardiovasculares con recomendaciones de expertos.",
            "imagen": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "tags": ["hipertensión", "salud cardiovascular", "prevención"],
            "tiempo_lectura": "5 min"
        },
        {
            "titulo": "Alimentación saludable para niños en crecimiento",
            "autor": "Dra. Laura Fernández",
            "fecha": "2 Junio 2023",
            "categoria": "Nutrición",
            "resumen": "Guía completa de nutrición infantil con recomendaciones por edades y cómo abordar necesidades especiales en cada etapa del desarrollo.",
            "imagen": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "tags": ["nutrición infantil", "crecimiento", "alimentación saludable"],
            "tiempo_lectura": "8 min"
        },
        {
            "titulo": "Manejo del estrés en tiempos modernos",
            "autor": "Dr. Marcos Pérez",
            "fecha": "10 Abril 2023",
            "categoria": "Salud Mental",
            "resumen": "Estrategias validadas por psicólogos para gestionar el estrés laboral y personal en el acelerado mundo actual.",
            "imagen": "https://images.unsplash.com/photo-1491841550275-ad7854e35ca6?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "tags": ["estrés", "salud mental", "bienestar"],
            "tiempo_lectura": "6 min"
        }
    ]
    
    for i, articulo in enumerate(articulos):
        # Filtrado
        if search_query and search_query.lower() not in articulo["titulo"].lower() and search_query.lower() not in articulo["resumen"].lower():
            continue
        if category != "Todas" and category != articulo["categoria"]:
            continue
        
        st.markdown(f"""
        <div class="card animate-in" style="animation-delay: {i*150}ms">
            <div style="display: flex; gap: 30px;">
                <div style="flex: 1;">
                    <img src="{articulo['imagen']}" style="
                        width: 100%;
                        height: 200px;
                        object-fit: cover;
                        border-radius: 10px;
                    ">
                </div>
                <div style="flex: 2;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: var(--primary); font-weight: 500;">{articulo['categoria']}</span>
                        <span style="color: #666;">{articulo['fecha']} • {articulo['tiempo_lectura']}</span>
                    </div>
                    <h2 style="margin: 0 0 10px 0; color: #00506E;">{articulo['titulo']}</h2>
                    <p style="color: #666; margin-bottom: 15px;">{articulo['resumen']}</p>
                    <div style="margin-bottom: 15px;">
                        {"".join([f'<span style="background: #e6f7ff; color: #0083B8; padding: 3px 10px; border-radius: 20px; font-size: 0.8em; margin-right: 8px;">{tag}</span>' for tag in articulo["tags"]])}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #666;">Por {articulo['autor']}</span>
                        <button style="
                            background: var(--primary);
                            color: white;
                            border: none;
                            padding: 8px 20px;
                            border-radius: 20px;
                            cursor: pointer;
                        ">Leer artículo</button>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def contacto_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #0083B8; font-size: 2.8em;">Contacta con MediPedido</h1>
        <p style="font-size: 1.2em; color: #555;">Estamos aquí para ayudarte</p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    
    with cols[0]:
        st.markdown("""
        <div class="card" style="padding: 30px; height: 100%;">
            <h2 style="color: #00506E; margin-top: 0;">Información de Contacto</h2>
            
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="font-size: 1.5em; margin-right: 15px; color: var(--primary);">📌</div>
                <div>
                    <h4 style="margin: 0 0 5px 0;">Dirección</h4>
                    <p style="margin: 0; color: #666;">Av. Corrientes 1234, Buenos Aires</p>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="font-size: 1.5em; margin-right: 15px; color: var(--primary);">📞</div>
                <div>
                    <h4 style="margin: 0 0 5px 0;">Teléfono</h4>
                    <p style="margin: 0; color: #666;">+54 11 1234-5678</p>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="font-size: 1.5em; margin-right: 15px; color: var(--primary);">✉️</div>
                <div>
                    <h4 style="margin: 0 0 5px 0;">Email</h4>
                    <p style="margin: 0; color: #666;">info@medipedido.com.ar</p>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <h4 style="margin: 0 0 15px 0; color: #00506E;">Horario de Atención</h4>
                <p style="margin: 5px 0; color: #666;"><strong>Servicio médico:</strong> 24/7</p>
                <p style="margin: 5px 0; color: #666;"><strong>Oficinas administrativas:</strong> Lunes a Viernes de 9:00 a 18:00</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        with st.form(key="contact_form"):
            st.markdown("""
            <div class="card" style="padding: 30px;">
                <h2 style="color: #00506E; margin-top: 0;">Envíanos un mensaje</h2>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre completo*", key="contact_name")
            with col2:
                email = st.text_input("Email*", key="contact_email")
            
            telefono = st.text_input("Teléfono", key="contact_phone")
            asunto = st.selectbox("Asunto*", 
                                ["Consulta general", "Soporte técnico", "Trabaja con nosotros", "Prensa", "Otro"],
                                key="contact_subject")
            mensaje = st.text_area("Mensaje*", height=150, key="contact_message")
            
            st.markdown("<small>* Campos obligatorios</small>", unsafe_allow_html=True)
            
            if st.form_submit_button("Enviar mensaje", type="primary"):
                st.success("¡Gracias por tu mensaje! Te responderemos en breve.")
                st.balloons()
            
            st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# APPLICATION PRINCIPALE
# =============================================

def main():
    setup_design()
    
    # Barre de navigation
    selected = option_menu(
        menu_title=None,
        options=["Inicio", "Servicios", "Profesionales", "Blog", "Contacto"],
        icons=["house", "clipboard-pulse", "people", "journal-text", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "white",
                "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
                "border-radius": "10px",
                "margin-bottom": "30px"
            },
            "icon": {"color": "#0083B8", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "padding": "12px 20px",
                "--hover-color": "#e6f7ff"
            },
            "nav-link-selected": {
                "background-color": "#0083B8",
                "font-weight": "normal"
            },
        }
    )
    
    # Affichage de la page sélectionnée
    if selected == "Inicio":
        home_page()
    elif selected == "Servicios":
        servicios_page()
    elif selected == "Profesionales":
        profesionales_page()
    elif selected == "Blog":
        blog_page()
    elif selected == "Contacto":
        contacto_page()

if __name__ == "__main__":
    main()
