# tabs/predictions.py
"""
Predictions Tab - ML-Powered YouTube Analytics
Provides predictive insights, optimal upload times, and performance forecasting.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from ui.components import chart_card, end_card, info_card


def render_predictions_tab(df, stats):
    """Render the Predictions tab with ML-powered insights"""
    
    if df.empty:
        info_card("Predictions", "Not enough data for predictions. Analyze more videos first.")
        return
    
    # Check if predictive analytics is available
    try:
        from platforms.youtube.predictive_analytics import PredictiveAnalytics
        predictor = PredictiveAnalytics()
    except ImportError:
        st.warning("⚠️ Predictive analytics requires scikit-learn. Install with: `pip install scikit-learn`")
        return
    
    # Initialize predictor
    st.markdown("## 🔮 Predictive Analytics & ML Insights")
    st.markdown("")
    
    # ==== SECTION 1: Best Upload Times ====
    cont = chart_card("⏰ Optimal Upload Times for Your Channel")
    with cont:
        try:
            optimal_times = predictor.analyze_optimal_upload_time(df)
            
            if optimal_times:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #033E6B 0%, #0D2956 100%); border-radius: 12px; padding: 24px; text-align: center;">
                        <div style="color: rgba(255,255,255,0.9); font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">🕐 BEST HOUR TO UPLOAD</div>
                        <div style="color: white; font-size: 48px; font-weight: 800; margin: 12px 0; font-family: 'Inter', sans-serif;">{optimal_times['best_hour']:02d}:00</div>
                        <div style="color: rgba(255,255,255,0.85); font-size: 14px;">UTC Time Zone</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #2587C8 0%, #156CA5 100%); border-radius: 12px; padding: 24px; text-align: center;">
                        <div style="color: rgba(255,255,255,0.9); font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">📅 BEST DAY TO UPLOAD</div>
                        <div style="color: white; font-size: 48px; font-weight: 800; margin: 12px 0; font-family: 'Inter', sans-serif;">{optimal_times['best_day']}</div>
                        <div style="color: rgba(255,255,255,0.85); font-size: 14px;">Highest Average Views</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Hour performance chart
                hour_perf = optimal_times['hour_performance'].reset_index()
                hour_perf.columns = ['Hour', 'Avg Views', 'Avg Engagement', 'Video Count']
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=hour_perf['Hour'],
                    y=hour_perf['Avg Views'],
                    marker=dict(
                        color=hour_perf['Avg Engagement'],
                        colorscale='Blues',
                        showscale=True,
                        colorbar=dict(title="Engagement %")
                    ),
                    hovertemplate='<b>Hour: %{x}:00</b><br>Avg Views: %{y:,.0f}<br><extra></extra>'
                ))
                
                fig.update_layout(
                    title="Average Views by Upload Hour",
                    xaxis_title="Hour (UTC)",
                    yaxis_title="Average Views",
                    height=400,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error analyzing upload times: {str(e)}")
    
    end_card()
    
    # ==== SECTION 2: Next Video Performance Predictor ====
    cont = chart_card("🎯 Next Video Performance Predictor")
    with cont:
        st.markdown("*Predict how many views your next video will get based on when you upload it*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            upload_hour = st.slider("⏰ Upload Hour (UTC)", 0, 23, 12, key="pred_hour")
            upload_day = st.selectbox("📅 Upload Day", 
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                index=2,
                key="pred_day"
            )
        
        with col2:
            duration = st.slider("⏱️ Video Duration (minutes)", 1, 60, 10, key="pred_duration")
            title_length = st.slider("📝 Title Length (characters)", 20, 100, 50, key="pred_title")
        
        if st.button("🔮 Predict Views", type="primary", use_container_width=True):
            try:
                results, error = predictor.train_view_predictor(df)
                
                if results:
                    # Map day to number
                    day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, 
                              "Friday": 4, "Saturday": 5, "Sunday": 6}
                    
                    predicted_views = predictor.predict_next_video_views(df, {
                        'hour': upload_hour,
                        'day_of_week': day_map[upload_day],
                        'duration': duration * 60,
                        'title_length': title_length,
                        'has_uppercase': 1
                    })
                    
                    if predicted_views:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #7CC0E0 0%, #B6DFF1 100%); border-radius: 12px; padding: 30px; text-align: center; margin-top: 20px;">
                            <div style="color: rgba(255,255,255,0.9); font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">🎯 PREDICTED VIEWS</div>
                            <div style="color: white; font-size: 56px; font-weight: 800; margin: 16px 0; font-family: 'Inter', sans-serif;">{predicted_views:,}</div>
                            <div style="color: rgba(255,255,255,0.85); font-size: 14px;">Based on your channel's historical performance</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show model accuracy
                        best_model = max(results.keys(), key=lambda k: results[k]['r2'])
                        accuracy = results[best_model]['r2'] * 100
                        error_margin = results[best_model]['mae']
                        
                        st.info(f"📊 Model: {best_model} | Accuracy: {accuracy:.1f}% | Error Margin: ±{error_margin:,.0f} views")
                else:
                    st.warning(error or "Not enough data for predictions. Need at least 10 videos.")
            
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
    
    end_card()
    
    # ==== SECTION 3: Video Performance Scoring ====
    cont = chart_card("⭐ Video Performance Scores")
    with cont:
        try:
            scored_df = predictor.calculate_video_score(df)
            
            # Top performers
            st.subheader("🏆 Top 10 Performing Videos")
            top_videos = scored_df.nlargest(10, 'performance_score')[
                ['title', 'performance_score', 'performance_tier', 'view_count', 'engagement_rate']
            ].copy()
            
            top_videos['title'] = top_videos['title'].str[:60] + '...'
            top_videos.columns = ['Title', 'Score', 'Tier', 'Views', 'Engagement %']
            
            st.dataframe(
                top_videos,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Score": st.column_config.ProgressColumn(
                        "Performance Score",
                        format="%.1f",
                        min_value=0,
                        max_value=100,
                    ),
                    "Tier": st.column_config.TextColumn("Tier"),
                    "Views": st.column_config.NumberColumn("Views", format="%d"),
                    "Engagement %": st.column_config.NumberColumn("Engagement", format="%.2f%%"),
                }
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Performance distribution
            col1, col2 = st.columns([1, 1])
            
            with col1:
                tier_counts = scored_df['performance_tier'].value_counts()
                fig = px.pie(
                    values=tier_counts.values,
                    names=tier_counts.index,
                    title="Performance Distribution",
                    color_discrete_sequence=['#B6DFF1', '#7CC0E0', '#2587C8', '#033E6B']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Average score by tier
                avg_by_tier = scored_df.groupby('performance_tier')['view_count'].mean().reset_index()
                fig = px.bar(
                    avg_by_tier,
                    x='performance_tier',
                    y='view_count',
                    title="Average Views by Performance Tier",
                    color='performance_tier',
                    color_discrete_sequence=['#B6DFF1', '#7CC0E0', '#2587C8', '#033E6B']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error calculating scores: {str(e)}")
    
    end_card()
    
    # ==== SECTION 4: ML Model Performance ====
    with st.expander("🎓 View Model Performance Details"):
        try:
            results, error = predictor.train_view_predictor(df)
            
            if results:
                st.subheader("Model Comparison")
                
                model_comparison = []
                for name, result in results.items():
                    model_comparison.append({
                        'Model': name,
                        'Accuracy (R²)': f"{result['r2']*100:.1f}%",
                        'Avg Error (MAE)': f"±{result['mae']:,.0f}",
                        'RMSE': f"{result['rmse']:,.0f}"
                    })
                
                st.table(pd.DataFrame(model_comparison))
                
                # Feature importance
                if predictor.feature_importance is not None:
                    st.subheader("📊 What Affects Your Views Most?")
                    
                    fig = px.bar(
                        predictor.feature_importance.head(7),
                        x='importance',
                        y='feature',
                        orientation='h',
                        title="Feature Importance (Higher = More Impact)",
                        labels={'importance': 'Importance', 'feature': 'Feature'}
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error showing model details: {str(e)}")
