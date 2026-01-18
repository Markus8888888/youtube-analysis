import streamlit as st
import time
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

# Import backend services
try:
    from src.backend.backend_service import BackEndService
    from src.frontend.dashboard import render_dashboard
    from src.frontend.chat_ui import render_chat_interface
    backend_available = True
except ImportError as e:
    st.error(f"Backend import error: {e}")
    backend_available = False

# Initialize backend service
@st.cache_resource
def get_backend_service():
    """Initialize and cache the backend service"""
    try:
        return BackEndService()
    except Exception as e:
        st.error(f"Failed to initialize backend: {e}")
        return None

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
    if not backend_available:
        st.error("❌ Backend services are not available. Please check your configuration.")
    else:
        backend = get_backend_service()
        if backend is None:
            st.error("❌ Failed to initialize backend service.")
        else:
            with st.spinner("🔍 Fetching video data and analyzing comments..."):
                try:
                    # Step 1: Fetch video data from YouTube
                    video_record = backend.fetch_and_process_video(youtube_url)
                    
                    if not video_record:
                        st.error("❌ Failed to fetch video data. Please check the URL.")
                    else:
                        st.info(f"✅ Fetched {len(video_record.get('comments', []))} comments from: {video_record.get('title', 'Unknown')}")
                        
                        # Step 2: Analyze with AI
                        with st.spinner("🧠 Analyzing sentiment and extracting insights..."):
                            analysis = backend.analyze_video_with_ai(video_record)
                            
                            if not analysis:
                                st.error("❌ AI analysis failed.")
                            else:
                                # Step 3: Communicate to frontend (updates session_state)
                                backend.communicate_analysis(analysis)
                                st.success("✨ Analysis Complete!")
                                st.rerun()
                
                except ValueError as ve:
                    st.error(f"❌ Invalid input: {ve}")
                except Exception as e:
                    st.error(f"❌ Error during analysis: {e}")
                    st.exception(e)  # Show full traceback in development

# Render content based on analysis state
if st.session_state.get('analysis_ready', False):
    analytics_data = st.session_state.get('analytics_data')
    
    if analytics_data:
        # Tabs for navigation
        tab1, tab2 = st.tabs(["📊 Dashboard", "💬 AI Chat"])
        
        with tab1:
            render_dashboard(analytics_data)
        
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