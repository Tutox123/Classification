import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ---------------------------
# 0. Setup - Page Config
# ---------------------------
st.set_page_config(page_title="Ultimate Sales Dashboard", layout="wide", page_icon="📊")

# ---------------------------
# 1. Sidebar Navigation
# ---------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📈 Dashboard", "📥 Export Data", "🚨 Alerts", "📊 Detailed Analysis"])

# ---------------------------
# 2. Upload Data
# ---------------------------
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, sep=';')
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Total Sales'] = df['Quantity'] * df['Selling price']
    df['Total Buying Cost'] = df['Quantity'] * df['Buying cost']
    df['Gross Profit'] = df['Total Sales'] - df['Total Buying Cost']
    df['Gross Margin %'] = (df['Gross Profit'] / df['Total Sales']) * 100
    return df

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

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
    filtered_df = filtered_df[(filtered_df['Date'] >= pd.to_datetime(selected_date[0])) & (filtered_df['Date'] <= pd.to_datetime(selected_date[1]))]

    # KPI Calculations
    total_sales = filtered_df['Total Sales'].sum()
    total_buying_cost = filtered_df['Total Buying Cost'].sum()
    gross_profit = filtered_df['Gross Profit'].sum()
    gross_margin = (gross_profit / total_sales) * 100 if total_sales else 0
    total_quantity = filtered_df['Quantity'].sum()
    avg_selling_price = filtered_df['Selling price'].mean()
    avg_margin = filtered_df['Gross Margin %'].mean()

    # Best and Worst sellers
    best_product = filtered_df.groupby('Type of Product')['Total Sales'].sum().idxmax()
    worst_product = filtered_df.groupby('Type of Product')['Total Sales'].sum().idxmin()

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
            st.metric("📦 Total Quantity", f"{total_quantity}")
        with col3:
            st.metric("📈 Gross Margin %", f"{gross_margin:.2f}%")

        st.success(f"🏆 Best Seller: **{best_product}**")
        st.error(f"⚠️ Worst Seller: **{worst_product}**")

        st.markdown("---")

        # Sales over time
        sales_time = filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).sum().reset_index()
        sales_time['Date'] = sales_time['Date'].dt.to_timestamp()

        fig1 = px.area(sales_time, x='Date', y='Total Sales', title="Sales Over Time", template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

        # Top 5 Countries
        top_countries = filtered_df.groupby('Code country').sum().sort_values('Total Sales', ascending=False).head(5).reset_index()
        fig2 = px.bar(top_countries, x='Code country', y='Total Sales', title="Top 5 Countries", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

        # Sales by Ordering Method
        ordering_sales = filtered_df.groupby('Ordering method').sum().reset_index()
        fig3 = px.pie(ordering_sales, values='Total Sales', names='Ordering method', title='Sales by Ordering Method', template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

    elif page == "📥 Export Data":
        st.title("📥 Download your filtered data")
        buffer = BytesIO()
        filtered_df.to_csv(buffer, index=False, sep=';')
        buffer.seek(0)
        st.download_button(label="Download CSV", data=buffer, file_name="filtered_data.csv", mime="text/csv")

    elif page == "🚨 Alerts":
        st.title("🚨 Alerts & Anomalies")

        low_margin = filtered_df[filtered_df['Gross Margin %'] < 20]
        negative_margin = filtered_df[filtered_df['Gross Margin %'] < 0]
        overpriced = filtered_df[filtered_df['Selling price'] > filtered_df['Selling price'].quantile(0.95)]

        if not low_margin.empty:
            st.warning(f"⚠️ {len(low_margin)} Products with Margin < 20%")
            st.dataframe(low_margin)
        
        if not negative_margin.empty:
            st.error(f"❌ {len(negative_margin)} Products with Negative Margin")
            st.dataframe(negative_margin)

        if not overpriced.empty:
            st.info(f"💸 {len(overpriced)} Products Highly Priced (Top 5%)")
            st.dataframe(overpriced)

    elif page == "📊 Detailed Analysis":
        st.title("📊 Deep Dive Analysis")

        # Analysis per Product Line
        st.subheader("Sales by Line of Product")
        line_sales = filtered_df.groupby('Line of product').sum().reset_index()
        fig4 = px.bar(line_sales, x='Line of product', y='Total Sales', title="Sales by Line of Product", template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)

        st.subheader("Raw Data View")
        st.dataframe(filtered_df)

else:
    st.warning("Please upload a CSV file to continue.")

