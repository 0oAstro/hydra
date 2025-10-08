# API Quick Start Guide

## 🚀 Get the API Running in 60 Seconds

### Step 1: Install Dependencies
```bash
pip install fastapi uvicorn requests
```

### Step 2: Start the API Server
```bash
cd src
python api.py
```

You'll see:
```
ML REASONING SYSTEM API
Starting server on http://0.0.0.0:8000
API Documentation: http://0.0.0.0:8000/docs
```

### Step 3: Test It!

**Open your browser**: http://localhost:8000/docs

Or use curl:
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is 2+2?",
    "options": ["3", "4", "5", "6", "7"]
  }'
```

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/solve` | POST | Solve single problem |
| `/batch-solve` | POST | Solve multiple problems |
| `/docs` | GET | Interactive documentation |

---

## 💡 Simple Examples

### Python
```python
import requests

response = requests.post(
    'http://localhost:8000/solve',
    json={
        'question': 'What is the next number: 2, 4, 6, 8, ?',
        'options': ['9', '10', '11', '12', '13']
    }
)

result = response.json()
print(f"Answer: {result['answer_text']}")
print(f"Reasoning: {result['reasoning']}")
```

### JavaScript/Node.js
```javascript
fetch('http://localhost:8000/solve', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: "What is 2+2?",
    options: ["3", "4", "5", "6", "7"]
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{"question":"What is 2+2?","options":["3","4","5","6","7"]}'
```

---

## 🎯 Request/Response Format

### Request
```json
{
  "question": "Your question here",
  "options": [
    "Option 1",
    "Option 2", 
    "Option 3",
    "Option 4",
    "Option 5"
  ]
}
```

### Response
```json
{
  "predicted_answer": 2,
  "answer_text": "Option 2",
  "confidence": 0.95,
  "reasoning": "Detailed explanation...",
  "category": "Sequence solving",
  "category_confidence": 0.92,
  "timestamp": "2025-10-08T12:34:56"
}
```

---

## 🧪 Test Scripts Included

### Quick Test (Python)
```bash
python test_api.py
```

### Example Usage
```bash
python example_api_usage.py
```

---

## 📚 Full Documentation

- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **Detailed Examples**: [API_EXAMPLES.md](API_EXAMPLES.md)

---

## 🔧 Advanced Options

### Custom Port
```bash
python api.py --port 8080
```

### Development Mode (Auto-reload)
```bash
python api.py --reload
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn src.api:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## ✅ Verify It's Working

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "..."
}
```

---

## 🎉 You're Ready!

The API is now running and ready to solve reasoning problems!

**Next steps:**
1. Visit http://localhost:8000/docs for interactive testing
2. Run `python example_api_usage.py` for examples
3. See [API_EXAMPLES.md](API_EXAMPLES.md) for more

---

**Questions?** Check the full documentation in [API_EXAMPLES.md](API_EXAMPLES.md)

