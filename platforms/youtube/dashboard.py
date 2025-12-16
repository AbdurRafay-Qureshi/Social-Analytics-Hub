# platforms/youtube/dashboard.py
"""
YouTube Dashboard Orchestrator.
Coordinates all YouTube view components and handles the main dashboard flow.
"""

import streamlit as st
from tabs import render_top_videos_tab, render_upload_schedule_tab, render_insights_tab, render_predictions_tab
from .data_processor import apply_filters, calculate_stats
from .views import (
    render_header,
    render_filters,
    render_kpi_cards,
    render_performance_chart,
    render_engagement_breakdown,
    render_data_table_tab
)


def render_dashboard():
    """
    Render the complete YouTube analytics dashboard.
    
    Requires session state to contain:
        - channel_stats: Channel statistics from YouTube API
        - video_df: DataFrame with video data
    """
    stats = st.session_state.channel_stats
    df_original = st.session_state.video_df.copy()

    if stats is None or df_original is None:
        st.error("❌ Could not retrieve channel data")
        return

    # Header
    render_header(stats)

    # Filters
    start_date, end_date, category_filter = render_filters(df_original)
    
    # Apply filters to working dataframe
    df = apply_filters(df_original, start_date, end_date, category_filter)

    st.markdown("")

    # Calculate statistics
    calculated_stats = calculate_stats(df_original, stats)

    # KPIs
    render_kpi_cards(calculated_stats)

    st.markdown("")

    # Charts
    left, right = st.columns([1, 1])

    with left:
        render_performance_chart(df)

    with right:
        render_engagement_breakdown(calculated_stats)

    st.markdown("")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Top Videos", "Upload Schedule", "Insights", "Predictions", "Data Table"])

    with tab1:
        render_top_videos_tab(df)

    with tab2:
        render_upload_schedule_tab(df)

    with tab3:
        render_insights_tab(df, stats)
    
    with tab4:
        render_predictions_tab(df, stats)

    with tab5:
        render_data_table_tab(df, stats)
