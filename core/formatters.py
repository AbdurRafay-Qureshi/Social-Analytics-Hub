# core/formatters.py
"""
Core utility functions for formatting numbers, subscribers, and time durations.
These are shared across all platform modules.
"""


def format_large_number(num):
    """
    Format large numbers with K/M suffix.
    
    Args:
        num: Number to format
        
    Returns:
        str: Formatted number (e.g., "1.5M", "500K", "1,234")
    """
    if num is None:
        return "N/A"
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return f"{num:,}"


def format_subscribers(num):
    """
    Format subscriber count with K/M suffix.
    
    Args:
        num: Subscriber count
        
    Returns:
        str: Formatted subscriber count (e.g., "1.5M", "500K", "1,234")
    """
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.0f}K"
    else:
        return f"{num:,}"


def seconds_to_hms(seconds):
    """
    Convert seconds to HH:MM:SS format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted time (e.g., "01:23:45")
    """
    if seconds is None:
        return "N/A"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
