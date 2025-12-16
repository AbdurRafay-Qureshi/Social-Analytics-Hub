# platforms/youtube/views/performance_chart.py
"""
YouTube Performance Over Time Chart Component.
"""

import streamlit as st
import plotly.graph_objects as go
from ui.components import chart_card, end_card
from ui.styles import plotly_layout
from core.formatters import seconds_to_hms


def render_performance_chart(df):
    """
    Render the Performance Over Time line chart.
    
    Args:
        df: Filtered dataframe with video data
    """
    cont = chart_card("Performance Over Time")
    with cont:
        dsort = df.sort_values("upload_date")
        
        # Prepare formatted columns
        dsort_copy = dsort.copy()
        dsort_copy["formatted_date"] = dsort_copy["upload_date"].dt.strftime("%b %d, %Y")
        dsort_copy["formatted_duration"] = dsort_copy["duration_seconds"].apply(seconds_to_hms)
        
        # Build hover text
        hover_text = []
        for idx, row in dsort_copy.iterrows():
            hover_text.append(
                f"<b>{row['title'][:60]}...</b><br>" +
                f"<br>📅 Date: {row['formatted_date']}<br>" +
                f"👁️ Views: {row['view_count']:,}<br>" +
                f"👍 Likes: {row['like_count']:,}<br>" +
                f"💬 Comments: {row['comment_count']:,}<br>" +
                f"📊 Engagement: {row['engagement_rate']:.2f}%<br>" +
                f"⏱️ Duration: {row['formatted_duration']}"
            )
        
        # Create figure
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dsort_copy["upload_date"],
                y=dsort_copy["view_count"],
                mode="lines+markers",
                name="Views",
                line=dict(color="#2563EB", width=2.5),
                marker=dict(size=6, color="#2563EB"),
                text=hover_text,
                hovertemplate='%{text}<extra></extra>',
            )
        )
        fig.update_layout(**plotly_layout(), height=400, hovermode='closest')
        st.plotly_chart(fig, use_container_width=True, key="chart_trend")
    end_card()
