import plistlib
from pathlib import Path
from uuid import uuid4


def build_demo_shortcut_plist(name: str, prompt: str) -> dict:
    text_uuid = str(uuid4()).upper()
    message = (
        f"{name}\n\n"
        "This demo Shortcut was generated from your prompt:\n\n"
        f"{prompt.strip()}"
    )

    return {
        "WFWorkflowActions": [
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
                "WFWorkflowActionParameters": {
                    "UUID": text_uuid,
                    "WFTextActionText": message,
                },
            },
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.showresult",
                "WFWorkflowActionParameters": {
                    "Text": {
                        "WFSerializationType": "WFTextTokenString",
                        "Value": {
                            "string": "\ufffc",
                            "attachmentsByRange": {
                                "{0, 1}": {
                                    "Type": "ActionOutput",
                                    "OutputName": "Text",
                                    "OutputUUID": text_uuid,
                                }
                            },
                        },
                    }
                },
            },
        ],
        "WFWorkflowClientVersion": "2700.0.4",
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowIcon": {
            "WFWorkflowIconGlyphNumber": 59511,
            "WFWorkflowIconStartColor": 4282601983,
        },
        "WFWorkflowImportQuestions": [],
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowName": name,
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowTypes": [],
    }


def write_shortcut_plist(shortcut: dict, output_path: Path) -> None:
    with output_path.open("wb") as file:
        plistlib.dump(shortcut, file, fmt=plistlib.FMT_XML, sort_keys=False)
