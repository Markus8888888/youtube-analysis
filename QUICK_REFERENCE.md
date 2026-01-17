# AI Brain - Quick Reference

## Installation (1 minute)

```bash
pip install -r requirements.txt
# .env file with GEMINI_API_KEY=your_key
```

## Basic Usage

```python
from src.ai_brain.brain import AIBrain

brain = AIBrain()
```

### Sentiment Analysis
```python
# Single comment
result = brain.analyze_comments("Great video!")
# Returns: {sentiment_score, top_3_themes, controversy_level}

# Multiple comments
results = brain.analyze_batch_comments(["Good!", "Bad audio", "Amazing"])
# Returns: {total_comments, analyses, aggregated stats}
```

### Chat
```python
response = brain.chat("How can I improve engagement?")
# Maintains conversation history automatically
```

### Query Routing
```python
category = brain.categorize_query("How many views?")
# Returns: "sentiment_analysis" | "engagement_analysis" | "content_analysis" | "general"
```

### Insights
```python
insights = brain.generate_insights(analytics_data)
# Returns actionable recommendations
```

### Full Pipeline
```python
report = brain.full_analysis(comments, include_insights=True)
# Single call: analyze + aggregate + insights
```

### Utilities
```python
# Health check
brain.health_check()

# Cache stats
brain.get_cache_stats()

# Clear cache
brain.clear_caches()

# Chat history reset
brain.clear_chat_history()
```

## Testing

```bash
# Quick test (7 tests)
cd src/ai_brain
python quick_test.py

# Manual test
python -c "from brain import AIBrain; print(AIBrain().health_check())"
```

## Deployment

### Standalone
```python
# my_script.py
from brain import AIBrain
brain = AIBrain()
# Use brain...
```

### Flask API
```bash
pip install flask gunicorn
python api.py              # Development
gunicorn -w 4 api:app      # Production
```

### Docker
```bash
docker build -t ai-brain .
docker run -e GEMINI_API_KEY=$KEY -p 5000:5000 ai-brain
```

## Configuration

**.env file:**
```
GEMINI_API_KEY=your_key_here
LOG_LEVEL=INFO
CACHE_MAX_SIZE=1000
CACHE_TTL_HOURS=24
```

## Performance

| Task | Time | Notes |
|------|------|-------|
| Single (new) | 2-5s | API call |
| Single (cache) | <100ms | Cached |
| Batch 5 (new) | 10-25s | API calls |
| Batch 5 (cache) | <500ms | Cached |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Check .env file exists |
| "429 Quota exceeded" | Wait 1-2 minutes |
| "Parse error" | Check API response format |
| Slow response | Check cache hit rate |

## Documentation

- `GEMINI_SETUP.md` - Setup guide
- `TESTING.md` - Testing guide
- `DEPLOYMENT.md` - Deployment guide
- `AI_BRAIN_SUMMARY.md` - Full summary

## Files

```
src/ai_brain/
├── brain.py           ← Main module (import this)
├── gemini_client.py   ← API wrapper
├── chat_manager.py    ← Chat state
├── prompts.py         ← System prompts
├── error_handlers.py  ← Error handling
├── cache.py           ← Caching
├── logger.py          ← Logging
└── quick_test.py      ← Tests
```

## Key Concepts

**Sentiment Score:** -1 (negative) to +1 (positive)
**Controversy Level:** 1-10 scale
**Themes:** Top 3 topics from comments
**Cache Hit Rate:** % of requests from cache
**TTL:** Time before cache expires

## Common Patterns

**Process many comments:**
```python
comments = [...]
batch = brain.analyze_batch_comments(comments)
print(f"Avg sentiment: {batch['aggregated']['avg_sentiment']}")
```

**Interactive chat:**
```python
while True:
    msg = input("> ")
    response = brain.chat(msg)
    print(response)
```

**Monitor performance:**
```python
health = brain.health_check()
stats = brain.get_cache_stats()
print(f"Healthy: {health['status']}")
print(f"Cache hit rate: {stats['sentiment_cache']['hit_rate']}")
```

## Limits

- **Free API:** 5 requests/minute
- **Cache:** 1000 entries default
- **Input:** Max 10,000 chars per comment
- **Batch:** No hard limit

## Support

1. Check logs: `tail -f logs/ai_brain_*.log`
2. Run health: `brain.health_check()`
3. See docs: Read DEPLOYMENT.md
4. Test: `python quick_test.py`

---

**Status:** ✅ Production Ready
**Last Updated:** Jan 2026
