import logging
import shutil
import subprocess
from pathlib import Path

from app.services.settings import SHORTCUTS_SIGN_MODE

logger = logging.getLogger("signer")


def sign_shortcut(unsigned_path: Path, signed_path: Path) -> bool:
    shortcuts_bin = shutil.which("shortcuts")
    if shortcuts_bin is None:
        logger.warning("shortcuts CLI not found, copying unsigned file as fallback")
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
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=60)
        logger.info("shortcuts sign succeeded: %s", result.stdout.strip() or "(no output)")
        return True
    except subprocess.TimeoutExpired:
        logger.error("shortcuts sign timed out after 60s")
        raise RuntimeError("shortcuts sign timed out after 60 seconds")
    except subprocess.CalledProcessError as exc:
        logger.error("shortcuts sign failed (exit %d): %s", exc.returncode, exc.stderr.strip())
        raise RuntimeError(f"shortcuts sign failed: {exc.stderr.strip()}")
