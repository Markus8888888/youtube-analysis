# Testing the AI Brain

## Quick Start

Run the quick test suite:

```bash
cd src/ai_brain
python quick_test.py
```

This runs 7 comprehensive tests covering all AI Brain features.

## Test Suite Overview

### Test 1: Health Check
Verifies all components are operational
- Checks sentiment analysis
- Checks chatbot
- Checks API key configuration

### Test 2: Single Comment Analysis
Tests sentiment analysis on individual comments
- Analyzes positive comments
- Analyzes negative comments
- Analyzes neutral comments

Expected output:
```
Comment: 'This is amazing!'
  Sentiment: 0.95
  Themes: ['quality', 'positive', ...]
  Controversy: 1/10
```

### Test 3: Caching System
Verifies caching reduces API calls
- Makes first API call (cache miss)
- Makes second identical call (cache hit)
- Shows cache statistics

Expected output:
```
Cache stats: {
  'size': 1,
  'hits': 1,
  'misses': 0,
  'hit_rate': '100.0%'
}
```

### Test 4: Chatbot Conversation
Tests multi-turn conversation
- Sends multiple messages
- Maintains conversation history
- Returns natural responses

### Test 5: Batch Analysis
Analyzes multiple comments at once
- Aggregates sentiment
- Tracks themes
- Calculates averages

Expected output:
```
Avg Sentiment: 0.65
Avg Controversy: 2.5/10
Analyzed: 5/5 comments
Top themes: {...}
```

### Test 6: Query Categorization
Routes user queries to appropriate analysis type
- sentiment_analysis
- engagement_analysis
- content_analysis
- general

### Test 7: Full Pipeline
Complete end-to-end analysis
- Analyzes all comments
- Aggregates results
- Generates insights

## Manual Testing

### Test Individual Features

**Sentiment Analysis:**
```python
from brain import AIBrain

brain = AIBrain()
result = brain.analyze_comments("Great video!")
print(result)
```

**Batch Analysis:**
```python
comments = ["Great!", "Bad audio", "Interesting"]
result = brain.analyze_batch_comments(comments)
print(result['aggregated'])
```

**Chatbot:**
```python
response = brain.chat("How can I improve engagement?")
print(response)
```

**Cache Stats:**
```python
stats = brain.get_cache_stats()
print(stats)
```

**Clear Cache:**
```python
brain.clear_caches()
```

## Troubleshooting

### "GEMINI_API_KEY not found"
- Check `.env` file exists in project root
- Verify format: `GEMINI_API_KEY=your_key_here`
- Restart Python interpreter

### "429 Quota exceeded"
- Free tier has 5 requests/minute limit
- Wait 1-2 minutes before running tests again
- Consider using cached results

### "Error: Failed to parse AI response"
- API may have returned unexpected format
- Check API is working with health check
- Verify API key is valid

### "Chat response seems empty or slow"
- First chat call may be slower (no cache)
- Wait for rate limit reset if quota exceeded
- Check internet connection

## Performance Expectations

**Sentiment Analysis:**
- First call: 2-5 seconds (API call)
- Cached call: <100ms (from cache)

**Batch Analysis (5 comments):**
- 10-25 seconds total (5 sequential API calls)
- With cache hits: Much faster

**Chatbot:**
- First message: 2-4 seconds
- Subsequent messages: 2-4 seconds (maintains history)

## What Gets Logged

Logs are saved to `logs/` directory:
- `ai_brain_brain.log` - Main brain operations
- `ai_brain_gemini_client.log` - API calls
- `ai_brain_cache.log` - Cache operations
- `ai_brain_errors.log` - Error tracking

Check logs for debugging:
```bash
tail -f logs/ai_brain_brain.log
```

## Success Criteria

All tests should show `[PASS]`:
```
[PASS]: Health Check
[PASS]: Single Comment Analysis
[PASS]: Caching System
[PASS]: Chatbot
[PASS]: Batch Analysis
[PASS]: Query Categorization
[PASS]: Full Pipeline

Total: 7/7 tests passed
```

## Next Steps

Once tests pass:
1. Integrate with YouTube API for real data
2. Connect to frontend/dashboard
3. Deploy to production
4. Monitor logs and metrics

## Support

For issues:
1. Check logs in `logs/` directory
2. Run health check: `brain.health_check()`
3. Review error messages carefully
4. Check `.env` file configuration
