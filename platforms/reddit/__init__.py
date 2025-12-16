# platforms/reddit/__init__.py
"""
Reddit Analytics Platform Module.
Handles Reddit subreddit/user analysis, data processing, and dashboard rendering.
"""

from .analyzer import analyze_reddit
from .dashboard import render_dashboard

__all__ = [
    'analyze_reddit',
    'render_dashboard',
]
