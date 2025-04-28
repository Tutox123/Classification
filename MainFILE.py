import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ---------------------------
# Setup - Page Config
# ---------------------------
st.set_page_config(page_title="Ultimate Sales Dashboard", layout="wide", page_icon="📊")

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📈 Dashboard", "📥 Export Data", "🚨 Alerts", "📊 Detailed Analysis"])

# ---------------------------
# Upload Data
# ---------------------------
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, sep=';', header=0, decimal=',', encoding='utf-8')
        df.columns = df.columns.str.strip()

        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        else:
            st.error("❌ 'Date' column is missing. Please check your CSV file.")
            st.stop()

        required_columns = ['Quantity', 'Selling price', 'Buying cost', 'Type of Product']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"❌ Column '{col}' is missing. Please check your CSV file.")
                st.stop()

        # Calculations
        df['Total Sales'] = df['Quantity'] * df['Selling price']
        df['Total Buying Cost'] = df['Quantity'] * df['Buying cost']
        df['Gross Profit'] = df['Total Sales'] - df['Total Buying Cost']
        df['Gross Margin %'] = (df['Gross Profit'] / df['Total Sales']) * 100
        return df
    except Exception as e:
        st.error(f"❌ Error loading CSV file: {str(e)}")
        st.stop()

uploaded_file = st.sidebar.file_uploader("Upload your CSV file (semicolon separated)", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    # Filters
    with st.sidebar.expander("🔎 Filters", expanded=True):
        selected_product = st.multiselect("Type of Product", options=df['Type of Product'].unique())
        selected_country = st.multiselect("Country Code", options=df['Code country'].unique())
        selected_ordering = st.multiselect("Ordering Method", options=df['Ordering method'].unique())
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        selected_date = st.date_input("Date Range", [min_date, max_date])

    # Apply filters
    filtered_df = df.copy()
    if selected_product:
        filtered_df = filtered_df[filtered_df['Type of Product'].isin(selected_product)]
    if selected_country:
        filtered_df = filtered_df[filtered_df['Code country'].isin(selected_country)]
    if selected_ordering:
        filtered_df = filtered_df[filtered_df['Ordering method'].isin(selected_ordering)]
    filtered_df = filtered_df[(filtered_df['Date'] >= pd.to_datetime(selected_date[0])) & 
                            (filtered_df['Date'] <= pd.to_datetime(selected_date[1]))]

    # KPI Calculations
    total_sales = filtered_df['Total Sales'].sum()
    total_buying_cost = filtered_df['Total Buying Cost'].sum()
    gross_profit = filtered_df['Gross Profit'].sum()
    gross_margin = (gross_profit / total_sales) * 100 if total_sales else 0
    total_quantity = filtered_df['Quantity'].sum()
    avg_selling_price = filtered_df['Selling price'].mean()
    avg_margin = filtered_df['Gross Margin %'].mean()

    # ---------------------------
    # Pages
    # ---------------------------
    if page == "🏠 Home":
        st.title("📊 Welcome to the Ultimate Dashboard")
        st.write("Upload your file in the sidebar and start exploring your sales data interactively!")
        st.image("https://media.giphy.com/media/L8K62iTDkzGX6/giphy.gif", width=400)

    elif page == "📈 Dashboard":
        st.title("📈 Dashboard Overview")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Total Sales", f"${total_sales:,.2f}")
        with col2:
            st.metric("📦 Total Quantity", f"{total_quantity:,}")
        with col3:
            st.metric("📈 Gross Margin %", f"{gross_margin:.2f}%")

        # Enhanced Product Performance Analysis
        product_analysis = filtered_df.groupby('Type of Product').agg({
            'Total Sales': 'sum',
            'Quantity': 'sum',
            'Gross Margin %': 'mean'
        }).sort_values('Total Sales', ascending=False).reset_index()
        
        if len(product_analysis) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏆 Top Performing Products")
                top_products = product_analysis.head(3)
                for i, row in top_products.iterrows():
                    st.metric(
                        label=f"#{i+1} {row['Type of Product']}",
                        value=f"${row['Total Sales']:,.2f}",
                        delta=f"{row['Gross Margin %']:.1f}% margin"
                    )
            
            with col2:
                st.subheader("⚠️ Underperforming Products")
                bottom_products = product_analysis.tail(3).iloc[::-1]  # Reverse to show worst first
                for i, row in bottom_products.iterrows():
                    st.metric(
                        label=f"#{len(product_analysis)-i} {row['Type of Product']}",
                        value=f"${row['Total Sales']:,.2f}",
                        delta=f"{row['Gross Margin %']:.1f}% margin",
                        delta_color="inverse"
                    )

        st.markdown("---")

        # Sales Over Time Chart
        try:
            sales_time = filtered_df.set_index('Date').resample('M').agg({
                'Total Sales': 'sum',
                'Quantity': 'sum'
            }).reset_index()
            
            fig1 = px.area(sales_time, x='Date', y='Total Sales', 
                          title="Sales Over Time", template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating sales over time chart: {str(e)}")

        # Top Countries Chart
        try:
            top_countries = filtered_df.groupby('Code country').agg({
                'Total Sales': 'sum'
            }).sort_values('Total Sales', ascending=False).head(5).reset_index()
            
            fig2 = px.bar(top_countries, x='Code country', y='Total Sales', 
                         title="Top 5 Countries", template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating countries chart: {str(e)}")

        # Ordering Method Chart
        try:
            ordering_sales = filtered_df.groupby('Ordering method').agg({
                'Total Sales': 'sum'
            }).reset_index()
            
            fig3 = px.pie(ordering_sales, values='Total Sales', names='Ordering method', 
                         title='Sales by Ordering Method', template="plotly_dark")
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating ordering method chart: {str(e)}")

    elif page == "📥 Export Data":
        st.title("📥 Download your filtered data")
        buffer = BytesIO()
        filtered_df.to_csv(buffer, index=False, sep=';', encoding='utf-8')
        buffer.seek(0)
        st.download_button(
            label="Download CSV",
            data=buffer,
            file_name="filtered_data.csv",
            mime="text/csv"
        )

    elif page == "🚨 Alerts":
        st.title("🚨 Alerts & Anomalies")

        # Low Margin Products
        low_margin = filtered_df[filtered_df['Gross Margin %'] < 20]
        if not low_margin.empty:
            st.warning(f"⚠️ {len(low_margin)} Products with Margin < 20%")
            st.dataframe(low_margin[['Type of Product', 'Gross Margin %', 'Total Sales']].sort_values('Gross Margin %'))
        
        # Negative Margin Products
        negative_margin = filtered_df[filtered_df['Gross Margin %'] < 0]
        if not negative_margin.empty:
            st.error(f"❌ {len(negative_margin)} Products with Negative Margin")
            st.dataframe(negative_margin[['Type of Product', 'Gross Margin %', 'Total Sales']].sort_values('Gross Margin %'))

        # Overpriced Products
        overpriced = filtered_df[filtered_df['Selling price'] > filtered_df['Selling price'].quantile(0.95)]
        if not overpriced.empty:
            st.info(f"💸 {len(overpriced)} Top 5% Most Expensive Products")
            st.dataframe(overpriced[['Type of Product', 'Selling price']].sort_values('Selling price', ascending=False))

    elif page == "📊 Detailed Analysis":
        st.title("📊 Deep Dive Analysis")
        
        # Product Performance Details
        st.subheader("Product Performance Breakdown")
        try:
            product_details = filtered_df.groupby('Type of Product').agg({
                'Total Sales': 'sum',
                'Quantity': 'sum',
                'Gross Margin %': 'mean',
                'Selling price': 'mean'
            }).sort_values('Total Sales', ascending=False).reset_index()
            
            st.dataframe(product_details.style.format({
                'Total Sales': '${:,.2f}',
                'Gross Margin %': '{:.1f}%',
                'Selling price': '${:.2f}'
            }))
        except Exception as e:
            st.error(f"Error generating product performance: {str(e)}")

        # Sales by Line of Product
        st.subheader("Sales by Line of Product")
        try:
            line_sales = filtered_df.groupby('Line of product').agg({
                'Total Sales': 'sum',
                'Quantity': 'sum'
            }).sort_values('Total Sales', ascending=False).reset_index()
            
            fig4 = px.bar(line_sales, x='Line of product', y='Total Sales', 
                         title="Sales by Line of Product", template="plotly_dark")
            st.plotly_chart(fig4, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating line of product chart: {str(e)}")

        # Raw Data View
        st.subheader("Raw Data View")
        st.dataframe(filtered_df)

else:
    st.warning("📥 Please upload a CSV file (semicolon separated).")
