# platforms/reddit/dashboard.py
"""
Reddit Dashboard Orchestrator.
Coordinates all Reddit view components and handles the main dashboard flow.
"""

import streamlit as st
from .data_processor import preprocess_reddit_data
from .views import (
    render_header,
    render_kpi_cards,
    render_stat_cards,
    render_top_posts_chart,
    render_reddit_tabs
)


def render_dashboard():
    """
    Render the complete Reddit analytics dashboard.
    
    Requires session state to contain:
        - reddit_data: Reddit data with 'type', 'name', 'stats', 'posts' keys
    """
    reddit_data = st.session_state.reddit_data
    stats = reddit_data['stats']
    
    # Preprocess data
    posts_df = preprocess_reddit_data(reddit_data)
    
    # Header
    render_header(reddit_data)
    
    st.markdown("")
    
    # KPIs
    render_kpi_cards(reddit_data, stats)
    
    st.markdown("")
    
    # Stat cards and chart
    render_stat_cards(posts_df)
    render_top_posts_chart(posts_df)
    
    st.markdown("")
    
    # Tabs
    render_reddit_tabs(posts_df, reddit_data, stats)
