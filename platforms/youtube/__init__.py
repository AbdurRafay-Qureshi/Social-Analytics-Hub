# platforms/youtube/__init__.py
"""
YouTube Analytics Platform Module.
Handles YouTube channel analysis, data processing, and dashboard rendering.
"""

from .analyzer import analyze_youtube_channel
from .dashboard import render_dashboard

__all__ = [
    'analyze_youtube_channel',
    'render_dashboard',
]
