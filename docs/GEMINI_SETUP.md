# Gemini AI Setup Guide

## Overview
This project uses Google's Gemini AI API to power sentiment analysis, conversation management, and content insights for YouTube videos.

## Prerequisites
- Python 3.8+
- pip (Python package manager)
- Google Cloud account

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

## Step 2: Configure Environment Variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

**IMPORTANT: Never commit this file to version control. Add to `.gitignore`:**

```
.env
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` - Gemini API client
- `python-dotenv` - Environment variable management

## Step 4: Test the Setup

Run the integration tests:

```bash
cd src/ai_brain
python test_integration.py
```

Expected output:
- ✅ Health Check
- ✅ Sentiment Analysis
- ✅ Batch Analysis
- ✅ Chatbot
- ✅ Query Categorization
- ✅ Insights Generation
- ✅ Full Pipeline

## Available Models

The AI Brain uses `gemini-2.5-flash`:
- Fast inference (ideal for real-time applications)
- Cost-effective
- Supports JSON structured output
- Supports system instructions (prompt engineering)

See all available models:
```python
import google.generativeai as genai
for model in genai.list_models():
    print(model.name, model.supported_generation_methods)
```

## Usage

### Basic Example

```python
from src.ai_brain.brain import AIBrain

# Initialize
brain = AIBrain()

# Analyze comments
comments = ["Great video!", "Bad audio"]
analysis = brain.analyze_batch_comments(comments)

# Chat
response = brain.chat("How can I improve?")

# Generate insights
insights = brain.generate_insights(analysis['aggregated'])
```

## Rate Limits

**Free Tier:**
- 5 requests per minute per model
- 1,500 requests per day

**After quota reset:**
- Wait ~1 minute before making new requests

**Check usage:**
- Monitor at [Google AI Studio](https://aistudio.google.com/app/apikey)

## Troubleshooting

### Error: "GEMINI_API_KEY not found"
- Check `.env` file exists in project root
- Verify API key is correct
- Run `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"`

### Error: "429 Quota exceeded"
- Free tier has 5 requests/minute limit
- Wait 1-2 minutes before retrying
- Upgrade to paid plan for higher limits

### Error: "ModuleNotFoundError: No module named 'google.generativeai'"
```bash
pip install google-generativeai
```

### FutureWarning about deprecated package
- This is expected - the free tier uses the older API
- Package will continue to work
- No action needed

## Architecture

The AI Brain consists of 4 main components:

1. **GeminiClient** (`gemini_client.py`)
   - Low-level API wrapper
   - Handles model configuration
   - JSON extraction setup

2. **ChatManager** (`chat_manager.py`)
   - Conversation state management
   - History tracking
   - Multi-turn dialogue support

3. **Prompts** (`prompts.py`)
   - System instructions for different tasks
   - Sentiment analysis prompts
   - Query categorization prompts
   - Insight generation prompts

4. **AIBrain** (`brain.py`)
   - Orchestrates all components
   - Task routing
   - Batch processing
   - Error handling and retries

## API Costs (Paid Plans)

- **Gemini 2.5 Flash**: $0.075 per 1M input tokens, $0.30 per 1M output tokens
- Typical use case: ~100 tokens per comment analysis
- Batch processing is cost-effective

## Next Steps

- Integrate with YouTube API for real comment data
- Add caching layer for frequently analyzed comments
- Set up production monitoring and logging
- Create dashboard for analytics visualization

## Resources

- [Gemini API Docs](https://ai.google.dev/gemini-api)
- [Rate Limits & Quotas](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Models Reference](https://ai.google.dev/models)
- [Google AI Studio](https://aistudio.google.com/)
