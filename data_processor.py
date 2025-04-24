"""
Data processing and handling for the TRM Modernization application.

This module provides functions to load, clean, preprocess, and filter
software data for the application.
"""

import pandas as pd
import numpy as np
import streamlit as st
import io
from typing import Optional, Dict, List, Any, Union

import config

def load_data(file_path: Optional[str] = None, uploaded_file: Optional[Any] = None) -> pd.DataFrame:
    """
    Load software data from the CSV file.
    
    Args:
        file_path: Path to the CSV file. If None, uses the default path
                  from config.
        uploaded_file: Streamlit UploadedFile object. If provided, this takes
                      precedence over file_path.
        
    Returns:
        Pandas DataFrame containing the software data
    """
    try:
        # Load data from uploaded file if provided
        if uploaded_file is not None:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file)
        else:
            # Use default path if not specified
            if file_path is None:
                file_path = config.DATA_FILE_PATH
                
            # Load the data from file path
            df = pd.read_csv(file_path)
        
        # Clean the data
        df = clean_data(df)
        
        return df
    except FileNotFoundError:
        st.error(f"Data file not found at {file_path}. Please ensure the file exists.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the software data.
    
    Args:
        df: Raw pandas DataFrame
        
    Returns:
        Cleaned pandas DataFrame
    """
    # Create a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # 1. Handle missing values
    # Fill missing descriptions with empty string
    cleaned_df['Description'] = cleaned_df['Description'].fillna('')
    
    # Fill missing category hints with empty string
    cleaned_df['Category Hint'] = cleaned_df['Category Hint'].fillna('')
    
    # Keep vendor as null if missing (used in risk assessment)
    
    # 2. Standardize text fields
    # Standardize product names (trim whitespace)
    cleaned_df['Product Name'] = cleaned_df['Product Name'].str.strip()
    
    # 3. Standardize lifecycle status
    # Make sure status is capitalized properly
    status_mapping = {
        'active': 'Active',
        'deprecated': 'Deprecated',
        'beta': 'Beta',
        'planned': 'Planned'
    }
    
    # Map known status values to standard format, defaulting to 'Active' for unknown values
    if 'Lifecycle Status' in cleaned_df.columns:
        cleaned_df['Lifecycle Status'] = cleaned_df['Lifecycle Status'].str.lower().map(
            lambda x: status_mapping.get(x, 'Active') if pd.notnull(x) else 'Active'
        )
    
    # 4. Add empty columns for classification results if they don't exist
    for col in ['TRM Domain', 'TRM Subdomain', 'Risk Flag']:
        if col not in cleaned_df.columns:
            cleaned_df[col] = np.nan
    
    return cleaned_df

def filter_data(
    df: pd.DataFrame, 
    search_term: Optional[str] = None,
    domain: Optional[str] = None,
    status: Optional[str] = None,
    risk_level: Optional[str] = None
) -> pd.DataFrame:
    """
    Filter the software data based on various criteria.
    
    Args:
        df: DataFrame containing software data
        search_term: Text to search for in product names and descriptions
        domain: TRM Domain to filter by
        status: Lifecycle Status to filter by
        risk_level: Risk Flag to filter by
        
    Returns:
        Filtered pandas DataFrame
    """
    # Create a copy to avoid modifying the original
    filtered_df = df.copy()
    
    # Apply search term filter (case-insensitive)
    if search_term and len(search_term.strip()) > 0:
        search_term = search_term.strip().lower()
        filtered_df = filtered_df[
            filtered_df['Product Name'].str.lower().str.contains(search_term) |
            filtered_df['Description'].str.lower().str.contains(search_term)
        ]
    
    # Apply domain filter
    if domain and domain != config.UI_SELECT_ALL:
        filtered_df = filtered_df[filtered_df['TRM Domain'] == domain]
    
    # Apply status filter
    if status and status != config.UI_SELECT_ALL:
        filtered_df = filtered_df[filtered_df['Lifecycle Status'] == status]
    
    # Apply risk level filter
    if risk_level and risk_level != config.UI_SELECT_ALL:
        filtered_df = filtered_df[filtered_df['Risk Flag'] == risk_level]
    
    return filtered_df

def get_unique_values(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Get unique values for various fields for filter dropdowns.
    
    Args:
        df: DataFrame containing software data
        
    Returns:
        Dictionary mapping column names to lists of unique values
    """
    unique_values = {}
    
    # Add "All" option to each list
    for column in ['TRM Domain', 'Lifecycle Status', 'Risk Flag']:
        if column in df.columns:
            values = sorted(df[column].dropna().unique().tolist())
            unique_values[column] = [config.UI_SELECT_ALL] + values
    
    return unique_values

def generate_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate statistics and metrics from the software dataframe.
    
    Args:
        df: Pandas DataFrame containing software data
        
    Returns:
        Dictionary of statistics and metrics
    """
    stats = {}
    
    # Basic metrics
    stats['total_products'] = len(df)
    stats['unique_vendors'] = df['Vendor'].nunique()
    
    # Domain distribution
    if 'TRM Domain' in df.columns:
        domain_counts = df['TRM Domain'].value_counts().to_dict()
        stats['domain_counts'] = domain_counts
        
        # Calculate percentages
        stats['domain_percentages'] = {
            domain: round(count / stats['total_products'] * 100, 1)
            for domain, count in domain_counts.items()
        }
    
    # Lifecycle status distribution
    if 'Lifecycle Status' in df.columns:
        stats['status_counts'] = df['Lifecycle Status'].value_counts().to_dict()
    
    # Risk distribution
    if 'Risk Flag' in df.columns:
        stats['risk_counts'] = df['Risk Flag'].value_counts().to_dict()
        
        # Calculate risk percentages
        stats['risk_percentages'] = {
            risk: round(count / stats['total_products'] * 100, 1)
            for risk, count in stats['risk_counts'].items()
        }
    
    return stats

def export_data(df: pd.DataFrame, format_type: str = 'csv') -> Dict[str, Any]:
    """
    Export the DataFrame to different formats.
    
    Args:
        df: DataFrame to export
        format_type: Export format ('csv', 'json', 'excel')
        
    Returns:
        Dictionary with format info, mimetype, and data
    """
    result = {
        'format': format_type,
        'success': True,
        'error': None
    }
    
    try:
        if format_type == 'csv':
            result['data'] = df.to_csv(index=False)
            result['mimetype'] = 'text/csv'
            result['filename'] = 'trm_data.csv'
        elif format_type == 'json':
            result['data'] = df.to_json(orient='records')
            result['mimetype'] = 'application/json'
            result['filename'] = 'trm_data.json'
        elif format_type == 'excel':
            # For Excel, we need to use BytesIO to handle binary data
            # This is a placeholder - would need to be implemented if Excel export is needed
            result['success'] = False
            result['error'] = "Excel export not implemented yet"
        else:
            result['success'] = False
            result['error'] = f"Unsupported export format: {format_type}"
    except Exception as e:
        result['success'] = False
        result['error'] = str(e)
    
    return result