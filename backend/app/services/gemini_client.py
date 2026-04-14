import json

from app.services.settings import GEMINI_API_KEY, GEMINI_MODEL


def generate_requirements_document(prompt: str) -> str:
    text = _generate_content(
        prompt=prompt,
        response_mime_type="text/plain",
        temperature=0.25,
    )
    return strip_markdown_fence(text).strip()


def generate_shortcut_plist(prompt: str) -> dict:
    text = _generate_content(
        prompt=prompt,
        response_mime_type="application/json",
        temperature=0.12,
    )
    return extract_json_object(text)


def _generate_content(prompt: str, response_mime_type: str, temperature: float) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set. Add it to your backend environment.")

    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is not installed. Run `pip install -r requirements.txt` in backend."
        ) from exc

    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": temperature,
                "top_p": 0.9,
                "max_output_tokens": 32768,
                "response_mime_type": response_mime_type,
            },
        )
    except Exception as exc:
        raise RuntimeError(f"Gemini API request failed for model {GEMINI_MODEL}: {exc}") from exc

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text


def extract_json_object(text: str) -> dict:
    stripped = strip_markdown_fence(text)

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise RuntimeError("Gemini response did not contain a JSON object.")

    try:
        parsed = json.loads(stripped[start : end + 1])
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Gemini returned invalid JSON: {exc.msg}.") from exc

    if not isinstance(parsed, dict):
        raise RuntimeError("Gemini JSON root must be an object.")

    return parsed


def strip_markdown_fence(text: str) -> str:
    stripped = text.strip()

    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()

    return stripped
