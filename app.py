import streamlit as st

st.set_page_config(
    page_title="CTI Fraud Pipeline",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Cyber Fraud Intelligence Architecture")
st.markdown("### Operational Deployment - Phase 1 Local")
st.markdown("Select a module from the sidebar to begin analysis.")

# Basic session state initialization for future RBAC integration
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = True 
    st.session_state['role'] = 'analyst'

st.sidebar.success("Pipeline Active.")