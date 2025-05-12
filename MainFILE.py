import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
from streamlit_option_menu import option_menu

# Configuración de la página
st.set_page_config(
    page_title="MediPedido - Medicina a domicilio",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
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
    .icon-text {
        display: flex;
        align-items: center;
    }
    .highlight {
        color: #0083B8;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Función para crear el menú de navegación
def create_nav_menu():
    selected = option_menu(
        menu_title=None,
        options=["Inicio", "Servicios", "Mercado", "Aspectos Legales", "Sostenibilidad", "Contacto"],
        icons=["house", "clipboard-pulse", "graph-up", "shield-check", "tree", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        key="main_nav_menu",
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f0f0"},
            "icon": {"color": "#0083B8", "font-size": "14px"}, 
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#e6f7ff"},
            "nav-link-selected": {"background-color": "#0083B8"},
        }
    )
    return selected

# Logo y encabezado
def display_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='main-header'>MediPedido</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 1.5em;'>La medicina que llega a tu puerta</div>", unsafe_allow_html=True)

# Página de inicio
def home_page():
    st.markdown("<div class='section-header'>Bienvenido a MediPedido</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        st.markdown("""
        <div class='info-box'>
            <div class='sub-header'>Quiénes Somos</div>
            <p>MediPedido es una innovadora aplicación de medicina a domicilio que conecta a profesionales de la salud con pacientes que necesitan atención médica en la comodidad de su hogar.</p>
            <p>Fundada por Ilias y Mathieu, nuestra empresa busca revolucionar el acceso a servicios médicos en Argentina, aprovechando la tecnología para ofrecer atención de calidad cuando y donde se necesite.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='sub-header'>Nuestra Misión</div>
        <p>Facilitar el acceso a servicios médicos de calidad a través de una plataforma digital innovadora, mejorando la experiencia de atención médica y contribuyendo al bienestar de la sociedad argentina.</p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>💉 Consultas médicas</h3>
            <p>Atención profesional en la comodidad de tu hogar</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>⏱️ Disponibilidad 24/7</h3>
            <p>Servicio médico cuando lo necesites</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>💊 Recetas digitales</h3>
            <p>Prescripciones médicas electrónicas seguras</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>🏥 Cobertura con Obras Sociales</h3>
            <p>Alianzas estratégicas con el sistema de salud</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>¿Por qué elegimos Argentina?</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class='info-box'>
            <ul>
                <li><span class='highlight'>Talento tecnológico</span>: Argentina cuenta con desarrolladores altamente calificados y una fuerte cultura de innovación</li>
                <li><span class='highlight'>Costos competitivos</span>: Desarrollo más económico manteniendo alta calidad</li>
                <li><span class='highlight'>Sistema de salud desarrollado</span>: Infraestructura sanitaria adecuada para implementar servicios de salud digital</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-box'>
            <ul>
                <li><span class='highlight'>Marco regulatorio favorable</span>: Regulaciones que facilitan la operación de empresas de tecnología sanitaria</li>
                <li><span class='highlight'>Zonas horarias compatibles</span>: Facilita la comunicación con equipos en Europa</li>
                <li><span class='highlight'>Mercado en crecimiento</span>: Demanda creciente de servicios de salud privados y soluciones digitales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Página de servicios
def services_page():
    st.markdown("<div class='section-header'>Nuestros Servicios</div>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Consultas a Domicilio", "Telemedicina", "Servicios Especializados", "Modelo de Negocio"], key="services_tabs")
    
    with tabs[0]:
        col1, col2 = st.columns([2, 3], gap="large")
        
        with col1:
            st.markdown("""
            <div class='sub-header'>Consultas Médicas a Domicilio</div>
            <p>Nuestros profesionales de la salud acuden directamente a tu hogar para brindarte atención médica de calidad.</p>
            <ul>
                <li>Médicos clínicos y especialistas</li>
                <li>Servicios de enfermería</li>
                <li>Fisioterapia a domicilio</li>
                <li>Atención para adultos mayores</li>
            </ul>
            """, unsafe_allow_html=True)
        
        with col2:
            st.image("https://via.placeholder.com/600x300?text=Consultas+Médicas+a+Domicilio", 
                   caption="Médicos profesionales a tu servicio",
                   use_column_width=True)
    
    with tabs[1]:
        col1, col2 = st.columns([3, 2], gap="large")
        
        with col1:
            st.markdown("""
            <div class='sub-header'>Servicios de Telemedicina</div>
            <p>Conectamos a pacientes con médicos mediante videoconsultas para casos que no requieren presencia física.</p>
            <ul>
                <li>Consultas médicas por video</li>
                <li>Seguimiento de tratamientos</li>
                <li>Segunda opinión médica</li>
                <li>Renovación de recetas</li>
            </ul>
            """, unsafe_allow_html=True)
        
        with col2:
            st.image("https://via.placeholder.com/500x300?text=Telemedicina", 
                   caption="Consultas médicas virtuales",
                   use_column_width=True)
    
    with tabs[2]:
        st.markdown("""
        <div class='sub-header'>Servicios Médicos Especializados</div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3, gap="large")
        
        with cols[0]:
            st.markdown("""
            <div class='feature-card'>
                <h3>👶 Pediatría</h3>
                <p>Atención especializada para bebés y niños</p>
            </div>
            <div class='feature-card'>
                <h3>🧠 Psicología</h3>
                <p>Apoyo para la salud mental desde casa</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown("""
            <div class='feature-card'>
                <h3>👵 Geriatría</h3>
                <p>Cuidado especializado para adultos mayores</p>
            </div>
            <div class='feature-card'>
                <h3>💉 Laboratorio</h3>
                <p>Toma de muestras a domicilio</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown("""
            <div class='feature-card'>
                <h3>💊 Nutrición</h3>
                <p>Asesoramiento nutricional personalizado</p>
            </div>
            <div class='feature-card'>
                <h3>❤️ Cardiología</h3>
                <p>Monitoreo y consultas especializadas</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("<div class='sub-header'>Modelo de Negocio</div>", unsafe_allow_html=True)
        
        cols = st.columns(2, gap="large")
        
        with cols[0]:
            st.markdown("""
            <div class='info-box'>
                <h3>Alianzas con Obras Sociales</h3>
                <p>Establecemos convenios con las principales Obras Sociales en Argentina para que:</p>
                <ul>
                    <li>Los servicios sean cubiertos total o parcialmente por las Obras Sociales</li>
                    <li>Los afiliados puedan acceder a nuestros servicios sin costos adicionales</li>
                    <li>Se facilite el acceso a la atención médica, especialmente para personas con movilidad reducida</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown("""
            <div class='info-box'>
                <h3>Beneficios clave</h3>
                <ul>
                    <li>Mayor base de usuarios potenciales</li>
                    <li>Confianza y legitimidad al asociarnos con instituciones reconocidas</li>
                    <li>Expansión territorial a través de obras sociales con presencia nacional</li>
                    <li>Modelo financiero sostenible con ingresos estables</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Página de mercado
def market_page():
    st.markdown("<div class='section-header'>Análisis del Mercado Argentino</div>", unsafe_allow_html=True)
    
    # Datos para los gráficos
    datos_penetracion = pd.DataFrame({
        'Año': [2020, 2021, 2022, 2023, 2024],
        'Penetración (%)': [55, 58, 62, 67, 70]
    })
    
    datos_demanda = pd.DataFrame({
        'Servicio': ['Consultas médicas', 'Enfermería', 'Fisioterapia', 'Laboratorio', 'Telemedicina'],
        'Demanda (%)': [40, 25, 15, 12, 8]
    })
    
    cols = st.columns([3, 2], gap="large")
    
    with cols[0]:
        st.markdown("""
        <div class='info-box'>
            <div class='sub-header'>Tendencias del Mercado</div>
            <ul>
                <li><span class='highlight'>Demanda creciente</span> de servicios de salud privados, impulsada por el aumento de ingresos y la preferencia por servicios de mayor calidad</li>
                <li><span class='highlight'>Reformas gubernamentales</span> para mejorar la eficiencia del sistema sanitario, aunque con aumento de costos</li>
                <li><span class='highlight'>Expansión del mercado mHealth</span> (aplicaciones de salud móvil) debido a la mayor penetración de smartphones</li>
                <li><span class='highlight'>Mercado competitivo</span> con actores públicos y privados buscando innovar en servicios de salud</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("<div class='sub-header'>Penetración de Smartphones en Argentina</div>", unsafe_allow_html=True)
        fig = px.line(datos_penetracion, x='Año', y='Penetración (%)', markers=True)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True, key="penetracion_chart")
    
    st.markdown("<div class='sub-header'>Oportunidades y Desafíos</div>", unsafe_allow_html=True)
    
    cols = st.columns(3, gap="large")
    
    with cols[0]:
        st.markdown("""
        <div class='feature-card'>
            <h3>🚀 Oportunidades</h3>
            <ul>
                <li>Población con alta adopción tecnológica</li>
                <li>Sistema de obras sociales bien establecido</li>
                <li>Demanda de atención médica sin desplazamientos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class='feature-card'>
            <h3>⚠️ Desafíos</h3>
            <ul>
                <li>Regulaciones cambiantes en telemedicina</li>
                <li>Inestabilidad económica del país</li>
                <li>Resistencia al cambio en el sector sanitario</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div class='feature-card'>
            <h3>🎯 Estrategias</h3>
            <ul>
                <li>Alianzas con obras sociales clave</li>
                <li>Marketing digital focalizado</li>
                <li>Educación sobre beneficios de la telemedicina</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='sub-header'>Demanda por Tipo de Servicio</div>", unsafe_allow_html=True)
    fig = px.pie(datos_demanda, values='Demanda (%)', names='Servicio', hole=0.4)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True, key="demanda_chart")

# Página de aspectos legales
def legal_page():
    st.markdown("<div class='section-header'>Aspectos Legales y Organizativos</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <p>Para operar legalmente en Argentina, MediPedido debe cumplir con diversos requisitos regulatorios en el ámbito de la salud y la tecnología.</p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2, gap="large")
    
    with cols[0]:
        st.markdown("""
        <div class='feature-card'>
            <h3>📋 Habilitación Sanitaria</h3>
            <p>La empresa debe estar registrada como prestadora de salud y trabajar exclusivamente con profesionales médicos habilitados por las autoridades nacionales y provinciales.</p>
        </div>
        
        <div class='feature-card'>
            <h3>🏢 Constitución Legal</h3>
            <p>Es necesario crear una sociedad formal (SRL o SA) e inscribirse ante la AFIP para operar legalmente en el país.</p>
        </div>
        
        <div class='feature-card'>
            <h3>🔒 Protección de Datos Personales</h3>
            <p>La aplicación debe cumplir con la Ley 25.326, garantizando la privacidad y seguridad de los datos médicos de los pacientes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class='feature-card'>
            <h3>📱 Regulación de Telemedicina</h3>
            <p>Las consultas virtuales deben seguir las normativas éticas y técnicas vigentes, incluyendo el uso de recetas electrónicas y firmas digitales válidas.</p>
        </div>
        
        <div class='feature-card'>
            <h3>🤝 Convenios con Obras Sociales</h3>
            <p>Para ser prestador oficial, hay que firmar acuerdos regulados por la Superintendencia de Servicios de Salud y cumplir con requisitos administrativos específicos.</p>
        </div>
        
        <div class='feature-card'>
            <h3>💼 Responsabilidad Profesional</h3>
            <p>Los médicos y profesionales de la salud deben contar con seguros de responsabilidad civil y mala praxis según lo exigido por la legislación argentina.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='sub-header'>Cronograma de Implementación Legal</div>", unsafe_allow_html=True)
    
    timeline_data = {
        'Fase': ['Constitución legal', 'Registro sanitario', 'Protección de datos', 'Convenios iniciales', 'Expansión nacional'],
        'Mes de inicio': [1, 2, 2, 4, 8],
        'Duración (meses)': [2, 3, 2, 4, 6]
    }
    df_timeline = pd.DataFrame(timeline_data)
    
    fig = px.timeline(df_timeline, x_start='Mes de inicio', 
                     x_end=df_timeline['Mes de inicio'] + df_timeline['Duración (meses)'], 
                     y='Fase', color='Fase')
    fig.update_layout(xaxis_title='Mes del proyecto', height=300)
    st.plotly_chart(fig, use_container_width=True, key="timeline_chart")

# Página de sostenibilidad
def sustainability_page():
    st.markdown("<div class='section-header'>Propuesta de Responsabilidad Social y Ambiental</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <p>En MediPedido creemos que la salud de las personas está intrínsecamente ligada a la salud del planeta. Por eso, implementamos diversas iniciativas para minimizar nuestro impacto ambiental y maximizar nuestro impacto social positivo.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["Movilidad Sostenible", "Gestión de Residuos", "Compromiso Social", "Transparencia"], key="sustainability_tabs")
    
    with tabs[0]:
        cols = st.columns([2, 2], gap="large")
        
        with cols[0]:
            st.markdown("""
            <div class='sub-header'>Transporte Sostenible</div>
            <p>Incentivamos a nuestros profesionales médicos a utilizar medios de transporte sostenibles para reducir la huella de carbono de nuestros servicios a domicilio:</p>
            <ul>
                <li>Bonificaciones para médicos que utilizan vehículos eléctricos</li>
                <li>Colaboración con servicios de transporte público</li>
                <li>Programa de bicicletas para desplazamientos cortos</li>
                <li>Optimización de rutas para reducir emisiones</li>
            </ul>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            transportes = {
                'Medio': ['Automóvil eléctrico', 'Transporte público', 'Bicicleta', 'A pie', 'Automóvil tradicional'],
                'Porcentaje': [30, 25, 20, 15, 10]
            }
            df_transportes = pd.DataFrame(transportes)
            
            fig = px.bar(df_transportes, x='Medio', y='Porcentaje', color='Porcentaje',
                        color_continuous_scale='Viridis')
            fig.update_layout(height=300, title='Distribución de medios de transporte (objetivo)')
            st.plotly_chart(fig, use_container_width=True, key="transport_chart")
    
    with tabs[1]:
        st.markdown("""
        <div class='sub-header'>Gestión Responsable de Residuos Médicos</div>
        <p>Implementamos prácticas sostenibles para el manejo de residuos generados durante la atención médica a domicilio:</p>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3, gap="large")
        
        with cols[0]:
            st.markdown("""
            <div class='feature-card'>
                <h3>♻️ Separación y Reciclaje</h3>
                <p>Capacitamos a nuestros profesionales para la correcta separación de residuos reciclables, orgánicos y médicos.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown("""
            <div class='feature-card'>
                <h3>🔬 Gestión de Residuos Peligrosos</h3>
                <p>Colaboramos con hospitales y centros especializados para el tratamiento adecuado de residuos patogénicos.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown("""
            <div class='feature-card'>
                <h3>📊 Monitoreo y Reducción</h3>
                <p>Medimos y trabajamos constantemente para reducir la cantidad de residuos generados por consulta médica.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("""
        <div class='sub-header'>Compromiso con la Comunidad</div>
        <p>Nuestro compromiso social se materializa a través de diversas iniciativas:</p>
        """, unsafe_allow_html=True)
        
        cols = st.columns(2, gap="large")
        
        with cols[0]:
            st.markdown("""
            <div class='feature-card'>
                <h3>🏥 Atención Gratuita</h3>
                <p>Programa mensual de atención médica gratuita en zonas vulnerables de Argentina.</p>
            </div>
            
            <div class='feature-card'>
                <h3>📚 Educación en Salud</h3>
                <p>Campañas educativas sobre prevención y hábitos saludables en escuelas y comunidades.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown("""
            <div class='feature-card'>
                <h3>💉 Campañas de Vacunación</h3>
                <p>Apoyo a campañas nacionales de vacunación facilitando recursos y personal médico.</p>
            </div>
            
            <div class='feature-card'>
                <h3>👵 Atención a Adultos Mayores</h3>
                <p>Programa especial para facilitar el acceso a la salud a adultos mayores con dificultades de movilidad.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("""
        <div class='sub-header'>Transparencia y Rendición de Cuentas</div>
        <p>Mantenemos una política de transparencia en todas nuestras operaciones:</p>
        <ul>
            <li>Publicación trimestral de informes de impacto ambiental y social</li>
            <li>Certificación por entidades independientes de nuestras prácticas sostenibles</li>
            <li>Comunicación clara con pacientes y profesionales sobre nuestras políticas</li>
            <li>Programa de mejora continua basado en feedback de la comunidad</li>
        </ul>
        
        <div class='info-box'>
            <p>Nuestra meta es convertirnos en la primera aplicación de salud a domicilio en Argentina con certificación de carbono neutro para 2026.</p>
        </div>
        """, unsafe_allow_html=True)

# Página de contacto
def contact_page():
    st.markdown("<div class='section-header'>Contacto</div>", unsafe_allow_html=True)
    
    cols = st.columns([2, 3], gap="large")
    
    with cols[0]:
        st.markdown("""
        <div class='info-box'>
            <div class='sub-header'>Información de Contacto</div>
            <p><strong>Dirección:</strong> Av. Corrientes 1234, Buenos Aires, Argentina</p>
            <p><strong>Teléfono:</strong> +54 11 1234-5678</p>
            <p><strong>Email:</strong> info@medipedido.com.ar</p>
            <p><strong>Redes sociales:</strong> @MediPedido</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>Horario de Atención</h3>
            <p>Soporte técnico: 24/7</p>
            <p>Oficinas: Lunes a Viernes de 9:00 a 18:00</p>
            <p>Servicio médico: 24/7</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("<div class='sub-header'>Envíanos un mensaje</div>", unsafe_allow_html=True)
        
        with st.form(key="contact_form"):
            nombre = st.text_input("Nombre completo", key="contact_nombre")
            email = st.text_input("Correo electrónico", key="contact_email")
            tema = st.selectbox("Tema", 
                              ["Consulta general", "Soporte técnico", "Trabaja con nosotros", "Alianzas comerciales", "Otro"],
                              key="contact_tema")
            mensaje = st.text_area("Mensaje", height=150, key="contact_mensaje")
            
            enviar = st.form_submit_button("Enviar mensaje", type="primary")
            
            if enviar:
                st.success("¡Gracias por contactarnos! Te responderemos a la brevedad.")

# Función principal
def main():
    display_header()
    selected = create_nav_menu()
    
    if selected == "Inicio":
        home_page()
    elif selected == "Servicios":
        services_page()
    elif selected == "Mercado":
        market_page()
    elif selected == "Aspectos Legales":
        legal_page()
    elif selected == "Sostenibilidad":
        sustainability_page()
    elif selected == "Contacto":
        contact_page()

if __name__ == "__main__":
    main()
