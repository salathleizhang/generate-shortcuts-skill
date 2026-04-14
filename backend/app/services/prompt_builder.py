from dataclasses import dataclass

from app.models.shortcuts import GenerateShortcutRequest
from app.services.settings import REPO_ROOT

KNOWLEDGE_DOCS = [
    "SKILL.md",
    "PLIST_FORMAT.md",
    "ACTIONS.md",
    "APPINTENTS.md",
    "PARAMETER_TYPES.md",
    "VARIABLES.md",
    "CONTROL_FLOW.md",
    "FILTERS.md",
    "EXAMPLES.md",
]


@dataclass(frozen=True)
class BuiltPrompt:
    prompt: str
    context_manifest: str


def build_requirements_prompt(request: GenerateShortcutRequest) -> BuiltPrompt:
    context = _build_context_bundle()

    prompt = f"""
You are a senior product designer and Apple Shortcuts automation architect.

Before generating a Shortcut, write a complete implementation requirements document.

Shortcut name:
{_display_name(request)}

Target platform:
{request.target}

User request:
{request.prompt.strip()}

Your task:
- Understand the user goal deeply.
- Identify missing or ambiguous details.
- Make reasonable MVP assumptions instead of asking follow-up questions.
- Convert the user request into a clear Shortcut behavior spec.
- Choose reliable Apple Shortcuts actions from the provided documentation.
- Explain the action-by-action plan in execution order.
- Define variable flow and expected user inputs/outputs.
- Call out unsupported or risky parts and propose safe fallbacks.
- Keep the first implementation practical and importable.

Output format:
- Markdown only.
- Use these sections exactly:
  0. Recommended Shortcut Name: <one concise name>
  1. Goal
  2. User Experience
  3. Assumptions
  4. Shortcut Inputs
  5. Shortcut Outputs
  6. Action Plan
  7. Variables And Data Flow
  8. Error Handling
  9. Unsupported Or Risky Behavior
  10. Generation Instructions

In "Recommended Shortcut Name", provide one concise, user-facing shortcut name based on the request on the same line as the heading. Do not use generic names like "Shortcut", "My Shortcut", or "Generated Shortcut".
In "Generation Instructions", write precise instructions for a plist generator. Include action identifiers when you are confident.

Reference documentation:
{context.docs}
""".strip()

    return BuiltPrompt(prompt=prompt, context_manifest=context.manifest)


def build_shortcut_prompt(request: GenerateShortcutRequest, requirements_doc: str) -> BuiltPrompt:
    context = _build_context_bundle()

    prompt = f"""
You are an expert Apple Shortcuts plist generator.

Create an Apple Shortcuts workflow as strict JSON. The backend will convert your JSON to plist.

Use the requirements document as the source of truth. Do not silently ignore its action plan.

Shortcut name:
{_display_name(request)}

Target platform:
{request.target}

Original user request:
{request.prompt.strip()}

Generated requirements document:
{requirements_doc}

Hard output rules:
- Output only raw JSON.
- Do not include Markdown fences.
- Do not include explanations before or after the JSON.
- The JSON root must be an object that can be directly serialized to an Apple Shortcuts plist.
- Include "WFWorkflowActions" as a non-empty array.
- Include "WFWorkflowClientVersion", "WFWorkflowIcon", "WFWorkflowMinimumClientVersion", "WFWorkflowMinimumClientVersionString", "WFWorkflowName", "WFWorkflowImportQuestions", "WFWorkflowOutputContentItemClasses", and "WFWorkflowTypes".
- Every action must contain "WFWorkflowActionIdentifier" and "WFWorkflowActionParameters".
- Any UUID value must be uppercase.
- Variable references must use "WFTextTokenString" with the object replacement character U+FFFC.
- Use JSON booleans true/false and numbers, not strings, for plist booleans and integers.
- Escape the object replacement character as "\\ufffc" if needed.
- Prefer reliable built-in actions from the provided documentation.
- If the request is too complex, generate the closest safe shortcut using supported built-in actions instead of inventing unsupported identifiers.
- Do not use actions that delete files, delete photos, send messages, make purchases, or perform destructive actions unless the user explicitly asked for them.

Minimal JSON shape:
{{
  "WFWorkflowActions": [
    {{
      "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
      "WFWorkflowActionParameters": {{
        "UUID": "11111111-1111-1111-1111-111111111111",
        "WFTextActionText": "Hello"
      }}
    }}
  ],
  "WFWorkflowClientVersion": "2700.0.4",
  "WFWorkflowHasOutputFallback": false,
  "WFWorkflowIcon": {{
    "WFWorkflowIconGlyphNumber": 59511,
    "WFWorkflowIconStartColor": 4282601983
  }},
  "WFWorkflowImportQuestions": [],
  "WFWorkflowMinimumClientVersion": 900,
  "WFWorkflowMinimumClientVersionString": "900",
  "WFWorkflowName": "{_display_name(request)}",
  "WFWorkflowOutputContentItemClasses": [],
  "WFWorkflowTypes": []
}}

Reference documentation:
{context.docs}
""".strip()

    return BuiltPrompt(prompt=prompt, context_manifest=context.manifest)


@dataclass(frozen=True)
class ContextBundle:
    docs: str
    manifest: str


def _build_context_bundle() -> ContextBundle:
    loaded_docs = [_load_doc(name) for name in KNOWLEDGE_DOCS]
    docs = "\n\n".join(item[0] for item in loaded_docs)
    total_chars = sum(item[1] for item in loaded_docs)

    manifest_lines = [
        "# Prompt Context Manifest",
        "",
        "The backend fully loaded these knowledge files for this generation.",
        "",
        "| File | Characters | Status |",
        "|---|---:|---|",
    ]

    for filename, char_count, status in ((item[2], item[1], item[3]) for item in loaded_docs):
        manifest_lines.append(f"| `{filename}` | {char_count} | {status} |")

    manifest_lines.extend(
        [
            "",
            f"Total knowledge context characters: {total_chars}",
            "",
            "Current strategy: load the complete curated Shortcuts knowledge base into both Gemini calls.",
            "No file is truncated by prompt_builder.py.",
        ]
    )

    return ContextBundle(docs=docs, manifest="\n".join(manifest_lines) + "\n")


def _load_doc(filename: str) -> tuple[str, int, str, str]:
    path = REPO_ROOT / filename
    if not path.exists():
        return f"## {filename}\nMissing.", 0, filename, "missing"

    content = path.read_text(encoding="utf-8", errors="replace")
    return f"## {filename}\n{content}", len(content), filename, "full"


def _display_name(request: GenerateShortcutRequest) -> str:
    if request.name and request.name.strip():
        return request.name.strip()

    return "Generate an appropriate concise name from the user request."
