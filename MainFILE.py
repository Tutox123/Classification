import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime
import numpy as np

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Advanced Sales Analytics Dashboard",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Utility Functions
# ---------------------------
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, sep=';', header=0, decimal=',', encoding='utf-8')
        df.columns = df.columns.str.strip()
        
        # Check for required columns
        required_columns = ['Date', 'Product type', 'Product line', 'Quantity', 
                          'Sale price', 'Purchase cost', 'Ordering method', 'Country of sale']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Missing columns: {', '.join(missing_cols)}")
            st.stop()

        # Convert dates with multiple possible formats
        date_formats = ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d', '%d-%m-%Y']
        for fmt in date_formats:
            try:
                df['Date'] = pd.to_datetime(df['Date'], format=fmt, errors='raise')
                break
            except ValueError:
                continue
        else:
            # If no format works, try automatic inference
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
        
        # Check for invalid dates
        if df['Date'].isnull().any():
            invalid_dates = df[df['Date'].isnull()]['Date'].head()
            st.warning(f"Some dates could not be interpreted. Examples: {invalid_dates.tolist()}")
        
        # Time-based calculations
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Week'] = df['Date'].dt.isocalendar().week
        df['Day'] = df['Date'].dt.day_name()
        
        # Financial calculations
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
        st.error(f"❌ Loading error: {str(e)}")
        st.stop()

def display_kpi(title, value, delta=None, delta_type=None):
    st.metric(
        label=title,
        value=value,
        delta=delta,
        delta_color=delta_type if delta_type else "normal"
    )

# ---------------------------
# User Interface
# ---------------------------
st.sidebar.title("🔍 Navigation & Configuration")
uploaded_file = st.sidebar.file_uploader("📤 Upload Data (CSV)", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    
    # Check if data is loaded successfully
    if df is not None:
        with st.sidebar.expander("⏱ Time Filter", expanded=True):
            # Convert dates to be compatible with st.date_input
            min_date = df['Date'].min().to_pydatetime()
            max_date = df['Date'].max().to_pydatetime()
            
            date_range = st.date_input(
                "Period",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
            
            time_granularity = st.selectbox(
                "Time Granularity",
                ["Daily", "Weekly", "Monthly", "Quarterly", "Annual"]
            )
        
        with st.sidebar.expander("🌍 Geographic Filters"):
            countries = st.multiselect(
                "Countries",
                options=df['Country of sale'].unique(),
                default=df['Country of sale'].unique()
            )
        
        with st.sidebar.expander("📦 Product Filters"):
            product_types = st.multiselect(
                "Product Type",
                options=df['Product type'].unique(),
                default=df['Product type'].unique()
            )
            
            product_lines = st.multiselect(
                "Product Line",
                options=df['Product line'].unique(),
                default=df['Product line'].unique()
            )
        
        with st.sidebar.expander("💰 Financial Filters"):
            margin_range = st.slider(
                "Margin (%)",
                min_value=float(df['Margin %'].min()),
                max_value=float(df['Margin %'].max()),
                value=(float(df['Margin %'].min()), float(df['Margin %'].max()))
            )
        
        # Apply filters
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
        # Main Dashboard
        # ---------------------------
        st.title("📈 Advanced Analytics Dashboard")
        
        # Key KPIs
        st.subheader("Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            display_kpi("💰 Total Sales", f"${filtered_df['Total Sales'].sum():,.0f}")
        with col2:
            display_kpi("📦 Total Quantity", f"{filtered_df['Quantity'].sum():,}")
        with col3:
            avg_margin = filtered_df['Margin %'].mean()
            margin_trend = "↑" if avg_margin > df['Margin %'].mean() else "↓"
            display_kpi("📈 Average Margin", 
                       f"{avg_margin:.1f}%", 
                       f"{margin_trend} {abs(avg_margin - df['Margin %'].mean()):.1f}%",
                       "inverse" if avg_margin < df['Margin %'].mean() else "normal")
        with col4:
            display_kpi("🔄 Average ROI", f"{filtered_df['ROI'].mean():.1f}%")
        
        # Time Trends
        st.subheader("Time-Based Analysis")
        time_group = {
            "Daily": 'Date',
            "Weekly": 'Week',
            "Monthly": 'Month',
            "Quarterly": pd.PeriodIndex(filtered_df['Date'], freq='Q'),
            "Annual": 'Year'
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
            title=f"Sales Evolution ({time_granularity.lower()})",
            template="plotly_dark"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Comparative Analysis
        st.subheader("Comparative Analysis")
        col1, col2 = st.columns(2)
        with col1:
            # Top 10 products by margin
            top_products = filtered_df.groupby('Product type').agg({
                'Total Sales': 'sum',
                'Margin %': 'mean'
            }).nlargest(10, 'Total Sales').reset_index()
            
            fig2 = px.bar(
                top_products,
                x='Product type',
                y='Total Sales',
                color='Margin %',
                title="Top 10 Products by Sales",
                template="plotly_dark"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Performance by ordering method
            order_method = filtered_df.groupby('Ordering method').agg({
                'Total Sales': 'sum',
                'Margin %': 'mean'
            }).reset_index()
            
            fig3 = px.pie(
                order_method,
                values='Total Sales',
                names='Ordering method',
                title="Sales Distribution by Ordering Method",
                template="plotly_dark"
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Opportunity Detection
        st.subheader("🔎 Opportunity Detection")
        high_margin = filtered_df[
            (filtered_df['Margin %'] > filtered_df['Margin %'].quantile(0.9)) &
            (filtered_df['Total Sales'] > filtered_df['Total Sales'].quantile(0.5))
        ]
        
        if not high_margin.empty:
            st.success("🌟 High Potential Products (High Margin & Good Volume)")
            st.dataframe(
                high_margin.groupby('Product type').agg({
                    'Total Sales': 'sum',
                    'Margin %': 'mean',
                    'Quantity': 'sum'
                }).sort_values('Margin %', ascending=False),
                column_config={
                    "Total Sales": st.column_config.NumberColumn("Sales", format="$%.0f"),
                    "Margin %": st.column_config.NumberColumn("Margin %", format="%.1f%%"),
                    "Quantity": st.column_config.NumberColumn("Quantity", format="%.0f")
                }
            )
        
        # Data Export
        st.subheader("📤 Data Export")
        export_format = st.selectbox("Export Format", ["CSV", "Excel"])
        
        if export_format == "CSV":
            buffer = BytesIO()
            filtered_df.to_csv(buffer, index=False, sep=';', encoding='utf-8')
            buffer.seek(0)
            st.download_button(
                label="Download CSV",
                data=buffer,
                file_name="export_sales.csv",
                mime="text/csv"
            )
        else:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                filtered_df.to_excel(writer, index=False)
            st.download_button(
                label="Download Excel",
                data=buffer,
                file_name="export_sales.xlsx",
                mime="application/vnd.ms-excel"
            )

else:
    st.warning("Please upload a CSV file to begin the analysis")
    st.image("https://media.giphy.com/media/L8K62iTDkzGX6/giphy.gif", width=400)

