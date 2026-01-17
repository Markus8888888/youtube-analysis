# AI Brain Deployment Guide

## Overview
This guide covers deploying the AI Brain sentiment analysis system to production environments.

## Pre-Deployment Checklist

- [ ] API key obtained and verified
- [ ] Requirements installed (`pip install -r requirements.txt`)
- [ ] All tests passing (`python quick_test.py`)
- [ ] `.env` file created (NOT committed to git)
- [ ] `.gitignore` includes `.env`
- [ ] Logs directory exists or will be auto-created
- [ ] Python 3.8+ installed

## Environment Setup

### 1. Production Environment Variables

Create `.env` file in project root:

```env
# Required
GEMINI_API_KEY=your_production_api_key_here

# Optional (defaults shown)
LOG_LEVEL=INFO
CACHE_MAX_SIZE=1000
CACHE_TTL_HOURS=24
BATCH_CACHE_TTL_HOURS=48
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Optional: Pin exact versions for reproducibility
pip freeze > requirements-lock.txt
```

### 3. Verify Installation

```bash
cd src/ai_brain
python -c "from brain import AIBrain; print('Import successful')"
```

## Deployment Options

### Option 1: Standalone Script (Simple)

**For batch processing or scheduled jobs:**

```python
# my_analysis_script.py
import sys
sys.path.insert(0, 'src')

from ai_brain.brain import AIBrain

brain = AIBrain()
comments = ["Great!", "Bad audio", "Amazing"]
result = brain.full_analysis(comments)
print(result)
```

Run:
```bash
python my_analysis_script.py
```

### Option 2: REST API (Flask)

**For web applications:**

```python
# api.py
from flask import Flask, request, jsonify
import sys
sys.path.insert(0, 'src')

from ai_brain.brain import AIBrain
from ai_brain.logger import setup_logging

app = Flask(__name__)
logger = setup_logging(__name__)
brain = AIBrain()

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze comments"""
    try:
        data = request.json
        comments = data.get('comments', [])
        
        if not comments:
            return {'error': 'No comments provided'}, 400
        
        result = brain.analyze_batch_comments(comments)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return {'error': str(e)}, 500

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return {'error': 'No message provided'}, 400
        
        response = brain.chat(message)
        return jsonify({'response': response})
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return {'error': str(e)}, 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    health = brain.health_check()
    status_code = 200 if health['status'] == 'healthy' else 503
    return jsonify(health), status_code

@app.route('/cache/stats', methods=['GET'])
def cache_stats():
    """Get cache statistics"""
    stats = brain.get_cache_stats()
    return jsonify(stats)

if __name__ == '__main__':
    # Use gunicorn in production:
    # gunicorn -w 4 -b 0.0.0.0:5000 api:app
    
    app.run(host='0.0.0.0', port=5000, debug=False)
```

Install Flask:
```bash
pip install flask gunicorn
```

Run locally:
```bash
python api.py
```

Run in production with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

### Option 3: Docker Deployment

**For containerized deployment:**

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.ai_brain.brain import AIBrain; brain = AIBrain(); print(brain.health_check())"

# Run API
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  ai-brain:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Build and run:
```bash
docker build -t ai-brain .
docker run -e GEMINI_API_KEY=your_key -p 5000:5000 ai-brain

# Or with docker-compose:
GEMINI_API_KEY=your_key docker-compose up
```

## Production Configuration

### 1. Logging

Logs are automatically saved to `logs/` directory:
- `ai_brain_brain.log` - Main operations
- `ai_brain_cache.log` - Cache operations
- `ai_brain_errors.log` - Error tracking

For production, monitor logs:

```bash
# Follow logs in real-time
tail -f logs/ai_brain_brain.log

# Search for errors
grep ERROR logs/ai_brain_errors.log

# Rotate logs (Linux)
logrotate -f /etc/logrotate.d/ai-brain
```

### 2. Caching Strategy

Production caching configuration:

```python
# Increase cache for high-traffic scenarios
brain = AIBrain()

# Check cache effectiveness
stats = brain.get_cache_stats()
print(f"Cache hit rate: {stats['sentiment_cache']['hit_rate']}")

# Clear cache if needed
brain.clear_caches()
```

### 3. Rate Limiting

**Free Tier:** 5 requests/minute per model
**Paid Plans:** Higher limits available

Handle rate limits gracefully:

```python
# The brain.py includes automatic retry logic
# with exponential backoff for quota exceeded errors

# To add custom rate limiting:
from functools import wraps
import time

def rate_limit(calls_per_minute=5):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
```

### 4. Error Monitoring

Production error handling:

```python
from ai_brain.error_handlers import handle_api_error
from ai_brain.logger import setup_logging

logger = setup_logging("production")

try:
    result = brain.analyze_comments(comment)
except Exception as e:
    error_response = handle_api_error(e)
    logger.error(f"Analysis failed: {error_response}")
    # Send alert to monitoring system
    send_alert(error_response)
```

## Scaling Considerations

### Horizontal Scaling

For high-volume deployments:

```python
# 1. Use process pool for parallel analysis
from concurrent.futures import ProcessPoolExecutor
from ai_brain.brain import AIBrain

def analyze_batch(comments_batch):
    brain = AIBrain()
    return brain.analyze_batch_comments(comments_batch)

# Split work across processes
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(analyze_batch, batches))
```

### Vertical Scaling

Optimize single instance:

```python
# 1. Increase cache size for more hits
cache.max_size = 5000

# 2. Batch processing
# Analyze 100 comments at once instead of individual calls

# 3. Use connection pooling for API calls
# Already built-in to genai library
```

### Load Balancing

For API deployments:

```bash
# Use load balancer (nginx example)
upstream ai_brain {
    server localhost:5001;
    server localhost:5002;
    server localhost:5003;
}

server {
    listen 80;
    location / {
        proxy_pass http://ai_brain;
    }
}
```

## Monitoring & Health Checks

### Health Check Endpoint

```python
# GET /health
# Returns: {"status": "healthy", ...}

# Usage
import requests
response = requests.get('http://localhost:5000/health')
if response.status_code == 200:
    print("System is healthy")
```

### Metrics to Monitor

1. **Cache Hit Rate**
   ```python
   stats = brain.get_cache_stats()
   hit_rate = stats['sentiment_cache']['hit_rate']
   ```

2. **API Response Time**
   - Track in logs: `duration_ms`
   - Alert if > 10 seconds

3. **Error Rate**
   - Monitor `logs/ai_brain_errors.log`
   - Alert if errors exceed threshold

4. **Cache Size**
   - Monitor cache growth
   - Implement cleanup for expired entries

## Troubleshooting Production Issues

### Issue: "GEMINI_API_KEY not found"

**Solution:**
```bash
# Verify .env file exists and is readable
ls -la .env

# Check environment variable
echo $GEMINI_API_KEY

# Reload .env
source .env
```

### Issue: "429 Quota exceeded"

**Solution:**
- Implement request queuing
- Use cached results more aggressively
- Upgrade API plan
- Batch requests intelligently

### Issue: High Memory Usage

**Solution:**
```python
# Reduce cache size
cache.max_size = 100

# Clear cache periodically
import schedule
schedule.every(1).hours.do(brain.clear_caches)
```

### Issue: Slow Response Times

**Solution:**
```python
# Monitor response times
import time
start = time.time()
result = brain.analyze_comments(text)
duration = time.time() - start
logger.info(f"Response time: {duration:.2f}s")

# If slow:
# 1. Check API quota
# 2. Increase cache hits
# 3. Use batch processing
```

## Security Considerations

### API Key Management

```bash
# Never commit .env
echo ".env" >> .gitignore
echo "logs/" >> .gitignore

# Use secrets manager in production
# AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, etc.
```

### Input Validation

```python
# Already implemented in error_handlers.py
from ai_brain.error_handlers import validate_input

try:
    validate_input(user_input, min_length=1, max_length=10000)
except ValueError as e:
    logger.warning(f"Invalid input: {e}")
```

### Rate Limiting (Security)

```python
# Prevent abuse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/analyze', methods=['POST'])
@limiter.limit("100 per hour")
def analyze():
    # ...
```

## Backup & Recovery

### Backup Logs

```bash
# Backup logs daily
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/

# Upload to cloud storage
gsutil cp logs_backup_*.tar.gz gs://my-bucket/
```

### Cache Recovery

```python
# Cache is automatically rebuilt on restart
# No recovery needed - cache misses will refetch from API
```

### Configuration Backup

```bash
# Backup .env (encrypted)
gpg -c .env
# Restore: gpg -d .env.gpg > .env
```

## Maintenance Tasks

### Weekly
- [ ] Review error logs
- [ ] Check cache hit rate
- [ ] Verify health checks pass
- [ ] Monitor API quota usage

### Monthly
- [ ] Update dependencies (`pip list --outdated`)
- [ ] Review and optimize slow queries
- [ ] Analyze performance trends
- [ ] Test failover/backup procedures

### Quarterly
- [ ] Update Python version if needed
- [ ] Security audit
- [ ] Capacity planning review
- [ ] Disaster recovery drill

## Performance Benchmarks

Expected performance in production:

| Operation | Time | Notes |
|-----------|------|-------|
| Single comment (first) | 2-5s | API call |
| Single comment (cached) | <100ms | From cache |
| Batch (5 comments) | 10-25s | Sequential API calls |
| Batch (5 cached) | <500ms | All from cache |
| Health check | <3s | Full system check |

## Support & Maintenance

### Get Help

1. Check logs: `tail -f logs/ai_brain_*.log`
2. Run health check: `brain.health_check()`
3. Review error handlers: `src/ai_brain/error_handlers.py`
4. Check API status: `https://ai.google.dev/gemini-api/docs`

### Report Issues

Include:
- Error message/traceback
- Relevant logs
- Input that caused issue
- Environment info (Python version, OS)
- Steps to reproduce

## Next Steps

After deployment:
1. ✅ Monitor metrics for 24 hours
2. ✅ Optimize cache settings based on hit rate
3. ✅ Set up alerting for errors
4. ✅ Document any custom changes
5. ✅ Plan scaling strategy

## Rollback Procedure

If deployment fails:

```bash
# 1. Stop current version
docker stop ai-brain

# 2. Revert to previous version
git checkout previous_version

# 3. Reinstall dependencies
pip install -r requirements.txt

# 4. Restart
docker run -d -e GEMINI_API_KEY=$KEY ai-brain

# 5. Verify health
curl http://localhost:5000/health
```

---

**Deployment complete!** Monitor logs and metrics. Good luck! 🚀
