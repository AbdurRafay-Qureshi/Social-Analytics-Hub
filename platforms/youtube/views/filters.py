# platforms/youtube/views/filters.py
"""
YouTube Dashboard Filter Component.
Renders date and category filters.
"""

import streamlit as st


def render_filters(df_original):
    """
    Render date and category filter inputs.
    
    Args:
        df_original: Original unfiltered dataframe
    
    Returns:
        tuple: (start_date, end_date, category_filter)
    """
    d1, d2, d3, _ = st.columns([1, 1, 1, 2])
    
    with d1:
        start_date = st.date_input(
            "Start Date", 
            key="start_date", 
            value=df_original["upload_date"].min().date()
        )
    
    with d2:
        end_date = st.date_input(
            "End Date", 
            key="end_date", 
            value=df_original["upload_date"].max().date()
        )
    
    with d3:
        category_filter = st.selectbox(
            "Category", 
            ["All Categories", "Top Performing", "Recent"],
            key="category_filter"
        )
    
    return start_date, end_date, category_filter
