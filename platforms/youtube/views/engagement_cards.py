# platforms/youtube/views/engagement_cards.py
"""
YouTube Engagement Breakdown Cards Component.
Displays Views, Likes, and Comments cards with gradient styling.
"""

import streamlit as st
from ui.components import chart_card, end_card


def render_engagement_breakdown(calculated_stats):
    """
    Render engagement breakdown cards (Views, Likes, Comments).
    
    Args:
        calculated_stats: Dict with keys:
            - total_views_fetched
            - total_views_channel
            - total_likes_fetched
            - total_comments_fetched
    """
    cont = chart_card("Engagement Breakdown")
    with cont:
        total_engagement = calculated_stats['total_likes_fetched'] + calculated_stats['total_comments_fetched']
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #033E6B 0%, #0D2956 100%); border-radius: 10px; padding: 20px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(3,62,107,0.25);">
            <div style="color: rgba(255,255,255,0.9); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">👁️ VIEWS</div>
            <div style="color: white; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: 'Inter', sans-serif;">{calculated_stats['total_views_fetched']:,}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px;">{(calculated_stats['total_views_fetched'] / calculated_stats['total_views_channel'] * 100):.1f}% of channel total</div>
        </div>
        <div style="background: linear-gradient(135deg, #2587C8 0%, #156CA5 100%); border-radius: 10px; padding: 20px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(37,135,200,0.25);">
            <div style="color: rgba(255,255,255,0.9); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">👍 LIKES</div>
            <div style="color: white; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: 'Inter', sans-serif;">{calculated_stats['total_likes_fetched']:,}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px;">{(calculated_stats['total_likes_fetched'] / total_engagement * 100):.1f}% of engagement</div>
        </div>
        <div style="background: linear-gradient(135deg, #7CC0E0 0%, #B6DFF1 100%); border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(124,192,224,0.25);">
            <div style="color: rgba(255,255,255,0.9); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">💬 COMMENTS</div>
            <div style="color: white; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: 'Inter', sans-serif;">{calculated_stats['total_comments_fetched']:,}</div>
            <div style="color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px;">{(calculated_stats['total_comments_fetched'] / total_engagement * 100):.1f}% of engagement</div>
        </div>
        """, unsafe_allow_html=True)
    end_card()
