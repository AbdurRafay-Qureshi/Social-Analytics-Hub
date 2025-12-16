# platforms/youtube/analyzer.py
"""
YouTube Channel Analysis Handler.
Handles API calls, data fetching, quota management, and session state updates.
"""

import streamlit as st
from .api_client import YouTubeChannelAnalyser


def analyze_youtube_channel(config):
    """
    Handle YouTube channel analysis workflow.
    
    Args:
        config: Configuration dict from sidebar with keys:
            - channel_input: Channel ID/URL/username
            - fetch_comments: Whether to fetch comments
            - max_comments: Max comments per video
            - num_videos_for_comments: Number of videos to fetch comments from
            - enable_predictions: Whether to enable predictions
    
    Returns:
        None. Updates st.session_state with channel_stats and video_df.
    """
    # Check if quota manager is available
    try:
        from config.quota_manager import quota_manager
        QUOTA_ENABLED = True
    except ImportError:
        QUOTA_ENABLED = False
    
    # Validate input
    if not config["channel_input"]:
        st.error("⚠️ Please enter channel identifier")
        return
    
    # Check quota
    if QUOTA_ENABLED and not quota_manager.can_make_request("youtube"):
        st.error("❌ Daily quota limit reached! Please try again tomorrow.")
        st.info("💡 Tip: The quota resets at midnight UTC (5:00 AM PKT)")
        return
    
    try:
        with st.spinner("🔄 Analyzing YouTube channel..."):
            # Get API key from secrets
            api_key = st.secrets["youtube"]["api_key"]
            
            # Create analyzer
            analyzer = YouTubeChannelAnalyser(api_key=api_key)
            
            # Fetch data
            st.session_state.channel_stats, st.session_state.video_df = analyzer.get_channel_data(
                config["channel_input"]
            )
            
            # Increment quota
            if QUOTA_ENABLED:
                quota_manager.increment_usage("youtube")
            
            # Store in session state
            st.session_state.analyzer = analyzer
            st.session_state.fetch_comments = config["fetch_comments"]
            st.session_state.max_comments = config["max_comments"]
            st.session_state.num_videos_for_comments = config["num_videos_for_comments"]
            st.session_state.enable_predictions = config["enable_predictions"]
            st.session_state.platform = "youtube"
            
            st.success("✅ Channel analyzed successfully!")
            st.rerun()
    
    except Exception as e:
        st.session_state.clear()
        st.error(f"❌ Error: {str(e)}")
