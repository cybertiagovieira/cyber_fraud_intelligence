import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_PATH = 'database/fraud_events.db'

st.set_page_config(page_title="Executive Pulse", layout="wide")

@st.cache_data
def fetch_telemetry():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM fraud_events", conn)
    conn.close()
    return df

st.title("Executive Pulse: Cyber Fraud Telemetry")

df = fetch_telemetry()

if df.empty:
    st.warning("No telemetry available in database.")
    st.stop()

# Metric KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Events (30d)", len(df))
col2.metric("Primary Vector", df['attack_vector'].mode()[0])
col3.metric("Top Targeted Geo", df['victim_geo'].mode()[0])
col4.metric("Estimated Impact", f"€{df['financial_impact'].sum():,.2f}")

st.markdown("---")

# Visualization Row
col_chart, col_data = st.columns([2, 1])

with col_chart:
    st.subheader("Fraud Category Distribution")
    fig = px.pie(df, names='fraud_category', values='financial_impact', hole=0.4, 
                 title="Impact by Fraud Category")
    st.plotly_chart(fig, width="stretch")

with col_data:
    st.subheader("Actionable Intelligence")
    for index, row in df.iterrows():
        st.info(f"**{row['fraud_category']}**: {row['management_impact']}")

st.markdown("---")
st.subheader("Raw Telemetry (Analyst View)")
st.dataframe(df[['event_id', 'occurrence_date', 'fraud_category', 'attack_vector', 'victim_geo', 'financial_impact']])