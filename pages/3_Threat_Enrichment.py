import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Path resolution to access ingestion modules from pages directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ingestion.tip_enrichment import pivot_ioc_to_entities, extract_ioc_context

load_dotenv()
API_KEY = os.getenv("SILOBREAKER_API_KEY")
SHARED_KEY = os.getenv("SILOBREAKER_SHARED_KEY")

st.set_page_config(page_title="Threat Enrichment", layout="wide")
st.title("External Enrichment: Silobreaker Pivot")

if not API_KEY or not SHARED_KEY:
    st.error("Silobreaker credentials missing from environment.")
    st.stop()

ioc_input = st.text_input("Enter Target Indicator (e.g., LockBit, APT29, Qilin)")

if st.button("Execute Structural Pivot"):
    if not ioc_input:
        st.warning("Indicator input required.")
        st.stop()
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Correlated Entities (Actors & Malware)")
        with st.spinner("Executing v2/infocus pivot..."):
            entity_data = pivot_ioc_to_entities(ioc_input, API_KEY, SHARED_KEY)
            
            if "error" in entity_data:
                st.error(entity_data["error"])
            elif "Items" in entity_data and entity_data["Items"]:
                for item in entity_data["Items"]:
                    st.markdown(f"- **{item.get('Description', 'Unknown')}** ({item.get('Type', 'Unknown')}) | Relevance: {item.get('Relevance', 0):.2f}")
            else:
                st.info("No entities correlated.")
                
    with col2:
        st.subheader("Contextual Documents (30d)")
        with st.spinner("Executing v2/documents/search extraction..."):
            doc_data = extract_ioc_context(ioc_input, API_KEY, SHARED_KEY)
            
            if "error" in doc_data:
                st.error(doc_data["error"])
            elif "Items" in doc_data and doc_data["Items"]:
                for item in doc_data["Items"]:
                    st.markdown(f"- [{item.get('Description', 'Untitled')}]({item.get('SourceUrl', '#')})")
                    st.caption(f"Publisher: {item.get('Publisher', 'Unknown')} | Date: {item.get('PublicationDate', 'Unknown')}")
            else:
                st.info("No documents found.")