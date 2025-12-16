# predictive_analytics.py
# Machine learning module for predictions and forecasting

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import streamlit as st
from datetime import datetime


class PredictiveAnalytics:
    """Machine learning predictions for YouTube performance"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.feature_importance = None
    
    def prepare_features(self, df):
        """Prepare features for machine learning - STRICT PRE-UPLOAD ONLY"""
        df_ml = df.copy()
        
        # CRITICAL: Sort by upload date to ensure lag features are correct
        df_ml = df_ml.sort_values('upload_date', ascending=True).reset_index(drop=True)
        
        # ===== TIME-BASED FEATURES (Pre-upload) =====
        df_ml['hour'] = df_ml['upload_date'].dt.hour
        df_ml['day_of_week'] = df_ml['upload_date'].dt.dayofweek
        df_ml['day_of_month'] = df_ml['upload_date'].dt.day
        df_ml['month'] = df_ml['upload_date'].dt.month
        df_ml['year'] = df_ml['upload_date'].dt.year
        df_ml['is_weekend'] = (df_ml['day_of_week'] >= 5).astype(int)
        
        # ===== VIDEO CONTENT FEATURES (Pre-upload) =====
        df_ml['duration_minutes'] = df_ml['duration_seconds'] / 60
        df_ml['title_length'] = df_ml['title'].str.len()
        df_ml['has_uppercase'] = df_ml['title'].str.contains(r'[A-Z]{2,}').astype(int)
        
        # Title word count
        df_ml['title_word_count'] = df_ml['title'].str.split().str.len()
        
        # ===== CATEGORY FEATURES (Pre-upload) =====
        if 'category_id' in df_ml.columns:
            # Get top 5 most common categories, group rest as 'other'
            top_categories = df_ml['category_id'].value_counts().head(5).index.tolist()
            df_ml['category_grouped'] = df_ml['category_id'].apply(
                lambda x: x if x in top_categories else 'other'
            )
            # One-hot encode
            category_dummies = pd.get_dummies(df_ml['category_grouped'], prefix='cat')
            df_ml = pd.concat([df_ml, category_dummies], axis=1)
        
        # ===== CHANNEL MOMENTUM FEATURES (Pre-upload) =====
        if len(df_ml) > 5:
            # Upload consistency
            df_ml['days_since_last_upload'] = df_ml['upload_date'].diff().dt.days.fillna(0)
            df_ml['avg_upload_interval'] = df_ml['days_since_last_upload'].rolling(window=5, min_periods=1).mean()
            
            # Historical performance (lag features)
            df_ml['prev_video_views'] = df_ml['view_count'].shift(1).fillna(0)
            df_ml['avg_last_3_views'] = df_ml['view_count'].rolling(window=3, min_periods=1).mean().shift(1).fillna(0)
            df_ml['avg_last_5_views'] = df_ml['view_count'].rolling(window=5, min_periods=1).mean().shift(1).fillna(0)
            
            # Channel growth trend
            df_ml['views_trend'] = df_ml['view_count'].rolling(window=5, min_periods=1).apply(
                lambda x: (x.iloc[-1] - x.iloc[0]) / len(x) if len(x) > 1 else 0
            ).shift(1).fillna(0)
        
        return df_ml
    
    def train_view_predictor(self, df, target='view_count'):
        """Train model to predict video views using ONLY pre-upload data"""
        df_ml = self.prepare_features(df)
        
        # ===== STRICT PRE-UPLOAD FEATURES ONLY =====
        feature_cols = [
            # Time features
            'duration_seconds', 'hour', 'day_of_week', 'month',
            'is_weekend', 
            # Title features
            'title_length', 'has_uppercase', 'title_word_count'
        ]
        
        # Add category features (dynamically find one-hot encoded columns)
        category_cols = [col for col in df_ml.columns if col.startswith('cat_')]
        if category_cols:
            feature_cols.extend(category_cols)
        
        # Add channel momentum features
        if 'days_since_last_upload' in df_ml.columns:
            feature_cols.extend([
                'days_since_last_upload',
                'avg_upload_interval',
                'prev_video_views',
                'avg_last_3_views',
                'avg_last_5_views',
                'views_trend'
            ])
        
        # Remove rows with NaN
        df_clean = df_ml[feature_cols + [target]].dropna()
        
        if len(df_clean) < 10:
            return None, "Not enough data for training (need at least 10 videos)"
        
        X = df_clean[feature_cols]
        y_raw = df_clean[target]
        
        # ===== LOG TRANSFORM (Handle Power Law Distribution) =====
        y = np.log1p(y_raw)  # log(1 + views) to handle zeros
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train multiple models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5)
        }
        
        results = {}
        
        for name, model in models.items():
            # Train
            if name == 'Linear Regression':
                model.fit(X_train_scaled, y_train)
                y_pred_log = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred_log = model.predict(X_test)
            
            # Convert predictions back to real scale
            y_pred = np.expm1(y_pred_log)
            y_test_real = np.expm1(y_test)
            
            # Evaluate on REAL scale (not log scale)
            r2 = r2_score(y_test_real, y_pred)
            mae = mean_absolute_error(y_test_real, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test_real, y_pred))
            
            results[name] = {
                'model': model,
                'r2': r2,
                'mae': mae,
                'rmse': rmse,
                'predictions': y_pred,
                'actual': y_test_real
            }
        
        # Get feature importance from best tree-based model
        best_model_name = max(results.keys(), key=lambda k: results[k]['r2'])
        if best_model_name in ['Random Forest', 'Gradient Boosting']:
            self.feature_importance = pd.DataFrame({
                'feature': feature_cols,
                'importance': results[best_model_name]['model'].feature_importances_
            }).sort_values('importance', ascending=False)
        
        # Store feature columns and scaler for prediction
        self.feature_cols = feature_cols
        self.use_log_transform = True  # Flag to remember we're using log transform
        
        self.models = results
        return results, None
    
    def predict_next_video_views(self, df, next_video_params):
        """Predict views for next video using ONLY pre-upload data"""
        if 'Random Forest' not in self.models:
            return None
        
        model = self.models['Random Forest']['model']
        
        # Prepare basic features for new video
        current_month = datetime.now().month
        features = {
            'duration_seconds': next_video_params.get('duration', 600),
            'hour': next_video_params.get('hour', 12),
            'day_of_week': next_video_params.get('day_of_week', 0),
            'month': next_video_params.get('month', current_month),
            'is_weekend': 1 if next_video_params.get('day_of_week', 0) >= 5 else 0,
            'title_length': next_video_params.get('title_length', 50),
            'has_uppercase': next_video_params.get('has_uppercase', 0),
            'title_word_count': next_video_params.get('title_length', 50) // 6  # Approximate
        }
        
        # Add category features (set most common category as default)
        category_cols = [col for col in self.feature_cols if col.startswith('cat_')]
        if category_cols and 'category_id' in df.columns:
            most_common_category = df['category_id'].mode()[0] if len(df) > 0 else None
            
            for cat_col in category_cols:
                features[cat_col] = 0
            
            if most_common_category:
                cat_col_name = f'cat_{most_common_category}'
                if cat_col_name in category_cols:
                    features[cat_col_name] = 1
                elif 'cat_other' in category_cols:
                    features['cat_other'] = 1
        
        # Add channel momentum features
        if 'days_since_last_upload' in self.feature_cols and len(df) > 0:
            # Calculate from actual data
            df_sorted = df.sort_values('upload_date', ascending=True)
            last_upload = df_sorted['upload_date'].iloc[-1]
            days_since = (datetime.now(last_upload.tzinfo) - last_upload).days
            
            features['days_since_last_upload'] = days_since
            features['avg_upload_interval'] = days_since  # Use same for new video
            features['prev_video_views'] = df_sorted['view_count'].iloc[-1]
            features['avg_last_3_views'] = df_sorted['view_count'].tail(3).mean() if len(df) >= 3 else df_sorted['view_count'].iloc[-1]
            features['avg_last_5_views'] = df_sorted['view_count'].tail(5).mean() if len(df) >= 5 else df_sorted['view_count'].mean()
            
            # Calculate trend
            if len(df_sorted) >= 5:
                recent_views = df_sorted['view_count'].tail(5).values
                features['views_trend'] = (recent_views[-1] - recent_views[0]) / len(recent_views)
            else:
                features['views_trend'] = 0
        
        # Create DataFrame with features in the same order as training
        if hasattr(self, 'feature_cols'):
            X_new = pd.DataFrame([features])[self.feature_cols]
        else:
            X_new = pd.DataFrame([features])
        
        # Predict (on log scale if model was trained that way)
        prediction_log = model.predict(X_new)[0]
        
        # Convert back from log scale
        if hasattr(self, 'use_log_transform') and self.use_log_transform:
            prediction = np.expm1(prediction_log)
        else:
            prediction = prediction_log
        
        return max(0, int(prediction))
    
    def forecast_channel_growth(self, df, days_ahead=30):
        """Forecast channel growth using proper exponential smoothing with trend"""
        df_sorted = df.sort_values('upload_date')
        
        # Aggregate by date
        daily_views = df_sorted.groupby(df_sorted['upload_date'].dt.date)['view_count'].sum()
        
        if len(daily_views) < 7:
            return None, "Not enough historical data for forecasting"
        
        # Holt's Linear Trend Method (Double Exponential Smoothing)
        alpha = 0.3  # Level smoothing
        beta = 0.1   # Trend smoothing
        
        # Initialize
        level = daily_views.iloc[0]
        trend = (daily_views.iloc[-1] - daily_views.iloc[0]) / len(daily_views)
        
        # Apply exponential smoothing to historical data
        for value in daily_views:
            prev_level = level
            level = alpha * value + (1 - alpha) * (level + trend)
            trend = beta * (level - prev_level) + (1 - beta) * trend
        
        # Generate forecasts
        forecast = []
        for i in range(1, days_ahead + 1):
            forecast_value = level + i * trend
            forecast.append(max(0, forecast_value))  # Ensure non-negative
        
        # Create forecast dataframe
        last_date = pd.to_datetime(daily_views.index[-1])
        forecast_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=days_ahead,
            freq='D'
        )
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'forecasted_views': forecast
        })
        
        return forecast_df, None
    
    def analyze_optimal_upload_time(self, df):
        """Analyze best time to upload videos"""
        if df.empty:
            return None
        
        # Group by hour and day of week
        hour_performance = df.groupby('publish_hour').agg({
            'view_count': 'mean',
            'engagement_rate': 'mean',
            'title': 'count'
        }).rename(columns={'title': 'video_count'})
        
        day_performance = df.groupby('publish_day').agg({
            'view_count': 'mean',
            'engagement_rate': 'mean',
            'title': 'count'
        }).rename(columns={'title': 'video_count'})
        
        # Find optimal time
        best_hour = hour_performance['view_count'].idxmax()
        best_day = day_performance['view_count'].idxmax()
        
        return {
            'best_hour': best_hour,
            'best_day': best_day,
            'hour_performance': hour_performance,
            'day_performance': day_performance
        }
    
    def calculate_video_score(self, df):
        """Calculate a comprehensive performance score for each video"""
        df_scored = df.copy()
        
        # Normalize metrics to 0-100 scale
        for col in ['view_count', 'like_count', 'comment_count', 'engagement_rate']:
            if col in df_scored.columns:
                min_val = df_scored[col].min()
                max_val = df_scored[col].max()
                if max_val > min_val:
                    df_scored[f'{col}_normalized'] = (
                        (df_scored[col] - min_val) / (max_val - min_val) * 100
                    )
                else:
                    df_scored[f'{col}_normalized'] = 50
        
        # Calculate weighted score
        df_scored['performance_score'] = (
            df_scored['view_count_normalized'] * 0.4 +
            df_scored['like_count_normalized'] * 0.3 +
            df_scored['comment_count_normalized'] * 0.2 +
            df_scored['engagement_rate_normalized'] * 0.1
        )
        
        # Categorize
        df_scored['performance_tier'] = pd.cut(
            df_scored['performance_score'],
            bins=[0, 25, 50, 75, 100],
            labels=['Poor', 'Fair', 'Good', 'Excellent']
        )
        
        return df_scored
