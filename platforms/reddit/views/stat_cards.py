# platforms/reddit/views/stat_cards.py
"""
Reddit Stat Cards Component.
Renders 6 gradient stat cards (3 orange + 3 blue).
"""

import streamlit as st
import pandas as pd


def render_stat_cards(posts_df):
    """
    Render 6 gradient stat cards.
    
    Args:
        posts_df: DataFrame with posts data
    """
    if posts_df.empty:
        return
    
    # Calculate stats
    total_upvotes = int(posts_df['upvotes'].sum())
    total_comments = int(posts_df['num_comments'].sum())
    avg_upvotes = round(posts_df['upvotes'].mean(), 1)
    avg_comments = round(posts_df['num_comments'].mean(), 1)
    top_post_upvotes = int(posts_df['upvotes'].max())
    
    # TOP ROW: 3 Orange Gradient Cards (Dark to Light)
    top_row = st.columns(3)
    
    with top_row[0]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #C1440E 0%, #FF4500 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(193,68,14,0.3);">
            <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">⬆️ TOTAL UPVOTES</div>
            <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{total_upvotes:,}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Across {len(posts_df)} posts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with top_row[1]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E25822 0%, #FF6B3D 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(226,88,34,0.3);">
            <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📊 AVG UPVOTES</div>
            <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{avg_upvotes:,.1f}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Per post average</div>
        </div>
        """, unsafe_allow_html=True)
    
    with top_row[2]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF7F50 0%, #FFA07A 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(255,127,80,0.3);">
            <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">🔥 TOP POST</div>
            <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{top_post_upvotes:,}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Highest upvotes</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    
    # BOTTOM ROW: 3 Blue Gradient Cards (Dark to Light)
    bottom_row = st.columns(3)
    
    with bottom_row[0]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(12,74,110,0.3);">
            <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">💬 TOTAL COMMENTS</div>
            <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{total_comments:,}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Community discussions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with bottom_row[1]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(2,132,199,0.3);">
            <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📝 AVG COMMENTS</div>
            <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{avg_comments:,.1f}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Per post average</div>
        </div>
        """, unsafe_allow_html=True)
    
    with bottom_row[2]:
        # Calculate posts per day
        if 'created_utc' in posts_df.columns:
            posts_df_copy = posts_df.copy()
            posts_df_copy['created_date'] = pd.to_datetime(posts_df_copy['created_utc'], unit='s', errors='coerce')
            date_range = (posts_df_copy['created_date'].max() - posts_df_copy['created_date'].min()).days
            posts_per_day = round(len(posts_df_copy) / max(date_range, 1), 1)
        else:
            posts_per_day = 0
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #38BDF8 0%, #7DD3FC 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(56,189,248,0.3);">
            <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📅 POSTS PER DAY</div>
            <div style="color: white; font-size: 40px; font-weight: 700; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{posts_per_day}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Community activity level</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 24px 0;'></div>", unsafe_allow_html=True)
