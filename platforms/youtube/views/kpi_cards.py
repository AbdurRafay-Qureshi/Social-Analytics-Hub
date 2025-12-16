# platforms/youtube/views/kpi_cards.py
"""
YouTube KPI Cards Component.
Renders the 4 main KPI cards at the top of the dashboard.
"""

import streamlit as st
from ui.components import kpi
from core.formatters import format_subscribers


def render_kpi_cards(calculated_stats):
    """
    Render 4 KPI cards in columns.
    
    Args:
        calculated_stats: Dict with keys:
            - total_subscribers
            - total_views_channel
            - total_videos_channel
            - fetched_count
            - engagement_rate_calculated
    """
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        kpi(
            "Subscribers", 
            format_subscribers(calculated_stats['total_subscribers']), 
            "Official count"
        )
    
    with c2:
        kpi(
            "Total Views", 
            f"{calculated_stats['total_views_channel']:,}", 
            "Official channel total"
        )
    
    with c3:
        kpi(
            "Total Videos", 
            f"{calculated_stats['total_videos_channel']:,}", 
            f"{calculated_stats['fetched_count']} analyzed"
        )
    
    with c4:
        kpi(
            "Engagement Rate", 
            f"{calculated_stats['engagement_rate_calculated']:.2f}%", 
            f"From {calculated_stats['fetched_count']} videos"
        )
