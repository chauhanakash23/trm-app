"""
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
COMPLEX_DATA_FILE_PATH = "data/complex_software_list.csv"

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