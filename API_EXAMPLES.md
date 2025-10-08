# API Usage Examples

## Starting the API Server

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the API server
cd src
python api.py

# Or with custom port
python api.py --port 8080

# With auto-reload (development)
python api.py --reload
```

The server will start at `http://localhost:8000`

**Interactive Documentation**: http://localhost:8000/docs  
**Alternative Docs**: http://localhost:8000/redoc

---

## API Endpoints

### 1. Health Check

**GET** `/health`

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-08T12:34:56"
}
```

---

### 2. Solve Single Problem

**POST** `/solve`

**Request Body:**
```json
{
  "question": "What is the next number in the sequence: 2, 4, 6, 8, ?",
  "options": ["9", "10", "11", "12", "13"]
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the next number in the sequence: 2, 4, 6, 8, ?",
    "options": ["9", "10", "11", "12", "13"]
  }'
```

**Response:**
```json
{
  "predicted_answer": 2,
  "answer_text": "10",
  "confidence": 0.95,
  "reasoning": "This is an arithmetic sequence with a common difference of 2...",
  "category": "Sequence solving",
  "category_confidence": 0.92,
  "timestamp": "2025-10-08T12:34:56"
}
```

---

### 3. Batch Solve

**POST** `/batch-solve`

**Request Body:**
```json
[
  {
    "question": "What is 2 + 2?",
    "options": ["3", "4", "5", "6", "7"]
  },
  {
    "question": "What color is the sky?",
    "options": ["Red", "Blue", "Green", "Yellow", "Purple"]
  }
]
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/batch-solve \
  -H "Content-Type: application/json" \
  -d '[
    {
      "question": "What is 2 + 2?",
      "options": ["3", "4", "5", "6", "7"]
    },
    {
      "question": "If all A are B, and some B are C, can we say all A are C?",
      "options": ["Yes", "No", "Maybe", "Cannot determine", "Sometimes"]
    }
  ]'
```

**Response:**
```json
[
  {
    "predicted_answer": 2,
    "answer_text": "4",
    "confidence": 0.98,
    "reasoning": "2 + 2 equals 4...",
    "category": "Sequence solving",
    "category_confidence": 0.85,
    "timestamp": "2025-10-08T12:34:56"
  },
  {
    "predicted_answer": 2,
    "answer_text": "No",
    "confidence": 0.88,
    "reasoning": "This is a logical fallacy...",
    "category": "Logical traps",
    "category_confidence": 0.91,
    "timestamp": "2025-10-08T12:34:57"
  }
]
```

---

## Python Client Examples

### Using `requests`

```python
import requests

# Solve a problem
response = requests.post(
    "http://localhost:8000/solve",
    json={
        "question": "What is the next number: 2, 4, 6, 8, ?",
        "options": ["9", "10", "11", "12", "13"]
    }
)

result = response.json()
print(f"Answer: Option {result['predicted_answer']} - {result['answer_text']}")
print(f"Confidence: {result['confidence']:.1%}")
print(f"Reasoning: {result['reasoning']}")
```

### Using `httpx` (async)

```python
import httpx
import asyncio

async def solve_problem():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/solve",
            json={
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6", "7"]
            }
        )
        return response.json()

result = asyncio.run(solve_problem())
print(result)
```

---

## JavaScript Client Examples

### Using `fetch`

```javascript
fetch('http://localhost:8000/solve', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: "What is the next number: 2, 4, 6, 8, ?",
    options: ["9", "10", "11", "12", "13"]
  })
})
.then(response => response.json())
.then(data => {
  console.log('Answer:', data.answer_text);
  console.log('Confidence:', data.confidence);
  console.log('Reasoning:', data.reasoning);
});
```

### Using `axios`

```javascript
const axios = require('axios');

axios.post('http://localhost:8000/solve', {
  question: "What is 2 + 2?",
  options: ["3", "4", "5", "6", "7"]
})
.then(response => {
  const result = response.data;
  console.log(`Answer: Option ${result.predicted_answer} - ${result.answer_text}`);
  console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
})
.catch(error => console.error('Error:', error));
```

---

## Testing the API

### Using the Test Script

```bash
# Start API server (in one terminal)
cd src && python api.py

# Run test client (in another terminal)
python test_api.py
```

### Manual Testing

```bash
# Health check
curl http://localhost:8000/health

# Solve a problem
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "question": "A man builds a house with all four sides facing south. A bear walks by. What color is the bear?",
    "options": ["Black", "Brown", "White", "Grey", "No bears"]
  }'
```

---

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `predicted_answer` | integer | Answer option number (1-5) |
| `answer_text` | string | The actual text of the selected option |
| `confidence` | float | Confidence score (0.0 to 1.0) |
| `reasoning` | string | Detailed step-by-step reasoning |
| `category` | string | Detected problem category |
| `category_confidence` | float | Category classification confidence |
| `timestamp` | string | ISO format timestamp |

---

## Error Handling

### 400 Bad Request
```json
{
  "detail": "Expected exactly 5 options, got 3"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing request: ..."
}
```

### 503 Service Unavailable
```json
{
  "detail": "Pipeline not initialized"
}
```

---

## Production Deployment

### Using Gunicorn (Recommended)

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
cd src
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY ML\ Challenge\ Dataset/ ./ML\ Challenge\ Dataset/
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## Rate Limiting & Caching

For production use, consider:
- Rate limiting (e.g., 100 requests/minute)
- Response caching for identical questions
- Load balancing with multiple workers
- Async processing for batch requests

---

## Support

- **Interactive Docs**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/health

---

**Ready to use! Start the server and begin making requests! 🚀**

