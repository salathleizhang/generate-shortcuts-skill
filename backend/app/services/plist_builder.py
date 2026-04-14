import plistlib
from pathlib import Path


def write_shortcut_plist(shortcut: dict, output_path: Path) -> None:
    with output_path.open("wb") as file:
        plistlib.dump(shortcut, file, fmt=plistlib.FMT_XML, sort_keys=False)
