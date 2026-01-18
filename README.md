![InsightTube](assets/InsightTube_Logo.png)
***Understand the audience, through every comment.***

InsightTube is an AI-powered YouTube comment analyzer that transforms thousands of viewer comments into actionable insights. Get instant sentiment analysis, trending topics, controversy detection, and an interactive AI assistant to explore your audience's feedback and summary of the video.

---

## Features

### **Comprehensive Analytics Dashboard**
- **Real-time Sentiment Analysis**: Gauge overall audience mood with visual sentiment scores
- **Topic Extraction**: Automatically identify trending themes and conversation topics
- **Controversy Detection**: Spot potentially divisive content before it becomes a problem
- **Spam Filtering**: Clean insights by removing noise from your comment data

### **AI Chat Assistant**
- Ask natural language questions about your video's performance
- Get context-aware answers based on actual comment data
- Explore sentiment trends, common complaints, and audience preferences
- Conversational memory maintains context throughout your session

### **Powered by Gemini AI**
- Google's Gemini 2.0 Flash for lightning-fast analysis
- Intelligent caching to reduce API calls and improve performance
- Robust error handling with automatic retries
- Production-ready logging and monitoring

---

## How to Use

### Prerequisites
- Python 3.8+

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Markus8888888/InsightTube
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser**

Navigate to `http://localhost:8501`

---

## How It Works

### 1. **Data Collection**
Paste any YouTube video URL, and InsightTube fetches comments using the YouTube Data API v3.

### 2. **AI Analysis**
Each comment is analyzed using Google's Gemini model to extract:
- Sentiment score
- Top themes/topics
- Controversy level
- Spam detection and filtering

### 3. **Interactive Exploration**
Use the AI chat assistant to dive deeper:
- "What are people saying about the audio quality?"
- "Are there any common complaints?"
- "What did viewers like most?"

---

## Acknowledgments

- **Google Gemini** for powerful AI capabilities
- **Streamlit** for the amazing web framework
- **Plotly** for formal visualizations
- **YouTube Data API** for comment access

---

<div align="center">

**Built with _goal of transparency_ by the InsightTube Team**

*Understand the audience, through every comment.*

Made for nwhacks 2026

</div>
