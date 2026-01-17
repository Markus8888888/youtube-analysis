# 🎥 YouTube Comment Analyzer

> AI-powered comment analysis tool that helps content creators understand their audience in seconds, not hours.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

- **📊 Instant Analytics Dashboard** - Get sentiment scores, top themes, and controversy levels in one glance
- **💬 AI-Powered Chat Interface** - Ask questions about your comments in natural language
- **🧹 Smart Data Cleaning** - Automatically removes spam, duplicates, and noise
- **📄 PDF Export** - Generate professional reports for stakeholders
- **⚡ Real-time Processing** - Analyze up to 200 comments in seconds

## 🎯 Business Value

**Save 10+ hours per week** by automating comment analysis that creators typically do manually.

- Content creators can identify trending topics and audience sentiment instantly
- Brands can monitor customer feedback and reputation in real-time
- Researchers can analyze public opinion at scale
- Community managers can prioritize responses to critical comments

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  YouTube    │─────▶│ Data Cleaner │─────▶│   Gemini    │
│  API v3     │      │  & Validator │      │   AI API    │
└─────────────┘      └──────────────┘      └─────────────┘
                              │                     │
                              ▼                     ▼
                     ┌─────────────────────────────────┐
                     │    Streamlit Dashboard          │
                     │  • Analytics  • Chat  • Export  │
                     └─────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.9 or higher
- Google Cloud Console account (for YouTube Data API)
- Google AI Studio account (for Gemini API)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-comment-analyzer.git
cd youtube-comment-analyzer
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**📚 Need help getting API keys?**
- [YouTube API Setup Guide](docs/API_SETUP.md)
- [Gemini API Setup Guide](docs/GEMINI_SETUP.md)

## 🎮 Usage

### Quick Start

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Step-by-Step

1. **Enter YouTube URL** - Paste any YouTube video URL in the sidebar
2. **Add API Keys** - Input your YouTube and Gemini API keys (or use environment variables)
3. **Analyze** - Click "Analyze Comments" and wait a few seconds
4. **Explore**:
   - **Dashboard Tab**: View sentiment scores, top themes, and visualizations
   - **Chat Tab**: Ask questions like "What are viewers complaining about?"
5. **Export** - Download your analysis as a PDF report

### Demo Mode (No API Keys Required)

```bash
# Uses dummy_data.json for testing
streamlit run app.py -- --demo
```

## 📁 Project Structure

```
youtube-comment-analyzer/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
│
├── src/
│   ├── data_miner/                 # Role 1: Data fetching & cleaning
│   │   ├── youtube_api.py          # YouTube API integration
│   │   ├── data_cleaner.py         # Text preprocessing
│   │   └── dummy_data.json         # Mock data for testing
│   │
│   ├── ai_brain/                   # Role 2: AI & prompt engineering
│   │   ├── gemini_client.py        # Gemini API wrapper
│   │   ├── prompts.py              # Prompt templates
│   │   └── chat_manager.py         # Conversation history
│   │
│   ├── frontend/                   # Role 3: UI & visualizations
│   │   ├── dashboard.py            # Analytics dashboard
│   │   ├── chat_ui.py              # Chat interface
│   │   └── visualizations.py       # Chart generation
│   │
│   └── utils/                      # Role 4: Integration & extras
│       ├── pdf_export.py           # PDF report generator
│       ├── validators.py           # Input validation
│       └── error_handlers.py       # Error handling
│
├── tests/                          # Unit tests
├── docs/                           # Documentation
└── pitch/                          # Presentation materials
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_youtube_api.py

# Run with coverage
pytest --cov=src tests/
```

## 🔧 Configuration

### AI Model Tuning

Edit `src/ai_brain/gemini_client.py`:

```python
# For data extraction (precise)
temperature = 0.1

# For chat interface (creative)
temperature = 0.7
```

### Comment Limit

Edit `src/data_miner/youtube_api.py`:

```python
MAX_COMMENTS = 200  # Adjust based on your needs
```

## 🚨 Error Handling

The app gracefully handles:

- ✅ Invalid YouTube URLs
- ✅ Videos with comments disabled
- ✅ API rate limits
- ✅ Network timeouts
- ✅ Empty comment sections
- ✅ Foreign language comments

## 🎨 Customization

### Add New Visualizations

```python
# In src/frontend/visualizations.py
def create_word_cloud(comments):
    # Your custom visualization
    pass
```

### Modify Analysis Prompts

```python
# In src/ai_brain/prompts.py
CUSTOM_PROMPT = """
Analyze these comments and return...
"""
```

## 🤝 Team Roles

This project is designed for hackathon teams of 4:

- **Role 1: Data Miner** - YouTube API, data cleaning
- **Role 2: AI Brain** - Gemini integration, prompt engineering
- **Role 3: Artist** - Streamlit UI, visualizations
- **Role 4: Glue** - Integration, error handling, PDF export

## 📊 Example Output

```json
{
  "sentiment_score": 7.5,
  "sentiment_label": "Positive",
  "top_themes": [
    {"theme": "Tutorial Quality", "count": 45},
    {"theme": "Audio Issues", "count": 23},
    {"theme": "Feature Requests", "count": 18}
  ],
  "controversy_level": "Low",
  "summary": "Viewers love the content but mention audio problems..."
}
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in Settings → Secrets

```toml
YOUTUBE_API_KEY = "your_key"
GEMINI_API_KEY = "your_key"
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for other options (Docker, Heroku, AWS).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- YouTube Data API v3
- Google Gemini AI
- Streamlit framework
- Hackathon organizers and mentors

## 📞 Support

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/youtube-comment-analyzer/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/youtube-comment-analyzer/discussions)

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Sentiment trend over time
- [ ] Toxic comment detection
- [ ] Competitor comparison
- [ ] Automated response suggestions
- [ ] Browser extension

---

**Made with ❤️ for creators who care about their community**

⭐ Star this repo if you find it useful!