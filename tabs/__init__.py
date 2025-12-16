# tabs/__init__.py
from .top_videos import render_top_videos_tab
from .upload_schedule import render_upload_schedule_tab
from .insights import render_insights_tab
from .predictions import render_predictions_tab

__all__ = ['render_top_videos_tab', 'render_upload_schedule_tab', 'render_insights_tab', 'render_predictions_tab']
