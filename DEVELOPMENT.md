# Local Demo Development

This repository now contains a front-end/back-end separated demo app:

```text
frontend/  Vite + React + TypeScript
backend/   FastAPI + Python
```

The first demo runs on your Mac because the backend needs macOS `shortcuts sign` to produce importable `.shortcut` files.

## 1. Start The Backend

Create a local environment file:

```bash
cd backend
cp .env.example .env
```

Then edit `.env`:

```bash
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3-pro-preview
```

Install and start:

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
- FastAPI fully loads the curated skill docs listed in `backend/app/services/prompt_builder.py`.
- FastAPI calls Gemini once to create a requirements document.
- FastAPI calls Gemini again to generate Shortcut JSON from that requirements document.
- FastAPI validates the generated plist.
- FastAPI tries to sign the file with `shortcuts sign`.
- If `shortcuts sign` is unavailable or fails, the backend returns an unsigned fallback so the web flow can still be tested.

If `GEMINI_API_KEY` is not configured, generation requests fail with a clear backend error instead of using the old placeholder generator.

Each generation stores:

- `requirements.md`: the generated requirements and implementation plan.
- `context_manifest.md`: the list of knowledge files included in the Gemini prompt, including character counts and truncation status.

The current context strategy is intentionally simple: load the complete curated Shortcuts knowledge base and do not truncate it. If the docs grow too large later, the next step should be retrieval-based context selection instead of blind truncation.

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
