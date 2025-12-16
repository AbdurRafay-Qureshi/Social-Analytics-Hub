# platforms/youtube/views/data_table.py
"""
YouTube Data Table Tab Component.
Displays video data in a styled HTML table with PDF export functionality.
"""

import streamlit as st
from ui.components import chart_card
from core.formatters import seconds_to_hms


def render_data_table_tab(df, stats):
    """
    Render the data table tab with HTML styling and PDF export.
    
    Args:
        df: Filtered dataframe with video data
        stats: Channel stats dict
    """
    cont = chart_card("Dataset")
    
    tbl = df.copy()
    tbl["Duration"] = tbl["duration_seconds"].apply(seconds_to_hms)
    tbl["Upload Date"] = tbl["upload_date"].dt.strftime("%Y-%m-%d %H:%M")
    
    display_tbl = tbl[[
        "title", "Upload Date", "view_count", "like_count", 
        "comment_count", "engagement_rate", "Duration"
    ]].copy()
    
    display_tbl.columns = [
        "Title", "Upload Date", "Views", "Likes", 
        "Comments", "Engagement Rate", "Duration"
    ]
    
    html_table = """
    <div style="background: white; border: 1px solid #E5E7EB; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
        <div style="max-height: 420px; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; background: white;">
                <thead style="background: #F3F4F6; position: sticky; top: 0; z-index: 10;">
                    <tr>
    """
    
    for col in display_tbl.columns:
        width = "30%" if col == "Title" else "10%"
        html_table += f'<th style="padding: 12px 8px; text-align: left; font-size: 13px; font-weight: 600; color: #1F2937; border-bottom: 2px solid #E5E7EB; width: {width};">{col}</th>'
    
    html_table += "</tr></thead><tbody style='background: white;'>"
    
    for idx, row in display_tbl.iterrows():
        html_table += "<tr style='border-bottom: 1px solid #F3F4F6; background: white;' onmouseover=\"this.style.background='#F9FAFB'\" onmouseout=\"this.style.background='white'\">"
        for col in display_tbl.columns:
            value = row[col]
            if col == "Engagement Rate":
                value = f"{value:.2f}%"
            elif col in ["Views", "Likes", "Comments"]:
                value = f"{value:,}"
            
            text_align = "left" if col == "Title" else "right"
            html_table += f'<td style="padding: 10px 8px; color: #1F2937; background: white; font-size: 12px; text-align: {text_align};">{value}</td>'
        html_table += "</tr>"
    
    html_table += "</tbody></table></div></div>"
    
    st.markdown(html_table, unsafe_allow_html=True)
    
    st.markdown("---")
    col_export, col_empty = st.columns([1, 3])
    with col_export:
        try:
            from pdf_exporter import generate_pdf_report
            
            if st.button("📄 Download PDF Report", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    pdf_buffer = generate_pdf_report(df, stats)
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_buffer,
                        file_name=f"{stats['channel_name']}_analytics_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        except ImportError:
            st.info("Install reportlab to enable PDF export: `pip install reportlab`")
