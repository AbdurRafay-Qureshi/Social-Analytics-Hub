# main.py
# Multi-Platform Analytics Dashboard (YouTube + Reddit)
# Refactored to modular platform-based architecture

import streamlit as st

# Core utilities
from core.config import setup_page_config, apply_css

# UI layer
from ui.sidebar import render_sidebar
from ui.components import info_card, section

# Platform modules
from platforms.youtube import analyze_youtube_channel, render_dashboard as render_youtube_dashboard
from platforms.reddit import analyze_reddit, render_dashboard as render_reddit_dashboard

# Optional modules availability flags
try:
    from sentiment_analyzer import SentimentAnalyzer
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False

try:
    from platforms.youtube.predictive_analytics import PredictiveAnalytics
    PREDICTIVE_AVAILABLE = True
except ImportError:
    PREDICTIVE_AVAILABLE = False


# ==================== PAGE SETUP ====================
setup_page_config()
apply_css()


# ==================== SIDEBAR ====================
config = render_sidebar(SENTIMENT_AVAILABLE, VADER_AVAILABLE, PREDICTIVE_AVAILABLE)


# ==================== ANALYZE ACTION - PLATFORM-AWARE ====================
if config["analyze_clicked"]:
    if config["platform"] == "youtube":
        analyze_youtube_channel(config)
    elif config["platform"] == "reddit":
        analyze_reddit(config)


# ==================== DISPLAY: YOUTUBE ====================
if "channel_stats" in st.session_state and st.session_state.get("platform") == "youtube":
    render_youtube_dashboard()


# ==================== DISPLAY: REDDIT ====================
elif "reddit_data" in st.session_state and st.session_state.get("platform") == "reddit":
    render_reddit_dashboard()


# ==================== DEFAULT VIEW ====================
else:
    section("Social Analytics Hub", "Multi-platform analytics for YouTube and Reddit")
    x1, x2, x3 = st.columns(3)
    with x1:
        info_card("🎥 YouTube", "Analyze channels with comprehensive metrics, insights, and performance tracking.")
    with x2:
        info_card("🔴 Reddit", "Track subreddits and users with engagement analytics and posting patterns.")
    with x3:
        info_card("🚀 Get Started", "Select a platform from the sidebar and enter an identifier to begin analysis.")
