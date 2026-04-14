# Local Demo Development

This repository now contains a front-end/back-end separated demo app:

```text
frontend/  Vite + React + TypeScript
backend/   FastAPI + Python
```

The first demo runs on your Mac because the backend needs macOS `shortcuts sign` to produce importable `.shortcut` files.

## 1. Start The Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/api/health
```

## 2. Start The Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5174
```

## 3. Current Demo Behavior

The current implementation is a working skeleton:

- The React UI accepts a Shortcut name, target, and prompt.
- FastAPI creates a simple Shortcut plist that displays the submitted prompt.
- FastAPI validates the generated plist.
- FastAPI tries to sign the file with `shortcuts sign`.
- If `shortcuts sign` is unavailable or fails, the backend returns an unsigned fallback so the web flow can still be tested.

The next major step is replacing the demo plist builder with a real LLM-backed generator that uses the skill docs as retrieval/generation context.

## 4. Important Endpoints

```text
GET  /api/health
POST /api/shortcuts/generate
GET  /api/shortcuts/download/{job_id}
```

Example request:

```json
{
  "prompt": "Create a Shortcut that asks for my name and shows a greeting.",
  "name": "Greeting Shortcut",
  "target": "macOS"
}
```

## 5. Next Implementation Steps

Recommended order:

1. Add an LLM provider service.
2. Add a prompt builder that reads `SKILL.md`, `PLIST_FORMAT.md`, `ACTIONS.md`, `VARIABLES.md`, and `CONTROL_FLOW.md`.
3. Generate a structured intermediate plan before generating plist.
4. Add a repair loop when validation fails.
5. Add a job status endpoint if generation becomes slow.
