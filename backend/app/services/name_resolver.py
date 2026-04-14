import re

from app.models.shortcuts import GenerateShortcutRequest

DEFAULT_SHORTCUT_NAME = "AI Shortcut"
GENERIC_NAMES = {
    "shortcut",
    "my shortcut",
    "generated shortcut",
    "new shortcut",
    "untitled shortcut",
    DEFAULT_SHORTCUT_NAME.lower(),
}


def resolve_shortcut_name(request: GenerateShortcutRequest, requirements_doc: str) -> str:
    if request.name and request.name.strip():
        return sanitize_shortcut_name(request.name)

    for pattern in (
        r"^##\s*0\.\s*Recommended Shortcut Name\s*\n+(.+)$",
        r"^0\.\s*Recommended Shortcut Name\s*\n+(.+)$",
        r"^0\.\s*Recommended Shortcut Name\s*:\s*(.+)$",
        r"^#*\s*Recommended Shortcut Name\s*\n+(.+)$",
        r"Recommended Shortcut Name\s*:\s*(.+)$",
    ):
        match = re.search(pattern, requirements_doc, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return sanitize_shortcut_name(match.group(1))

    return sanitize_shortcut_name(_name_from_prompt(request.prompt))


def apply_shortcut_name(shortcut: dict, name: str) -> dict:
    shortcut["WFWorkflowName"] = name
    return shortcut


def sanitize_shortcut_name(name: str) -> str:
    cleaned = re.sub(r"[*_`\"'“”‘’]", "", name).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.splitlines()[0].strip(" :-")

    if not cleaned or cleaned.lower() in GENERIC_NAMES:
        return DEFAULT_SHORTCUT_NAME

    return cleaned[:80]


def _name_from_prompt(prompt: str) -> str:
    words = re.findall(r"[\w\u4e00-\u9fff]+", prompt, flags=re.UNICODE)
    if not words:
        return DEFAULT_SHORTCUT_NAME

    candidate = " ".join(words[:5])
    return candidate.title()
