# AI Service (AI Developer 1)

Flask microservice for Tool-103. Exposes AI endpoints on port `5000`.

## Setup

### 1) Create `.env`

Create `ai-service/.env`:

- `GROQ_API_KEY` = your Groq key
- `GROQ_MODEL` (optional) = `llama-3.3-70b-versatile`
- `GROQ_BASE_URL` (optional) = `https://api.groq.com/openai/v1`
- `GROQ_TIMEOUT_S` (optional) = `10`
- `PORT` (optional) = `5000`

### 2) Install deps

```bash
py -m pip install -r requirements.txt
```

### 3) Run

```bash
py app.py
```

Health check: `http://localhost:5000/health`

## API

### POST `/describe`
Request:
```json
{ "input": "..." }
```

Response:
```json
{
  "generated_at": 0,
  "elapsed_ms": 0,
  "is_fallback": false,
  "description": {
    "title": "string",
    "summary": "string",
    "key_risks": ["string", "string", "string"]
  }
}
```

### POST `/recommend`
Request:
```json
{ "input": "..." }
```

Response:
```json
{
  "generated_at": 0,
  "elapsed_ms": 0,
  "is_fallback": false,
  "recommendations": [
    { "action_type": "string", "description": "string", "priority": "LOW|MEDIUM|HIGH" }
  ]
}
```

