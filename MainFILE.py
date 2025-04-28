import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime
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

        # Conversion des dates avec plusieurs formats possibles
        date_formats = ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d', '%d-%m-%Y']
        for fmt in date_formats:
            try:
                df['Date'] = pd.to_datetime(df['Date'], format=fmt, errors='raise')
                break
            except ValueError:
                continue
        else:
            # Si aucun format ne fonctionne, essayer l'inférence automatique
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
        
        # Vérifier si des dates sont invalides
        if df['Date'].isnull().any():
            invalid_dates = df[df['Date'].isnull()]['Date'].head()
            st.warning(f"Certaines dates n'ont pas pu être interprétées. Exemples : {invalid_dates.tolist()}")
        
        # Calculs temporels
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Week'] = df['Date'].dt.isocalendar().week
        df['Day'] = df['Date'].dt.day_name()
        
        # Calculs financiers
        df['Total Sales'] = df['Quantity'] * df['Sale price']
        df['Total Cost'] = df['Quantity'] * df['Purchase cost']
        df['Profit'] = df['Total Sales'] - df['Total Cost']
        df['Margin %'] = np.where(
            df['Total Sales'] > 0,
            (df['Profit'] / df['Total Sales']) * 100,
            0
        )
        df['ROI'] = np.where(
            df['Total Cost'] > 0,
            (df['Profit'] / df['Total Cost']) * 100,
            0
        )
        
        # Segmentation
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
    
    # Vérifier si le chargement a réussi
    if df is not None:
        with st.sidebar.expander("⏱ Filtre temporel", expanded=True):
            # Convertir les dates en format compatible avec st.date_input
            min_date = df['Date'].min().to_pydatetime()
            max_date = df['Date'].max().to_pydatetime()
            
            date_range = st.date_input(
                "Période",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date
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
            avg_margin = filtered_df['Margin %'].mean()
            margin_trend = "↑" if avg_margin > df['Margin %'].mean() else "↓"
            display_kpi("📈 Marge Moyenne", 
                       f"{avg_margin:.1f}%", 
                       f"{margin_trend} {abs(avg_margin - df['Margin %'].mean()):.1f}%",
                       "inverse" if avg_margin < df['Margin %'].mean() else "normal")
        with col4:
            display_kpi("🔄 ROI Moyen", f"{filtered_df['ROI'].mean():.1f}%")
        
        # Tendances temporelles
        st.subheader("Analyse temporelle")
        time_group = {
            "Journalier": 'Date',
            "Hebdomadaire": 'Week',
            "Mensuel": 'Month',
            "Trimestriel": pd.PeriodIndex(filtered_df['Date'], freq='Q'),
            "Annuel": 'Year'
        }[time_granularity]
        
        time_analysis = filtered_df.groupby(time_group).agg({
            'Total Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
        fig1 = px.area(
            time_analysis,
            x=time_group,
            y='Total Sales',
            title=f"Évolution du CA ({time_granularity.lower()})",
            template="plotly_dark"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Analyse comparative
        st.subheader("Analyse comparative")
        col1, col2 = st.columns(2)
        with col1:
            # Top 10 produits par marge
            top_products = filtered_df.groupby('Product type').agg({
                'Total Sales': 'sum',
                'Margin %': 'mean'
            }).nlargest(10, 'Total Sales').reset_index()
            
            fig2 = px.bar(
                top_products,
                x='Product type',
                y='Total Sales',
                color='Margin %',
                title="Top 10 Produits par CA",
                template="plotly_dark"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Performance par méthode de commande
            order_method = filtered_df.groupby('Ordering method').agg({
                'Total Sales': 'sum',
                'Margin %': 'mean'
            }).reset_index()
            
            fig3 = px.pie(
                order_method,
                values='Total Sales',
                names='Ordering method',
                title="Répartition par méthode de commande",
                template="plotly_dark"
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Détection d'opportunités
        st.subheader("🔎 Détection d'opportunités")
        high_margin = filtered_df[
            (filtered_df['Margin %'] > filtered_df['Margin %'].quantile(0.9)) &
            (filtered_df['Total Sales'] > filtered_df['Total Sales'].quantile(0.5))
        ]
        
        if not high_margin.empty:
            st.success("🌟 Produits à fort potentiel (Haute marge et bon volume)")
            st.dataframe(
                high_margin.groupby('Product type').agg({
                    'Total Sales': 'sum',
                    'Margin %': 'mean',
                    'Quantity': 'sum'
                }).sort_values('Margin %', ascending=False),
                column_config={
                    "Total Sales": st.column_config.NumberColumn("CA", format="$%.0f"),
                    "Margin %": st.column_config.NumberColumn("Marge %", format="%.1f%%"),
                    "Quantity": st.column_config.NumberColumn("Quantité", format="%.0f")
                }
            )
        
        # Export des données
        st.subheader("📤 Export des données")
        export_format = st.selectbox("Format d'export", ["CSV", "Excel"])
        
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
        else:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                filtered_df.to_excel(writer, index=False)
            st.download_button(
                label="Télécharger Excel",
                data=buffer,
                file_name="export_sales.xlsx",
                mime="application/vnd.ms-excel"
            )

else:
    st.warning("Veuillez importer un fichier CSV pour commencer l'analyse")
    st.image("https://media.giphy.com/media/L8K62iTDkzGX6/giphy.gif", width=400)
