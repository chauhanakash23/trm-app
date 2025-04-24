"""
Script to create required Python files for the TRM Modernization application.
"""

import os

# Classification module
classification_content = '''"""
Classification services for software products.

This module provides functions to classify software products into
appropriate TRM Domains and Subdomains using either rule-based or
LLM-based classification methods.
"""

import openai
import streamlit as st
from typing import Tuple, Dict, List, Optional

import config

def rule_based_classify(description: str, hint: str) -> Tuple[str, str]:
    """
    Classify software using rule-based keyword matching.
    
    Args:
        description: Description of the software product
        hint: Category hint for the software product
        
    Returns:
        A tuple of (domain, subdomain)
    """
    # Convert inputs to lowercase strings for case-insensitive matching
    desc_hint = f"{str(description).lower()} {str(hint).lower()}"
    
    # Check each domain's keywords
    for domain, keywords in config.CLASSIFICATION_KEYWORDS.items():
        if any(keyword in desc_hint for keyword in keywords):
            # Return the domain and its first subdomain
            return domain, config.TRM_DOMAINS_SUBDOMAINS[domain][0]
    
    # If no match found, return unclassified
    return config.DEFAULT_DOMAIN, config.DEFAULT_SUBDOMAIN

def llm_classify(product_name: str, description: str, hint: str) -> Tuple[str, str]:
    """
    Classify software using LLM-based classification (OpenAI GPT).
    
    Args:
        product_name: Name of the software product
        description: Description of the software product
        hint: Category hint for the software product
        
    Returns:
        A tuple of (domain, subdomain)
    """
    # Check if API key is configured
    if not config.OPENAI_API_KEY:
        st.warning("OpenAI API Key not configured. Using rule-based classification instead.")
        return rule_based_classify(description, hint)
    
    # Set the API key
    openai.api_key = config.OPENAI_API_KEY
    
    # Construct a prompt that includes valid domains and subdomains
    domains_text = "\\n".join([
        f"{i+1}. {domain} - {', '.join(subdomains)}"
        for i, (domain, subdomains) in enumerate(config.TRM_DOMAINS_SUBDOMAINS.items())
        if domain != config.DEFAULT_DOMAIN  # Exclude unclassified from prompt options
    ])
    
    prompt = (
        f"Classify the software product '{product_name}' described as '{description}' "
        f"with hint '{hint}' into one of these TRM Domains and Subdomains:\\n"
        f"{domains_text}\\n"
        f"If uncertain, return 'Unclassified'.\\n\\n"
        f"Return your answer in 'Domain, Subdomain' format only."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.OPENAI_TEMPERATURE
        )
        classification = response['choices'][0]['message']['content']
        
        # Handle unclassified case
        if classification.lower() == "unclassified":
            return config.DEFAULT_DOMAIN, config.DEFAULT_SUBDOMAIN
            
        # Parse the response
        try:
            domain, subdomain = classification.split(", ")
            domain = domain.strip()
            subdomain = subdomain.strip()
            
            # Validate domain and subdomain against known values
            if domain in config.TRM_DOMAINS_SUBDOMAINS:
                if subdomain in config.TRM_DOMAINS_SUBDOMAINS[domain]:
                    return domain, subdomain
            
            # If domain is valid but subdomain is not recognized
            if domain in config.TRM_DOMAINS_SUBDOMAINS:
                return domain, config.TRM_DOMAINS_SUBDOMAINS[domain][0]
                
            return config.DEFAULT_DOMAIN, config.DEFAULT_SUBDOMAIN
        except ValueError:
            # If the response couldn't be split
            return config.DEFAULT_DOMAIN, config.DEFAULT_SUBDOMAIN
            
    except Exception as e:
        st.warning(f"LLM API Error: {e}")
        # Fall back to rule-based classification on error
        return rule_based_classify(description, hint)
'''

# Config module
config_content = '''"""
Configuration settings for the TRM Modernization application.

This module contains application settings, constants, and configuration
values used throughout the application.
"""

import os
from dotenv import load_dotenv
from typing import Dict, List

# Load environment variables from .env file
load_dotenv()

# --- API Settings ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0"))

# --- Application Settings ---
APP_TITLE = "🛡️ USCIS TRM Modernization Prototype with LLM"
DATA_FILE_PATH = "data/software_list.csv"

# --- Default Values ---
DEFAULT_RISK_FLAG = "Normal"
DEFAULT_DOMAIN = "Unclassified"
DEFAULT_SUBDOMAIN = "Unclassified"

# --- Classification Settings ---
# TRM domains and their associated subdomains
TRM_DOMAINS_SUBDOMAINS: Dict[str, List[str]] = {
    "Data Management": ["Database Platforms", "Data Processing", "Data Storage"],
    "Artificial Intelligence": ["ML Frameworks", "NLP Tools", "Computer Vision"],
    "Security": ["Security Tools", "Authentication", "Encryption"],
    "Network": ["Networking Tools", "Load Balancers", "API Gateways"],
    "Development": ["IDEs", "Version Control", "CI/CD"],
    "Unclassified": ["Unclassified"]
}

# Keywords for rule-based classification
CLASSIFICATION_KEYWORDS = {
    "Data Management": ["database", "sql", "nosql", "data store", "postgresql", "mysql", "mongodb", "redis"],
    "Artificial Intelligence": ["machine learning", "ai", "ml", "artificial intelligence", "deep learning", "tensorflow", "pytorch"],
    "Security": ["security", "auth", "encryption", "firewall", "protection", "vulnerability", "antivirus"],
    "Network": ["network", "protocol", "routing", "traffic", "proxy", "load balancer", "api gateway"],
    "Development": ["ide", "git", "development", "programming", "code", "compiler", "build", "cicd"]
}

# --- UI Settings ---
UI_SELECT_ALL = "All"

# Risk status categories and descriptions
RISK_STATUSES = {
    "High-Risk": "High-Risk items require immediate attention",
    "Medium-Risk": "Medium-Risk items should be reviewed during regular cycles",
    "Normal": "Normal items have acceptable risk levels"
}

# Lifecycle statuses
LIFECYCLE_STATUSES = ["Active", "Deprecated", "Planned", "Beta"]

# Status to risk level mapping
STATUS_RISK_MAPPING = {
    "Deprecated": "High-Risk",
    "Beta": "Medium-Risk",
    "Active": "Normal",
    "Planned": "Normal"
}

# --- Styling ---
# Color schemes for risk levels
RISK_COLORS = {
    "High-Risk": "#FFCCCC",  # Light red
    "Medium-Risk": "#FFFFCC", # Light yellow
    "Normal": "#CCFFCC"       # Light green
}
'''

# Risk assessment module
risk_assessment_content = '''"""
Risk assessment services for software products.

This module provides functions to assess risk levels of software products
based on various criteria such as lifecycle status, vendor information,
and classification status.
"""

import pandas as pd
from typing import Dict, Any

import config

def flag_risk(row: pd.Series) -> str:
    """
    Determine the risk level for a software product.
    
    Args:
        row: A pandas Series representing a row in the software dataframe
        
    Returns:
        Risk flag as a string: "High-Risk", "Medium-Risk", or "Normal"
    """
    # High risk: Deprecated software
    if 'Lifecycle Status' in row and row['Lifecycle Status'].lower() == 'deprecated':
        return "High-Risk"
    
    # High risk: Missing vendor information
    elif 'Vendor' in row and (pd.isnull(row['Vendor']) or row['Vendor'].strip() == ''):
        return "High-Risk"
    
    # High risk: Unclassified software
    elif 'TRM Domain' in row and row['TRM Domain'] == config.DEFAULT_DOMAIN:
        return "High-Risk"
    
    # Medium risk: Beta software
    elif 'Lifecycle Status' in row and row['Lifecycle Status'].lower() == 'beta':
        return "Medium-Risk"
    
    # Normal risk: All other cases
    return config.DEFAULT_RISK_FLAG

def generate_risk_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate risk metrics from the software dataframe.
    
    Args:
        df: Pandas DataFrame containing software data with risk flags
        
    Returns:
        Dictionary of risk metrics
    """
    # Count products by risk level
    risk_counts = df['Risk Flag'].value_counts().to_dict() if 'Risk Flag' in df.columns else {}
    
    # Calculate percentages
    total = len(df)
    risk_percentages = {k: round(v/total*100, 1) for k, v in risk_counts.items()}
    
    # Get deprecated software counts
    deprecated_count = len(df[df['Lifecycle Status'] == 'Deprecated']) if 'Lifecycle Status' in df.columns else 0
    
    # Get missing vendor counts
    missing_vendor_count = len(df[df['Vendor'].isnull() | (df['Vendor'] == '')]) if 'Vendor' in df.columns else 0
    
    # Get unclassified counts
    unclassified_count = len(df[df['TRM Domain'] == config.DEFAULT_DOMAIN]) if 'TRM Domain' in df.columns else 0
    
    return {
        'counts': risk_counts,
        'percentages': risk_percentages,
        'deprecated_count': deprecated_count,
        'missing_vendor_count': missing_vendor_count,
        'unclassified_count': unclassified_count,
        'total': total
    }
'''

# UI components module (simplified version)
ui_components_content = '''"""
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
'''

# Write the files
with open('classification.py', 'w') as f:
    f.write(classification_content)

with open('config.py', 'w') as f:
    f.write(config_content)

with open('risk_assessment.py', 'w') as f:
    f.write(risk_assessment_content)

with open('ui_components.py', 'w') as f:
    f.write(ui_components_content)

print("All files created successfully!") 