import streamlit as st
from src.frontend.visualizations import render_sentiment_gauge, render_topic_chart

def render_dashboard(analytics_data):
    """
    Renders the premium analytics dashboard.
    """
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("")
    
    # Key Metrics Row with custom styling
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='padding: 24px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%); 
                    border-radius: 16px; border: 1px solid rgba(59, 130, 246, 0.2);'>
            <div style='color: #60a5fa; font-size: 0.875rem; margin-bottom: 8px;'>Total Comments</div>
            <div style='color: white; font-size: 2.5rem; font-weight: 700;'>{}</div>
        </div>
        """.format(analytics_data.get('total_comments', 0)), unsafe_allow_html=True)
    
    with col2:
        spam_percent = (analytics_data.get('spam_count', 0) / analytics_data.get('total_comments', 1)) * 100
        st.markdown("""
        <div style='padding: 24px; background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%); 
                    border-radius: 16px; border: 1px solid rgba(34, 197, 94, 0.2);'>
            <div style='color: #4ade80; font-size: 0.875rem; margin-bottom: 8px;'>Spam Removed</div>
            <div style='color: white; font-size: 2.5rem; font-weight: 700;'>{}</div>
            <div style='color: #4ade80; font-size: 0.75rem; margin-top: 4px;'>-{:.1f}% noise</div>
        </div>
        """.format(analytics_data.get('spam_count', 0), spam_percent), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='padding: 24px; background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, rgba(249, 115, 22, 0.05) 100%); 
                    border-radius: 16px; border: 1px solid rgba(249, 115, 22, 0.2);'>
            <div style='color: #fb923c; font-size: 0.875rem; margin-bottom: 8px;'>Controversy Score</div>
            <div style='color: white; font-size: 2.5rem; font-weight: 700;'>{}</div>
        </div>
        """.format(analytics_data.get('controversy_score', 'Low')), unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    # Charts Row
    col_left, col_right = st.columns([2, 3])
    
    with col_left:
        st.markdown("""
        <div style='padding: 32px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; 
                    border: 1px solid rgba(255, 255, 255, 0.1);'>
        """, unsafe_allow_html=True)
        render_sentiment_gauge(analytics_data.get('sentiment_score', 0))
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div style='padding: 32px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; 
                    border: 1px solid rgba(255, 255, 255, 0.1);'>
        """, unsafe_allow_html=True)
        render_topic_chart(analytics_data.get('top_topics', {}))
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    # Export Button
    st.download_button(
        "📄 Download PDF Report",
        "dummy content",
        "report.pdf",
        use_container_width=False
    )