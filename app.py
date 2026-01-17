import streamlit as st
import time

# Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="YouTube Comment Analyzer",
    page_icon="🚀",
    layout="wide"
)

# Import frontend modules
from src.frontend.dashboard import render_dashboard
from src.frontend.chat_ui import render_chat_interface

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("🚀 Settings")
    
    api_key = st.text_input("Gemini API Key", type="password")
    youtube_url = st.text_input("YouTube Video URL", placeholder="https://youtube.com/...")
    
    st.markdown("---")
    analyze_btn = st.button("⚡ Analyze Comments", type="primary")
    
    st.markdown("### Export")
    st.download_button("📄 Download PDF Report", "dummy content", "report.pdf")

# --- MAIN APP LOGIC ---

# Tabs for navigation
tab1, tab2 = st.tabs(["📊 Dashboard", "💬 AI Chat"])

if analyze_btn and youtube_url:
    # Task 4: UX Polish - Loading Spinner
    with st.spinner("🔍 Fetching comments, removing spam, and crunching numbers..."):
        # Simulate processing time for the demo
        time.sleep(2) 
        
        # MOCK DATA (Ideally this comes from src/data_miner)
        st.session_state['analytics_data'] = {
            'total_comments': 452,
            'spam_count': 34,
            'controversy_score': 'Medium',
            'sentiment_score': 0.65, # Range -1 to 1
            'top_topics': {
                'Topic': ['Video Quality', 'Sound Design', 'Price Point', 'Editing', 'Intro Length'],
                'Count': [120, 85, 60, 45, 20]
            }
        }
        st.success("Analysis Complete!")

# Render Tabs based on data availability
if 'analytics_data' in st.session_state:
    with tab1:
        render_dashboard(st.session_state['analytics_data'])
    
    with tab2:
        render_chat_interface()
else:
    # Empty State / Landing Page
    st.info("👈 Enter a YouTube URL and click 'Analyze' to start.")
    st.markdown("""
    ### Features
    * **Sentiment Analysis:** See how people feel instantly.
    * **Topic Extraction:** Find out what they are talking about.
    * **Chat:** Ask questions like *"Why are people angry?"*
    """)