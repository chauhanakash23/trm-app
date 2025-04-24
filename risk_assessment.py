"""
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
