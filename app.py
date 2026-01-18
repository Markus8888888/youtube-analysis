import streamlit as st
import time

# Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="YouTube Comment Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium dark theme
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a0b2e 50%, #0f0f23 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .stButton>button {
        background: linear-gradient(135deg, #9333ea 0%, #ec4899 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 12px 32px;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(147, 51, 234, 0.3);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        box-shadow: 0 15px 40px rgba(147, 51, 234, 0.5);
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        color: white;
        padding: 16px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px 12px 0 0;
        color: #9ca3af;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-bottom: 2px solid #9333ea;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }
    
    [data-testid="stMetricLabel"] {
        color: #9ca3af;
        font-size: 0.875rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white;
    }
    
    h1 {
        background: linear-gradient(135deg, #ffffff 0%, #e0c3fc 50%, #fbc2eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Import frontend modules
from src.frontend.dashboard import render_dashboard
from src.frontend.chat_ui import render_chat_interface

# --- HEADER ---
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("# 🚀 YouTube Comment Analyzer")
    st.markdown("**Powered by AI • Instant insights from your audience**")

# --- URL INPUT SECTION ---
st.markdown("---")
col_input, col_button = st.columns([4, 1])

with col_input:
    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="Paste YouTube video URL here...",
        label_visibility="collapsed"
    )

with col_button:
    analyze_btn = st.button("⚡ Analyze", type="primary", use_container_width=True)

st.markdown("---")

# --- MAIN APP LOGIC ---
if analyze_btn and youtube_url:
    with st.spinner("🔍 Analyzing comments, detecting sentiment, and extracting insights..."):
        time.sleep(2.5)
        
        st.session_state['analytics_data'] = {
            'total_comments': 452,
            'spam_count': 34,
            'controversy_score': 'Medium',
            'sentiment_score': 0.65,
            'top_topics': {
                'Topic': ['Video Quality', 'Sound Design', 'Price Point', 'Editing', 'Intro Length'],
                'Count': [120, 85, 60, 45, 20]
            }
        }
        st.success("✨ Analysis Complete!")

# Render content based on analysis state
if 'analytics_data' in st.session_state:
    # Tabs for navigation
    tab1, tab2 = st.tabs(["📊 Dashboard", "💬 AI Chat"])
    
    with tab1:
        render_dashboard(st.session_state['analytics_data'])
    
    with tab2:
        render_chat_interface()
else:
    # Landing Page
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px;'>
        <div style='font-size: 4rem; margin-bottom: 20px;'>✨</div>
        <h2 style='color: white; font-size: 2rem; margin-bottom: 16px;'>Unlock Deep Audience Insights</h2>
        <p style='color: #9ca3af; font-size: 1.125rem; margin-bottom: 48px;'>
            Paste any YouTube URL above to instantly analyze comments, detect sentiment, and discover what your audience really thinks
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='padding: 24px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;'>
            <div style='font-size: 2.5rem; margin-bottom: 16px;'>📈</div>
            <h3 style='color: white; font-size: 1.125rem; margin-bottom: 8px;'>Sentiment Analysis</h3>
            <p style='color: #9ca3af; font-size: 0.875rem;'>See how people feel instantly</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 24px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;'>
            <div style='font-size: 2.5rem; margin-bottom: 16px;'>📊</div>
            <h3 style='color: white; font-size: 1.125rem; margin-bottom: 8px;'>Topic Extraction</h3>
            <p style='color: #9ca3af; font-size: 0.875rem;'>Find trending conversation themes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='padding: 24px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;'>
            <div style='font-size: 2.5rem; margin-bottom: 16px;'>💬</div>
            <h3 style='color: white; font-size: 1.125rem; margin-bottom: 8px;'>AI Chat</h3>
            <p style='color: #9ca3af; font-size: 0.875rem;'>Ask questions about your data</p>
        </div>
        """, unsafe_allow_html=True)