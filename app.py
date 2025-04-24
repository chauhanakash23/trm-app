"""
TRM Modernization Application - Main Entry Point

This application classifies software products into TRM domains and subdomains,
assesses risk factors, and provides visualization tools for analysis.
"""

import streamlit as st
import pandas as pd
import os
import base64
import json
from typing import Dict, Any, List, Optional

# Import configuration
import config

# Import utilities and services
from classification import rule_based_classify, llm_classify, AVAILABLE_METHODS, DEFAULT_METHODS, run_classification
from risk_assessment import flag_risk, generate_risk_metrics
from data_processor import load_data, filter_data, get_unique_values, generate_statistics, export_data
from ui_components import (
    render_header, render_classification_controls, render_filters,
    render_results, render_dashboard, render_audit_log
)
from utils import is_api_key_configured, create_download_link

# Configure Streamlit page
st.set_page_config(
    page_title="TRM Modernization Tool",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_classified' not in st.session_state:
    st.session_state.data_classified = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

def main():
    """Main application function."""
    # Render header
    render_header()
    
    # Create sidebar for settings and actions
    with st.sidebar:
        st.header("Data Source")
        
        # File upload option
        uploaded_file = st.file_uploader(
            "Upload a CSV file containing software data",
            type=["csv"],
            help="If no file is uploaded, the default dataset will be used."
        )
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        use_default = st.checkbox("Use default dataset", value=st.session_state.uploaded_file is None)
        
        # Horizontal line for visual separation
        st.markdown("---")
        
        # Classification method selection
        classification_methods = st.multiselect(
            "Select Classification Methods",
            options=AVAILABLE_METHODS,
            default=DEFAULT_METHODS,
            help="Choose one or more classification methods to apply"
        )
        
        if not classification_methods:
            st.warning("Please select at least one classification method")
        
        # Run classification button
        if st.button("Run Classification", type="primary"):
            with st.spinner('Classifying software products...'):
                # Load data based on user selection
                if use_default or st.session_state.uploaded_file is None:
                    df = load_data()
                else:
                    df = load_data(uploaded_file=st.session_state.uploaded_file)
                
                # Run classification based on selected methods
                for method in classification_methods:
                    df = run_classification(df, method)
                
                # Run risk assessment
                df['Risk Flag'] = df.apply(flag_risk, axis=1)
                
                # Save the classified data in the session state
                st.session_state.classified_df = df
                st.session_state.data_classified = True
                
                st.success('Classification Complete!')
        
        # Export options
        if st.session_state.data_classified:
            st.header("Export Options")
            export_format = st.selectbox(
                "Export Format",
                ["CSV", "JSON"]
            )
            
            if st.button("Export Data"):
                # Use the correct DataFrame
                export_df = st.session_state.classified_df
                
                if export_format == "CSV":
                    download_link = create_download_link(
                        export_df,
                        "trm_classification.csv",
                        "Download CSV"
                    )
                    st.markdown(download_link, unsafe_allow_html=True)
                else:
                    # JSON export
                    json_str = export_df.to_json(orient='records')
                    b64 = base64.b64encode(json_str.encode()).decode()
                    href = f'<a href="data:file/json;base64,{b64}" download="trm_classification.json">Download JSON</a>'
                    st.markdown(href, unsafe_allow_html=True)
    
    # Display initial instructions
    if not st.session_state.data_classified:
        # Show simple instructions without data preview
        st.info("👈 Upload a CSV file or select the default dataset, then choose a classification method and click 'Run Classification'.")
    
    # Process and display data
    if st.session_state.data_classified:
        # Use the classified data
        display_df = st.session_state.classified_df
        
        # Generate risk metrics
        risk_metrics = generate_risk_metrics(display_df)
        
        # Render the dashboard
        render_dashboard(display_df, risk_metrics)
        
        # Get unique values for filters
        unique_values = get_unique_values(display_df)
        
        # Render search and filters
        search_term, domain, status, risk_level = render_filters(unique_values)
        
        # Filter the data
        filtered_df = filter_data(
            display_df,
            search_term=search_term,
            domain=domain if domain != config.UI_SELECT_ALL else None,
            status=status if status != config.UI_SELECT_ALL else None,
            risk_level=risk_level if risk_level != config.UI_SELECT_ALL else None
        )
        
        # Render results and audit log
        render_results(filtered_df, risk_metrics)
        render_audit_log(filtered_df.reset_index(drop=True))

# Run the app
if __name__ == "__main__":
    main()