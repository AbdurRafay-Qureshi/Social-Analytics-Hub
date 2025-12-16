# platforms/reddit/views/top_posts_chart.py
"""
Reddit Top Posts Chart Component.
"""

import streamlit as st
import plotly.graph_objects as go
from ui.components import chart_card, end_card
from ui.styles import plotly_layout


def render_top_posts_chart(posts_df):
    """
    Render Top 20 Posts by Upvotes chart.
    
    Args:
        posts_df: DataFrame with posts data
    """
    cont = chart_card("Top 20 Posts by Upvotes")
    with cont:
        top_posts = posts_df.nlargest(20, 'upvotes')
        
        # Create color scale based on comments (engagement indicator)
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_posts['title'],
            x=top_posts['upvotes'],
            orientation='h',
            marker=dict(
                color=top_posts['num_comments'],
                colorscale='Oranges',
                showscale=True,
                colorbar=dict(
                    title="Comments",
                    thickness=15,
                    len=0.7
                ),
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            hovertemplate='<b>%{y}</b><br>' +
                          'Upvotes: %{x:,}<br>' +
                          'Comments: %{marker.color:,}<br>' +
                          '<extra></extra>',
            text=top_posts['upvotes'],
            texttemplate='%{text:,}',
            textposition='outside',
            textfont=dict(size=11, color='#1F2937')
        ))
        
        fig.update_layout(
            **plotly_layout(),
            height=550,
            xaxis_title="Upvotes",
            yaxis_title="",
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=40)
        )
        
        fig.update_yaxes(
            categoryorder="total ascending",
            tickfont=dict(size=11),
            tickmode='linear'
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    end_card()
