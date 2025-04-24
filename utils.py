"""
Utility functions for the TRM Modernization application.

This module provides general utility functions used throughout the application.
"""

import pandas as pd
import numpy as np
import json
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

def is_api_key_configured(api_key: Optional[str]) -> bool:
    """
    Check if an API key is configured.
    
    Args:
        api_key: API key to check
        
    Returns:
        True if the API key is configured, False otherwise
    """
    return api_key is not None and len(str(api_key).strip()) > 0

def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format a timestamp for display or filenames.
    
    Args:
        dt: Datetime object (defaults to current time)
        
    Returns:
        Formatted timestamp string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y%m%d_%H%M%S")

def create_download_link(df: pd.DataFrame, filename: str, link_text: str) -> str:
    """
    Creates a download link for a DataFrame.
    
    Args:
        df: DataFrame to create a download link for
        filename: Name of the file to download
        link_text: Text to display for the link
        
    Returns:
        HTML link to download the file
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def json_serializer(obj: Any) -> Union[str, int, float, bool, List, Dict]:
    """
    JSON serializer for objects not serializable by default json code.
    
    Args:
        obj: Object to serialize
        
    Returns:
        JSON-serializable representation of the object
    """
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, datetime):
        return obj.isoformat()
    if pd.isna(obj):
        return None
    raise TypeError(f"Type {type(obj)} not serializable")

def serialize_dataframe(df: pd.DataFrame, format_type: str = 'json') -> str:
    """
    Serialize a DataFrame to a string in various formats.
    
    Args:
        df: DataFrame to serialize
        format_type: Format type ('json' or 'csv')
        
    Returns:
        Serialized string representation of the DataFrame
    """
    if format_type == 'json':
        return df.to_json(orient='records', date_format='iso')
    elif format_type == 'csv':
        return df.to_csv(index=False)
    else:
        raise ValueError(f"Unsupported format type: {format_type}")

def generate_html_report(df: pd.DataFrame, metrics: Dict[str, Any]) -> str:
    """
    Generate an HTML report from DataFrame and metrics.
    
    Args:
        df: DataFrame with classification data
        metrics: Dictionary of metrics
        
    Returns:
        HTML string with report
    """
    # Get timestamp
    timestamp = format_timestamp()
    
    # Start HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TRM Classification Report - {timestamp}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2C3E50; }}
            .metrics {{ display: flex; margin-bottom: 20px; }}
            .metric-card {{ background-color: #f5f5f5; padding: 15px; margin-right: 15px; border-radius: 5px; }}
            .high-risk {{ background-color: #FFCCCC; }}
            .medium-risk {{ background-color: #FFFFCC; }}
            .normal-risk {{ background-color: #CCFFCC; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>TRM Classification Report</h1>
        <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <h2>Risk Metrics</h2>
        <div class="metrics">
    """
    
    # Add metrics
    risk_counts = metrics.get('counts', {})
    
    html += f"""
            <div class="metric-card">
                <h3>Total Products</h3>
                <p>{metrics.get('total', 0)}</p>
            </div>
    """
    
    # Add risk level metrics
    for risk_level in ['High-Risk', 'Medium-Risk', 'Normal']:
        count = risk_counts.get(risk_level, 0)
        percentage = metrics.get('percentages', {}).get(risk_level, 0)
        
        risk_class = risk_level.lower().replace('-', '-') + '-risk'
        
        html += f"""
            <div class="metric-card {risk_class}">
                <h3>{risk_level}</h3>
                <p>{count} ({percentage}%)</p>
            </div>
        """
    
    html += """
        </div>
        
        <h2>Classification Results</h2>
        <table>
            <tr>
                <th>Product Name</th>
                <th>Description</th>
                <th>Vendor</th>
                <th>Lifecycle Status</th>
                <th>TRM Domain</th>
                <th>TRM Subdomain</th>
                <th>Risk Flag</th>
            </tr>
    """
    
    # Add table rows
    for _, row in df.iterrows():
        risk_class = row.get('Risk Flag', '').lower().replace('-', '-') + '-risk'
        
        html += f"""
            <tr class="{risk_class}">
                <td>{row.get('Product Name', '')}</td>
                <td>{row.get('Description', '')}</td>
                <td>{row.get('Vendor', '')}</td>
                <td>{row.get('Lifecycle Status', '')}</td>
                <td>{row.get('TRM Domain', '')}</td>
                <td>{row.get('TRM Subdomain', '')}</td>
                <td>{row.get('Risk Flag', '')}</td>
            </tr>
        """
    
    # Close HTML
    html += """
        </table>
    </body>
    </html>
    """
    
    return html