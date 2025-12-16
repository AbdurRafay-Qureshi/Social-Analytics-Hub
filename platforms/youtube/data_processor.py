# platforms/youtube/data_processor.py
"""
YouTube Data Processing Module.
Handles filtering, statistics calculation, and data transformations.
"""

import pandas as pd
import streamlit as st
from .engagement_calculator import EngagementCalculator


def apply_filters(df_original, start_date, end_date, category_filter):
    """
    Apply date and category filters to dataframe.
    
    Args:
        df_original: Original unfiltered dataframe
        start_date: Start date for filtering
        end_date: End date for filtering
        category_filter: Category filter ("All Categories", "Top Performing", "Recent")
    
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df = df_original.copy()
    
    # Date filter
    if start_date and end_date:
        df = df[
            (df["upload_date"].dt.date >= start_date) & 
            (df["upload_date"].dt.date <= end_date)
        ]
    
    # Category filter
    if category_filter == "Top Performing":
        threshold = df["view_count"].quantile(0.75)
        df = df[df["view_count"] >= threshold]
    elif category_filter == "Recent":
        recent_date = df["upload_date"].max() - pd.Timedelta(days=30)
        df = df[df["upload_date"] >= recent_date]
    
    return df


def calculate_stats(df_original, stats):
    """
    Calculate comprehensive statistics from YouTube data.
    
    Args:
        df_original: Original dataframe with video data
        stats: Channel stats dict from YouTube API
    
    Returns:
        dict: Calculated statistics with keys:
            - total_videos_channel: Total videos on channel (from API)
            - total_views_channel: Total views on channel (from API)
            - total_subscribers: Total subscribers (from API)
            - total_likes_fetched: Total likes from fetched videos
            - total_comments_fetched: Total comments from fetched videos
            - total_views_fetched: Total views from fetched videos
            - fetched_count: Number of videos fetched
            - engagement_rate_calculated: Calculated engagement rate
            - engagement_comparison: 30-day engagement comparison
            - coverage_percent: Percentage of channel videos analyzed
    """
    # Get ACTUAL channel stats from YouTube API
    total_videos_channel = stats['total_videos']
    total_views_channel = stats['total_views']
    total_subscribers = stats['total_subscribers']
    
    # Calculate stats from FETCHED videos only
    total_likes_fetched = df_original['like_count'].sum()
    total_comments_fetched = df_original['comment_count'].sum()
    total_views_fetched = df_original['view_count'].sum()
    fetched_count = len(df_original)
    
    # Calculate engagement rate
    if total_views_channel > 0:
        engagement_rate_calculated = ((total_likes_fetched + total_comments_fetched) / total_views_channel) * 100
    else:
        engagement_rate_calculated = 0.0
    
    # Get 30-day comparison
    eng_calc = EngagementCalculator(df_original)
    engagement_comparison = eng_calc.get_engagement_comparison()
    
    # Calculate coverage
    coverage_percent = (fetched_count / total_videos_channel * 100) if total_videos_channel > 0 else 0
    
    # Show warning if coverage is low
    if coverage_percent < 95:
        st.warning(f"⚠️ Showing data for {fetched_count} of {total_videos_channel} videos ({coverage_percent:.1f}% coverage).")
    
    return {
        'total_videos_channel': total_videos_channel,
        'total_views_channel': total_views_channel,
        'total_subscribers': total_subscribers,
        'total_likes_fetched': total_likes_fetched,
        'total_comments_fetched': total_comments_fetched,
        'total_views_fetched': total_views_fetched,
        'fetched_count': fetched_count,
        'engagement_rate_calculated': engagement_rate_calculated,
        'engagement_comparison': engagement_comparison,
        'coverage_percent': coverage_percent
    }
