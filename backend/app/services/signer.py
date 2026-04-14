import shutil
import subprocess
from pathlib import Path

from app.services.settings import SHORTCUTS_SIGN_MODE


def sign_shortcut(unsigned_path: Path, signed_path: Path) -> bool:
    shortcuts_bin = shutil.which("shortcuts")
    if shortcuts_bin is None:
        shutil.copyfile(unsigned_path, signed_path)
        return False

    command = [
        shortcuts_bin,
        "sign",
        "--mode",
        SHORTCUTS_SIGN_MODE,
        "--input",
        str(unsigned_path),
        "--output",
        str(signed_path),
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        shutil.copyfile(unsigned_path, signed_path)
        return False

    return True
