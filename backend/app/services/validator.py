import plistlib
from pathlib import Path


REQUIRED_ROOT_KEYS = {
    "WFWorkflowActions",
    "WFWorkflowClientVersion",
    "WFWorkflowIcon",
    "WFWorkflowMinimumClientVersion",
    "WFWorkflowMinimumClientVersionString",
}


def validate_shortcut_file(path: Path) -> None:
    try:
        with path.open("rb") as file:
            shortcut = plistlib.load(file)
    except Exception as exc:
        raise ValueError("Generated file is not a valid plist.") from exc

    missing_keys = REQUIRED_ROOT_KEYS - shortcut.keys()
    if missing_keys:
        missing = ", ".join(sorted(missing_keys))
        raise ValueError(f"Shortcut plist is missing required keys: {missing}.")

    actions = shortcut.get("WFWorkflowActions")
    if not isinstance(actions, list) or not actions:
        raise ValueError("Shortcut plist must contain at least one workflow action.")

    seen_uuids: set[str] = set()
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            raise ValueError(f"Action {index} must be a dictionary.")

        identifier = action.get("WFWorkflowActionIdentifier")
        parameters = action.get("WFWorkflowActionParameters")

        if not isinstance(identifier, str) or not identifier:
            raise ValueError(f"Action {index} is missing WFWorkflowActionIdentifier.")

        if not isinstance(parameters, dict):
            raise ValueError(f"Action {index} is missing WFWorkflowActionParameters.")

        uuid = parameters.get("UUID")
        if uuid is not None:
            if not isinstance(uuid, str) or uuid != uuid.upper():
                raise ValueError(f"Action {index} has an invalid UUID.")
            if uuid in seen_uuids:
                raise ValueError(f"Action {index} reuses UUID {uuid}.")
            seen_uuids.add(uuid)
