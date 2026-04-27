import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_PATH = 'database/fraud_events.db'

st.set_page_config(page_title="Trend Lines", layout="wide")

@st.cache_data
def fetch_telemetry():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM fraud_events", conn)
    conn.close()
    df['occurrence_date'] = pd.to_datetime(df['occurrence_date'])
    df['month_year'] = df['occurrence_date'].dt.to_period('M').astype(str)
    return df

st.title("Analytical Models: Trend Lines & Commoditization")

df = fetch_telemetry()

if df.empty:
    st.warning("Insufficient telemetry for trend generation.")
    st.stop()

# 1. Commoditization Clock
st.subheader("TTP Commoditization Timeline")
fig_commoditization = px.scatter(
    df, 
    x="occurrence_date", 
    y="fraud_category",
    color="commoditization_stage",
    color_discrete_map={
        "Artisanal": "#e74c3c",
        "Packaged": "#f39c12",
        "Saturated": "#95a5a6"
    },
    hover_data=["attack_vector", "ttp_mitre"],
    title="Window of Maximum Risk Identification"
)
fig_commoditization.update_traces(marker=dict(size=12))
st.plotly_chart(fig_commoditization, use_container_width=True)

# 2. Sector Targeting Shift
st.subheader("Sector Targeting Distribution")
sector_counts = df.groupby(['victim_sector', 'fraud_category']).size().reset_index(name='count')
fig_sectors = px.bar(
    sector_counts, 
    x="victim_sector", 
    y="count",
    color="fraud_category",
    title="Targeted Client Sectors"
)
st.plotly_chart(fig_sectors, use_container_width=True)

# 3. Confidence Baseline
st.subheader("Intelligence Source Confidence")
fig_confidence = px.histogram(
    df, 
    x="confidence_overall", 
    color="confidence_overall",
    category_orders={"confidence_overall": ["Low", "Medium", "High"]},
    title="Telemetry Reliability Distribution"
)
st.plotly_chart(fig_confidence, use_container_width=True)