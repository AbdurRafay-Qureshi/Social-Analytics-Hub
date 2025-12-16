# platforms/youtube/views/header.py
"""
YouTube Dashboard Header Component.
"""

from ui.components import section


def render_header(stats):
    """
    Render YouTube dashboard header with channel name.
    
    Args:
        stats: Channel stats dict with 'channel_name' key
    """
    section(
        "YouTube Analytics Dashboard",
        f"Professional analytics for {stats['channel_name']}",
    )
