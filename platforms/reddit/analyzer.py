# platforms/reddit/analyzer.py
"""
Reddit Analysis Handler.
Handles API calls, data fetching, quota management, and session state updates.
"""

import streamlit as st


def analyze_reddit(config):
    """
    Handle Reddit analysis workflow.
    
    Args:
        config: Configuration dict from sidebar with keys:
            - identifier: Subreddit name or username
            - identifier_type: 'subreddit' or 'user'
            - post_limit: Number of posts to fetch
    
    Returns:
        None. Updates st.session_state with reddit_data.
    """
    # Check if quota manager is available
    try:
        from config.quota_manager import quota_manager
        QUOTA_ENABLED = True
    except ImportError:
        QUOTA_ENABLED = False
    
    # Validate input
    if not config["identifier"]:
        st.error("⚠️ Please enter a subreddit or username")
        return
    
    # Check quota
    if QUOTA_ENABLED and not quota_manager.can_make_request("reddit"):
        st.error("❌ Daily quota limit reached! Please try again tomorrow.")
        st.info("💡 Tip: The quota resets at midnight UTC (5:00 AM PKT)")
        return
    
    try:
        with st.spinner(f"🔄 Analyzing Reddit {config['identifier_type']}..."):
            # Get credentials from secrets
            client_id = st.secrets["reddit"]["client_id"]
            client_secret = st.secrets["reddit"]["client_secret"]
            user_agent = st.secrets["reddit"]["user_agent"]
            
            # Import reddit analyzer
            from .api_client import RedditAnalyser
            
            # Create analyzer
            reddit_analyzer = RedditAnalyser(client_id, client_secret, user_agent)
            
            # Analyze based on type
            if config["identifier_type"] == "subreddit":
                reddit_data = reddit_analyzer.analyze_subreddit(
                    config["identifier"],
                    limit=config["post_limit"]
                )
            else:
                reddit_data = reddit_analyzer.analyze_user(
                    config["identifier"],
                    limit=config["post_limit"]
                )
            
            # Increment quota
            if QUOTA_ENABLED:
                quota_manager.increment_usage("reddit")
            
            # Store in session state
            st.session_state.reddit_data = reddit_data
            st.session_state.platform = "reddit"
            
            st.success(f"✅ {config['identifier_type'].title()} analyzed successfully!")
            st.rerun()
    
    except ImportError:
        st.error("❌ Reddit module not found. Please ensure reddit.py exists.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)
