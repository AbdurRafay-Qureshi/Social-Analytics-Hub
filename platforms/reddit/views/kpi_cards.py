# platforms/reddit/views/kpi_cards.py
"""
Reddit KPI Cards Component.
Renders different KPI cards for subreddit vs user analysis.
"""

import streamlit as st
from ui.components import kpi


def render_kpi_cards(reddit_data, stats):
    """
    Render KPI cards (different for subreddit vs user).
    
    Args:
        reddit_data: Dict with 'type' key ('subreddit' or 'user')
        stats: Stats dict from Reddit API
    """
    if reddit_data['type'] == 'subreddit':
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            kpi("Members", f"{stats.get('members', 0):,}", "Total subscribers")
        with c2:
            kpi("Posts Analyzed", f"{stats.get('posts_analyzed', 0):,}", f"{stats.get('total_posts_fetched', 0)} fetched")
        with c3:
            kpi("Avg Upvotes", f"{stats.get('avg_upvotes', 0):,.1f}", "Per post")
        with c4:
            engagement_display = stats.get('total_engagement_rate', stats.get('avg_engagement_rate', 0))
            kpi("Community Engagement", f"{engagement_display:.2f}%", "Overall activity rate")
    
    else:  # User
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            kpi("Total Karma", f"{stats.get('total_karma', 0):,}", "Post + Comment")
        with c2:
            kpi("Posts", f"{stats.get('posts_analyzed', 0):,}", "Analyzed")
        with c3:
            kpi("Comments", f"{stats.get('comments_analyzed', 0):,}", "Analyzed")
        with c4:
            kpi("Avg Upvotes", f"{stats.get('avg_post_upvotes', 0):,.1f}", "Per post")
