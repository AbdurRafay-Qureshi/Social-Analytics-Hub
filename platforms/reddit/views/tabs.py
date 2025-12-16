# platforms/reddit/views/tabs.py
"""
Reddit Tabs Component.
Renders all 4 tab contents: Top Content, Activity Analysis, Insights, Data Table.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from ui.components import chart_card, end_card, info_card
from ui.styles import plotly_layout


def render_reddit_tabs(posts_df, reddit_data, stats):
    """
    Render all 4 tabs for Reddit dashboard.
    
    Args:
        posts_df: DataFrame with posts data
        reddit_data: Reddit data dict with 'type' and 'name' keys
        stats: Stats dict from Reddit API
    """
    tab1, tab2, tab3, tab4 = st.tabs(["Top Content", "Activity Analysis", "Insights", "Data Table"])
    
    # TAB 1: Top Content
    with tab1:
        cont = chart_card("Top 20 Posts")
        with cont:
            posts_df_sorted = posts_df.sort_values('upvotes', ascending=False).head(20).reset_index(drop=True)
            
            # Add rank column
            posts_df_sorted.insert(0, 'Rank', range(1, len(posts_df_sorted) + 1))
            
            # Prepare display dataframe
            display_df = posts_df_sorted[['Rank', 'title', 'upvotes', 'num_comments', 'engagement_rate']].copy()
            display_df.columns = ['#', 'Post Title', 'Upvotes', 'Comments', 'Engagement %']
            
            # Truncate titles
            display_df['Post Title'] = display_df['Post Title'].apply(lambda x: x[:80] + "..." if len(str(x)) > 80 else x)
            
            # Display with styling
            st.dataframe(
                display_df,
                use_container_width=True,
                height=600,
                hide_index=True,
                column_config={
                    "#": st.column_config.NumberColumn(
                        "#",
                        width="small",
                        help="Rank"
                    ),
                    "Post Title": st.column_config.TextColumn(
                        "Post Title",
                        width="large",
                    ),
                    "Upvotes": st.column_config.NumberColumn(
                        "⬆️ Upvotes",
                        width="small",
                        format="%d"
                    ),
                    "Comments": st.column_config.NumberColumn(
                        "💬 Comments",
                        width="small",
                        format="%d"
                    ),
                    "Engagement %": st.column_config.NumberColumn(
                        "📊 Engagement %",
                        width="small",
                        format="%.4f%%"
                    ),
                }
            )
        end_card()
    
    # TAB 2: Activity Analysis
    with tab2:
        if reddit_data['type'] == 'subreddit':
            a, b = st.columns(2)
            with a:
                cont = chart_card("Posts by Hour")
                with cont:
                    if 'created_utc' in posts_df.columns:
                        posts_df_copy = posts_df.copy()
                        posts_df_copy['hour'] = pd.to_datetime(posts_df_copy['created_utc'], unit='s', errors='coerce').dt.hour
                        hour_counts = posts_df_copy['hour'].value_counts().sort_index()
                        fig = px.line(hour_counts, markers=True)
                        fig.update_traces(line_color="#FF4500", line_width=2.5)
                        fig.update_layout(**plotly_layout(), height=350)
                        st.plotly_chart(fig, use_container_width=True)
                end_card()
            
            with b:
                cont = chart_card("Posts by Day")
                with cont:
                    if 'created_utc' in posts_df.columns:
                        posts_df_copy = posts_df.copy()
                        posts_df_copy['day_name'] = pd.to_datetime(posts_df_copy['created_utc'], unit='s', errors='coerce').dt.day_name()
                        day_counts = posts_df_copy['day_name'].value_counts().reindex(
                            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                            fill_value=0
                        )
                        fig = px.bar(day_counts, color=day_counts.values, color_continuous_scale="Oranges")
                        fig.update_layout(**plotly_layout(), height=350)
                        st.plotly_chart(fig, use_container_width=True)
                end_card()
        
        else:  # User
            cont = chart_card("Activity Across Subreddits")
            with cont:
                if 'subreddit' in posts_df.columns:
                    subreddit_counts = posts_df['subreddit'].value_counts().head(10)
                    fig = px.bar(subreddit_counts, orientation='h')
                    fig.update_traces(marker_color="#FF4500")
                    fig.update_layout(**plotly_layout(), height=400)
                    st.plotly_chart(fig, use_container_width=True)
            end_card()
    
    # TAB 3: Insights
    with tab3:
        if not posts_df.empty:
            try:
                from ..insights import RedditInsights
                insights = RedditInsights(posts_df, stats)
                
                chart_choice = st.selectbox(
                    "Choose Analysis",
                    [
                        "Engagement Heatmap",
                        "Engagement Distribution",
                        "Posting Timeline",
                        "Top Subreddits" if reddit_data['type'] == 'user' else "Content Type Analysis"
                    ],
                    key="reddit_insights_choice"
                )
                
                cont = chart_card(chart_choice)
                with cont:
                    try:
                        if chart_choice == "Posting Timeline":
                            st.warning("⚠️ Note: This shows the sample of posts analyzed, not the entire subreddit history")
                            st.markdown("*Distribution of the most recent posts*")
                            fig = insights.posting_timeline()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif chart_choice == "Engagement Heatmap":
                            st.markdown("*See when posts perform best (darker = better)*")
                            st.success("💡 **Strategy Tip:** Post during darker time slots to avoid competition and maximize engagement")
                            fig = insights.engagement_heatmap()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif chart_choice == "Engagement Distribution":
                            st.markdown("*Distribution of upvotes across posts*")
                            fig = insights.engagement_distribution()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif chart_choice == "Top Subreddits":
                            st.markdown("*Your best performing subreddits*")
                            fig = insights.top_subreddits_performance()
                            if fig:
                                fig.update_layout(**plotly_layout())
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("Not enough data for this analysis")
                        
                        else:  # Content Type Analysis
                            st.markdown("*Compare self posts vs links/media*")
                            fig = insights.content_type_analysis()
                            if fig:
                                fig.update_layout(**plotly_layout())
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("Post type data not available")
                    
                    except Exception as e:
                        st.error(f"Error creating chart: {str(e)}")
                end_card()
            except ImportError:
                info_card("Insights", "reddit_insights.py module not found")
        else:
            info_card("Insights", "No data available for analysis")
    
    # TAB 4: Data Table
    with tab4:
        cont = chart_card("Raw Data")
        
        # Safely select only existing columns
        if reddit_data['type'] == 'subreddit':
            available_cols = [col for col in ['title', 'author', 'upvotes', 'num_comments'] if col in posts_df.columns]
        else:
            available_cols = [col for col in ['title', 'subreddit', 'upvotes', 'num_comments'] if col in posts_df.columns]
        
        if available_cols:
            display_df = posts_df[available_cols].copy()
            
            # Rename for display
            column_rename_map = {
                'title': 'Title',
                'author': 'Author',
                'subreddit': 'Subreddit',
                'upvotes': 'Upvotes',
                'num_comments': 'Comments'
            }
            display_df.columns = [column_rename_map.get(col, col) for col in available_cols]
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=500,
                hide_index=True
            )
        else:
            st.warning("No data columns available to display")
        
        end_card()
