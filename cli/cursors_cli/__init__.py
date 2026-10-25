"""cursors-cli: build palette-specific Xscriptor-X Xcursor themes."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

__version__ = "0.1.0"

CLI_DIR = Path(__file__).resolve().parent
CLI_ROOT = CLI_DIR.parent
REPO_ROOT = CLI_ROOT.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def design_version() -> str:
    """Hash of the sources that shape the generated theme.

    Used by callers to invalidate caches when the artwork, catalogue or
    manifest rules change.
    """
    digest = hashlib.sha256()
    paths = (
        SCRIPTS_DIR / "art.py",
        SCRIPTS_DIR / "spec.py",
        CLI_DIR / "builder.py",
        CLI_DIR / "palette.py",
    )
    for path in paths:
        try:
            digest.update(path.read_bytes())
        except OSError:
            return "unknown"
        digest.update(b"\0")
    return digest.hexdigest()[:12]
