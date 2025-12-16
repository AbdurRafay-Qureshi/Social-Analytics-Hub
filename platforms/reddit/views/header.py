# platforms/reddit/views/header.py
"""
Reddit Dashboard Header Component.
"""

from ui.components import section


def render_header(reddit_data):
    """
    Render Reddit dashboard header.
    
    Args:
        reddit_data: Dict with 'type' ('subreddit' or 'user') and 'name' keys
    """
    if reddit_data['type'] == 'subreddit':
        title_text = f"Professional analytics for {reddit_data['type']}: r/{reddit_data['name']}"
    else:
        title_text = f"Professional analytics for user: u/{reddit_data['name']}"
    
    section("Reddit Analytics Dashboard", title_text)
