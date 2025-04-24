"""
UI components for the TRM Modernization application.

This module provides functions to render various UI elements
for the application interface.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Tuple, Dict, List, Any

import config

def render_header():
    """Render the application header."""
    st.title(config.APP_TITLE)
    
    # Add app description
    st.markdown("""
    This application helps classify software products into appropriate TRM Domains and Subdomains,
    and identifies potential risk factors. Use the tools below to classify products and explore the results.
    """)
    
    # Add horizontal rule
    st.markdown("---")

def render_classification_controls() -> str:
    """
    Render the classification method selection controls.
    
    Returns:
        Selected classification method
    """
    st.subheader("Classification Settings")
    
    # Classification method selection
    classification_method = st.selectbox(
        "Select Classification Method",
        ["Rule-based", "LLM-based (OpenAI GPT)"]
    )
    
    # Check if OpenAI API key is configured when LLM-based is selected
    if classification_method == "LLM-based (OpenAI GPT)" and not config.OPENAI_API_KEY:
        st.warning("⚠️ OpenAI API Key not configured. Classification may fall back to rule-based method.")
    
    return classification_method

def render_filters(unique_values: Dict[str, List[str]]) -> Tuple[str, str, str, str]:
    """
    Render the search and filter UI elements.
    
    Args:
        unique_values: Dictionary of unique values for each filter field
        
    Returns:
        Tuple of (search_term, domain, status, risk_level)
    """
    st.header("🔍 Search and Filter Software")
    
    # Create a 2-column layout for filters
    col1, col2 = st.columns([3, 1])
    
    # Search input in column 1
    with col1:
        search_term = st.text_input("Search by Name or Description")
    
    # Add an empty column for spacing
    st.write("")
    
    # Create a 3-column layout for dropdowns
    col1, col2, col3 = st.columns(3)
    
    # Filter dropdowns
    with col1:
        domain = st.selectbox(
            "TRM Domain", 
            unique_values.get('TRM Domain', [config.UI_SELECT_ALL])
        )
    
    with col2:
        status = st.selectbox(
            "Lifecycle Status", 
            unique_values.get('Lifecycle Status', [config.UI_SELECT_ALL])
        )
    
    with col3:
        risk_level = st.selectbox(
            "Risk Level", 
            unique_values.get('Risk Flag', [config.UI_SELECT_ALL])
        )
    
    # Add a small space below filters
    st.write("")
    
    return search_term, domain, status, risk_level

def render_results(filtered_df, risk_metrics):
    """Display the filtered results."""
    st.subheader("Results")
    st.dataframe(filtered_df)

def render_dashboard(df, risk_metrics):
    """Display the dashboard visualizations."""
    st.subheader("Dashboard")
    st.write("Total Products:", len(df))

def render_audit_log(df):
    """Display the audit log."""
    st.subheader("Audit Log")
    st.write("Last updated:", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
