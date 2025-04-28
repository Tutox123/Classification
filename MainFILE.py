import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, timedelta
import numpy as np

# ---------------------------
# Configuration de la page
# ---------------------------
st.set_page_config(
    page_title="Advanced Sales Analytics Dashboard",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Fonctions utilitaires
# ---------------------------
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, sep=';', header=0, decimal=',', encoding='utf-8')
        df.columns = df.columns.str.strip()
        
        # Vérification des colonnes requises
        required_columns = ['Date', 'Product type', 'Product line', 'Quantity', 
                          'Sale price', 'Purchase cost', 'Ordering method', 'Country of sale']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Colonnes manquantes : {', '.join(missing_cols)}")
            st.stop()

        # Conversion et calculs - Utilisation de dayfirst=True pour gérer le format européen (jour/mois/année)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Week'] = df['Date'].dt.isocalendar().week
        df['Day'] = df['Date'].dt.day_name()
        
        # Calculs financiers
        df['Total Sales'] = df['Quantity'] * df['Sale price']
        df['Total Cost'] = df['Quantity'] * df['Purchase cost']
        df['Profit'] = df['Total Sales'] - df['Total Cost']
        df['Margin %'] = (df['Profit'] / df['Total Sales']) * 100
        df['ROI'] = (df['Profit'] / df['Total Cost']) * 100
        
        # Segmentation clients/produits
        df['Sales Quartile'] = pd.qcut(df['Total Sales'], q=4, labels=['Low', 'Medium', 'High', 'Very High'])
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur de chargement : {str(e)}")
        st.stop()

def display_kpi(title, value, delta=None, delta_type=None):
    st.metric(
        label=title,
        value=value,
        delta=delta,
        delta_color=delta_type if delta_type else "normal"
    )

# ---------------------------
# Interface utilisateur
# ---------------------------
st.sidebar.title("🔍 Navigation & Configuration")
uploaded_file = st.sidebar.file_uploader("📤 Importer des données (CSV)", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    
    with st.sidebar.expander("⏱ Filtre temporel", expanded=True):
        date_range = st.date_input(
            "Période",
            value=[df['Date'].min(), df['Date'].max()],
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
        
        time_granularity = st.selectbox(
            "Granularité temporelle",
            ["Journalier", "Hebdomadaire", "Mensuel", "Trimestriel", "Annuel"]
        )
    
    with st.sidebar.expander("🌍 Filtres géographiques"):
        countries = st.multiselect(
            "Pays",
            options=df['Country of sale'].unique(),
            default=df['Country of sale'].unique()
        )
    
    with st.sidebar.expander("📦 Filtres produits"):
        product_types = st.multiselect(
            "Type de produit",
            options=df['Product type'].unique(),
            default=df['Product type'].unique()
        )
        
        product_lines = st.multiselect(
            "Ligne de produit",
            options=df['Product line'].unique(),
            default=df['Product line'].unique()
        )
    
    with st.sidebar.expander("💰 Filtres financiers"):
        margin_range = st.slider(
            "Marge (%)",
            min_value=float(df['Margin %'].min()),
            max_value=float(df['Margin %'].max()),
            value=(float(df['Margin %'].min()), float(df['Margin %'].max()))
        )
    
    # Application des filtres
    filtered_df = df[
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1])) &
        (df['Country of sale'].isin(countries)) &
        (df['Product type'].isin(product_types)) &
        (df['Product line'].isin(product_lines)) &
        (df['Margin %'] >= margin_range[0]) &
        (df['Margin %'] <= margin_range[1])
    ]
    
    # ---------------------------
    # Tableau de bord principal
    # ---------------------------
    st.title("📈 Tableau de bord analytique avancé")
    
    # KPIs principaux
    st.subheader("Indicateurs clés de performance")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        display_kpi("💰 CA Total", f"${filtered_df['Total Sales'].sum():,.0f}")
    with col2:
        display_kpi("📦 Quantité Totale", f"{filtered_df['Quantity'].sum():,}")
    with col3:
        display_kpi("📈 Marge Moyenne", f"{filtered_df['Margin %'].mean():.1f}%")
    with col4:
        display_kpi("🔄 ROI Moyen", f"{filtered_df['ROI'].mean():.1f}%")
    
    # Tendances temporelles
    st.subheader("Analyse temporelle")
    
    # Gestion correcte des regroupements temporels
    if time_granularity == "Journalier":
        time_analysis = filtered_df.groupby('Date').agg({
            'Total Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        x_axis = 'Date'
    elif time_granularity == "Hebdomadaire":
        filtered_df['Year_Week'] = filtered_df['Date'].dt.strftime('%Y-%U')
        time_analysis = filtered_df.groupby('Year_Week').agg({
            'Total Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        x_axis = 'Year_Week'
    elif time_granularity == "Mensuel":
        filtered_df['Year_Month'] = filtered_df['Date'].dt.strftime('%Y-%m')
        time_analysis = filtered_df.groupby('Year_Month').agg({
            'Total Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        x_axis = 'Year_Month'
    elif time_granularity == "Trimestriel":
        filtered_df['Quarter'] = filtered_df['Date'].dt.to_period('Q').astype(str)
        time_analysis = filtered_df.groupby('Quarter').agg({
            'Total Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        x_axis = 'Quarter'
    else:  # Annuel
        time_analysis = filtered_df.groupby('Year').agg({
            'Total Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        x_axis = 'Year'
    
    fig1 = px.area(
        time_analysis,
        x=x_axis,
        y='Total Sales',
        title=f"Évolution du CA ({time_granularity.lower()})",
        template="plotly_dark"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Analyse géographique
    st.subheader("Performance géographique")
    geo_analysis = filtered_df.groupby('Country of sale').agg({
        'Total Sales': 'sum',
        'Profit': 'sum',
        'Margin %': 'mean'
    }).sort_values('Total Sales', ascending=False).reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig2 = px.bar(
            geo_analysis.head(10),
            x='Country of sale',
            y='Total Sales',
            title="Top 10 Pays par CA",
            color='Margin %',
            template="plotly_dark"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        try:
            fig3 = px.choropleth(
                geo_analysis,
                locations='Country of sale',
                locationmode='country names',
                color='Total Sales',
                title="CA par Pays",
                template="plotly_dark"
            )
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.warning(f"Impossible d'afficher la carte: {str(e)}")
    
    # Analyse des produits
    st.subheader("Performance des produits")
    product_analysis = filtered_df.groupby('Product type').agg({
        'Total Sales': 'sum',
        'Profit': 'sum',
        'Margin %': 'mean',
        'Quantity': 'sum'
    }).sort_values('Total Sales', ascending=False).reset_index()
    
    fig4 = px.treemap(
        product_analysis,
        path=['Product type'],
        values='Total Sales',
        color='Margin %',
        title="Répartition du CA par type de produit",
        template="plotly_dark"
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    # Analyse de rentabilité
    st.subheader("Analyse de rentabilité")
    profitability = filtered_df.groupby(['Product type', 'Product line']).agg({
        'Total Sales': 'sum',
        'Profit': 'sum',
        'Margin %': 'mean'
    }).reset_index()
    
    fig5 = px.scatter(
        profitability,
        x='Total Sales',
        y='Margin %',
        size='Profit',
        color='Product line',
        hover_name='Product type',
        log_x=True,
        title="Matrice de rentabilité (CA vs Marge)",
        template="plotly_dark"
    )
    st.plotly_chart(fig5, use_container_width=True)
    
    # Détection d'anomalies
    st.subheader("🚨 Détection d'anomalies")
    
    try:
        anomalies = filtered_df[
            (filtered_df['Margin %'] < filtered_df['Margin %'].quantile(0.05)) |
            (filtered_df['Sale price'] > filtered_df['Sale price'].quantile(0.95))
        ]
        
        if not anomalies.empty:
            st.dataframe(
                anomalies.sort_values('Margin %').head(20),
                column_config={
                    "Date": "Date",
                    "Product type": "Produit",
                    "Country of sale": "Pays",
                    "Total Sales": st.column_config.NumberColumn("CA", format="$%.2f"),
                    "Margin %": st.column_config.NumberColumn("Marge %", format="%.1f%%"),
                    "Sale price": st.column_config.NumberColumn("Prix", format="$%.2f")
                }
            )
        else:
            st.success("✅ Aucune anomalie détectée selon les critères actuels")
    except Exception as e:
        st.warning(f"Impossible de calculer les anomalies: {str(e)}")
    
    # Export des données
    st.subheader("📤 Export des données")
    export_format = st.selectbox("Format d'export", ["CSV", "Excel", "JSON"])
    
    if export_format == "CSV":
        buffer = BytesIO()
        filtered_df.to_csv(buffer, index=False, sep=';', encoding='utf-8')
        buffer.seek(0)
        st.download_button(
            label="Télécharger CSV",
            data=buffer,
            file_name="export_sales.csv",
            mime="text/csv"
        )
    elif export_format == "Excel":
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            filtered_df.to_excel(writer, index=False)
        buffer.seek(0)  # Important pour que le téléchargement fonctionne
        st.download_button(
            label="Télécharger Excel",
            data=buffer,
            file_name="export_sales.xlsx",
            mime="application/vnd.ms-excel"
        )
    else:
        st.download_button(
            label="Télécharger JSON",
            data=filtered_df.to_json(orient='records'),
            file_name="export_sales.json",
            mime="application/json"
        )

else:
    st.warning("Veuillez importer un fichier CSV pour commencer l'analyse")
    st.image("https://media.giphy.com/media/L8K62iTDkzGX6/giphy.gif", width=400)
