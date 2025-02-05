
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Set page config
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS
st.markdown('''
    <style>
    .main {
        padding: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
''', unsafe_allow_html=True)

# Title and description
st.title("📊 Sales Analytics Dashboard")
st.markdown("Interactive dashboard for analyzing sales performance and customer insights")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['Date'].min(), df['Date'].max()],
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

# Region filter
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Product filter
selected_products = st.sidebar.multiselect(
    "Select Products",
    options=df['Product'].unique(),
    default=df['Product'].unique()
)

# Filter data based on selections
filtered_df = df[
    (df['Date'].dt.date >= date_range[0]) &
    (df['Date'].dt.date <= date_range[1]) &
    (df['Region'].isin(selected_regions)) &
    (df['Product'].isin(selected_products))
]

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
with col2:
    st.metric("Average Order Value", f"${filtered_df['Sales'].mean():,.2f}")
with col3:
    st.metric("Total Customers", len(filtered_df))
with col4:
    st.metric("Avg. Satisfaction", f"{filtered_df['Customer_Satisfaction'].mean():.2f}/5.0")

# Sales Trends
st.subheader("Sales Trends")
sales_tab1, sales_tab2 = st.tabs(["Daily Trends", "Regional Analysis"])

with sales_tab1:
    daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()
    fig_daily = px.line(daily_sales, x='Date', y='Sales',
                       title='Daily Sales Trend')
    fig_daily.update_layout(height=400)
    st.plotly_chart(fig_daily, use_container_width=True)

with sales_tab2:
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    fig_region = px.bar(region_sales, x='Region', y='Sales',
                       title='Sales by Region')
    fig_region.update_layout(height=400)
    st.plotly_chart(fig_region, use_container_width=True)

# Customer Analysis
st.subheader("Customer Insights")
customer_tab1, customer_tab2 = st.tabs(["Demographics", "Satisfaction Analysis"])

with customer_tab1:
    col1, col2 = st.columns(2)

    with col1:
        gender_dist = filtered_df['Customer_Gender'].value_counts()
        fig_gender = px.pie(values=gender_dist.values, 
                          names=gender_dist.index,
                          title='Customer Gender Distribution')
        st.plotly_chart(fig_gender, use_container_width=True)

    with col2:
        fig_age = px.histogram(filtered_df, x='Customer_Age',
                             title='Customer Age Distribution',
                             nbins=20)
        st.plotly_chart(fig_age, use_container_width=True)

with customer_tab2:
    satisfaction_by_product = filtered_df.groupby('Product')['Customer_Satisfaction'].mean().reset_index()
    fig_satisfaction = px.bar(satisfaction_by_product, 
                            x='Product', 
                            y='Customer_Satisfaction',
                            title='Average Customer Satisfaction by Product')
    st.plotly_chart(fig_satisfaction, use_container_width=True)

# Product Performance
st.subheader("Product Performance")
product_sales = filtered_df.groupby('Product')['Sales'].sum().reset_index()
fig_product = px.bar(product_sales, x='Product', y='Sales',
                    title='Sales by Product')
st.plotly_chart(fig_product, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit")
