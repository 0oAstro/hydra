# Quick Start Guide

## Setup (5 minutes)

### 1. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add API Keys

Create `.env` file in **project root** (not in frontend):

```bash
# In /Users/shaurya/Developer/hackathon/hydra/.env
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

Get keys:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys

### 3. Start Backend API

```bash
cd src
python api.py
```

Backend runs at `http://localhost:8000`

### 4. Install Frontend Dependencies

```bash
cd frotend
pnpm install
```

### 5. Start Frontend

```bash
pnpm dev
```

Frontend runs at `http://localhost:3000`

## How to Use

1. **Enter Question** (minimum 10 characters)
   - Example: "What is the next number: 2, 4, 6, 8, ?"

2. **Enter 5 Options** (exactly 5 required)
   - Example: 9, 10, 11, 12, 13

3. **Click "Solve"**
   - AI analyzes the question
   - Classifies the problem type
   - Returns answer with reasoning

## Example Problems

### Sequence Solving
- Question: "What comes next: 1, 4, 9, 16, 25, ?"
- Options: 30, 32, 36, 40, 49

### Spatial Reasoning
- Question: "A cube has how many edges?"
- Options: 6, 8, 10, 12, 14

### Logic Puzzles
- Question: "If all bloops are razzles and all razzles are lazzles, are all bloops lazzles?"
- Options: Yes, No, Maybe, Sometimes, Never

## Troubleshooting

### 422 Error (API Validation Failed)
- Question must be at least 10 characters
- Must provide exactly 5 options
- All fields required (no empty strings)

### Backend Not Starting
```bash
# Missing API key
echo "OPENAI_API_KEY=sk-..." > .env

# Install dependencies
pip install fastapi uvicorn langchain openai anthropic pandas scikit-learn python-dotenv
```

### Frontend Not Connecting
```bash
# Check backend is running on port 8000
curl http://localhost:8000/health

# Should return: {"status":"healthy","version":"1.0.0","timestamp":"..."}
```

## API Format

**Request:**
```json
{
  "question": "What is 2+2?",
  "options": ["3", "4", "5", "6", "7"]
}
```

**Response:**
```json
{
  "predicted_answer": 2,
  "answer_text": "4",
  "confidence": 0.95,
  "reasoning": "2+2 equals 4...",
  "category": "Sequence solving",
  "category_confidence": 0.87,
  "timestamp": "2025-10-08T12:34:56"
}
```

## Architecture

```
┌─────────────┐      HTTP POST      ┌──────────────┐
│   Next.js   │ ───────────────────> │   FastAPI    │
│  Frontend   │      /solve          │   Backend    │
│ :3000       │ <─────────────────── │   :8000      │
└─────────────┘      JSON            └──────────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │  LLM Agent   │
                                     │ GPT-4/Claude │
                                     └──────────────┘
```

1. Frontend collects question + 5 options
2. Sends to `/solve` endpoint
3. Backend classifies problem category
4. Routes to specialized LLM agent
5. Returns answer with reasoning
6. Frontend displays results

## Notes

- API keys go in **backend** `.env` file (project root)
- Frontend needs no API keys (it calls your backend)
- Backend must be running for frontend to work
- First run trains classifier (~30 seconds)
- Subsequent runs use cached model (instant)

