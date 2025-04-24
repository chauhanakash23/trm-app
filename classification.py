"""
Classification services for software products.

This module provides functions to classify software products into
appropriate TRM Domains and Subdomains using either rule-based or
LLM-based classification methods.
"""

import openai
import streamlit as st
from typing import Tuple, Dict, List, Optional

import config

# Available classification methods
AVAILABLE_METHODS = ["rule-based", "llm-based"]
DEFAULT_METHODS = ["rule-based"]

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
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    
    # Construct a prompt that includes valid domains and subdomains
    domains_text = "\n".join([
        f"{i+1}. {domain} - {', '.join(subdomains)}"
        for i, (domain, subdomains) in enumerate(config.TRM_DOMAINS_SUBDOMAINS.items())
        if domain != config.DEFAULT_DOMAIN  # Exclude unclassified from prompt options
    ])
    
    prompt = (
        f"Classify the software product '{product_name}' described as '{description}' "
        f"with hint '{hint}' into one of these TRM Domains and Subdomains:\n"
        f"{domains_text}\n"
        f"If uncertain, return 'Unclassified'.\n\n"
        f"Return your answer in 'Domain, Subdomain' format only."
    )
    
    try:
        # Use the new OpenAI API format
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.OPENAI_TEMPERATURE
        )
        classification = response.choices[0].message.content
        
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

def classify_software(df, method: str = "rule-based") -> Dict[str, List[Tuple[str, str]]]:
    """
    Classify all software in the DataFrame.
    
    Args:
        df: DataFrame containing software data
        method: Classification method ("rule-based" or "llm-based")
        
    Returns:
        Dictionary with classification results and statistics
    """
    results = {
        'classifications': [],
        'domain_counts': {},
        'unclassified_count': 0
    }
    
    # Choose the classification function based on method
    classify_func = rule_based_classify if method == "rule-based" else llm_classify
    
    # Process each row
    for _, row in df.iterrows():
        product_name = row['Product Name']
        description = row['Description']
        hint = row['Category Hint'] if 'Category Hint' in row else ""
        
        # Classify the software
        if method == "rule-based":
            domain, subdomain = classify_func(description, hint)
        else:
            domain, subdomain = classify_func(product_name, description, hint)
        
        # Store the classification
        results['classifications'].append((domain, subdomain))
        
        # Update statistics
        if domain in results['domain_counts']:
            results['domain_counts'][domain] += 1
        else:
            results['domain_counts'][domain] = 1
            
        if domain == config.DEFAULT_DOMAIN:
            results['unclassified_count'] += 1
    
    return results

def run_classification(df, method: str = "rule-based"):
    """
    Run classification on the dataframe and update it with results.
    
    Args:
        df: DataFrame containing software data
        method: Classification method ("rule-based" or "llm-based")
        
    Returns:
        Updated DataFrame with classification results
    """
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    
    # Process each row
    for idx, row in result_df.iterrows():
        product_name = row['Product Name']
        description = row['Description']
        hint = row['Category Hint'] if 'Category Hint' in row else ""
        
        # Classify the software
        if method == "rule-based":
            domain, subdomain = rule_based_classify(description, hint)
        else:
            domain, subdomain = llm_classify(product_name, description, hint)
        
        # Update the dataframe with classification results
        result_df.at[idx, 'TRM Domain'] = domain
        result_df.at[idx, 'TRM Subdomain'] = subdomain
    
    return result_df
