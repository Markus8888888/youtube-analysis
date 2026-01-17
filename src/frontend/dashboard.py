import streamlit as st
from src.frontend.visualizations import render_sentiment_gauge, render_topic_chart

def render_dashboard(analytics_data):
    """
    Renders the main analytics dashboard.
    """
    st.markdown("## 📊 Instant Analytics Dashboard")
    
    # Key Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Comments", analytics_data.get('total_comments', 0))
    col2.metric("Spam Removed", analytics_data.get('spam_count', 0), delta="-Noise")
    col3.metric("Controversy Score", analytics_data.get('controversy_score', 'Low'))
    
    st.divider()
    
    # Charts Row
    c1, c2 = st.columns([1, 2])  # 1/3 width for gauge, 2/3 for topics
    
    with c1:
        render_sentiment_gauge(analytics_data.get('sentiment_score', 0))
        
    with c2:
        render_topic_chart(analytics_data.get('top_topics', {}))