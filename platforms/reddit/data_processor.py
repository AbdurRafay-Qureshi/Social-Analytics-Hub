# platforms/reddit/data_processor.py
"""
Reddit Data Processing Module.
Handles column mapping, data validation, and transformations.
"""

import pandas as pd


def preprocess_reddit_data(reddit_data):
    """
    Clean and validate Reddit data.
    
    Args:
        reddit_data: Dict with 'posts' key containing DataFrame
    
    Returns:
        pd.DataFrame: Cleaned posts dataframe
    """
    posts_df = reddit_data['posts'].copy()
    
    # Map Reddit API column names to our expected names
    column_mapping = {
        'score': 'upvotes',
        'comments': 'num_comments'
    }
    
    for old_name, new_name in column_mapping.items():
        if old_name in posts_df.columns and new_name not in posts_df.columns:
            posts_df[new_name] = posts_df[old_name]
    
    # Ensure ALL required columns exist with safe defaults
    default_values = {
        'title': 'No Title',
        'author': 'Unknown',
        'upvotes': 0,
        'num_comments': 0,
        'engagement_rate': 0.0,
        'subreddit': 'Unknown',
        'created_utc': 0
    }
    
    for col, default in default_values.items():
        if col not in posts_df.columns:
            posts_df[col] = default
    
    return posts_df
