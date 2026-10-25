#!/usr/bin/env python3
"""Validate the generated/installed cursor themes.

Checks:
  * every cursor name shipped by the system themes exists (no functional gap),
  * every entry is either a valid XCursor or a symlink that resolves,
  * every image has a hotspot inside its bitmap,
  * animated cursors really carry multiple frames.

Run after building: python3 scripts/validate.py
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    "Xscriptor-X": ROOT / "build" / "themes" / "Xscriptor-X",
    "Xscriptor-Berlin": ROOT / "build" / "themes" / "Xscriptor-Berlin",
}
SYSTEM_ICONS = Path("/usr/share/icons")
METADATA = {".directory", "xcursorconfig"}
ANIMATED = {"wait", "left_ptr_watch"}
CURSORFONT = """
arrow based_arrow_down based_arrow_up boat bogosity bottom_left_corner
bottom_right_corner bottom_side bottom_tee box_spiral center_ptr circle clock
coffee_mug cross cross_reverse crosshair diamond_cross dot dotbox double_arrow
draft_large draft_small draped_box exchange fleur gobbler gumby hand heart icon
iron_cross left_ptr left_side left_tee leftbutton ll_angle lr_angle man
middlebutton mouse pencil pirate plus question_arrow right_ptr right_side
right_tee rightbutton rtl_logo sailboat sb_down_arrow sb_h_double_arrow
sb_left_arrow sb_right_arrow sb_up_arrow sb_v_double_arrow shuttle sizing
spider spraycan star target tcross top_left_arrow top_left_corner
top_right_corner top_side top_tee trek ul_angle umbrella ur_angle watch xterm
""".split()


def system_cursor_names() -> set[str]:
    names: set[str] = set()
    for theme in SYSTEM_ICONS.iterdir():
        cursors = theme / "cursors"
        if cursors.is_dir():
            names |= {entry.name for entry in cursors.iterdir()}
    return names - METADATA


def parse_xcursor(path: Path) -> tuple[set[int], int, list[str]]:
    data = path.read_bytes()
    if data[:4] != b"Xcur":
        return set(), 0, ["not an XCursor file"]
    _, _, _, ntoc = struct.unpack("<4sIII", data[:16])
    sizes: set[int] = set()
    frames = 0
    problems: list[str] = []
    for i in range(ntoc):
        kind, _, pos = struct.unpack("<III", data[16 + i * 12: 28 + i * 12])
        if kind != 0xFFFD0002:  # image chunk
            continue
        _, _, nominal, _, width, height, xhot, yhot, _ = struct.unpack(
            "<IIIIIIIII", data[pos: pos + 36]
        )
        frames += 1
        sizes.add(nominal)
        if not (0 <= xhot < width and 0 <= yhot < height):
            problems.append(f"hotspot {xhot},{yhot} outside {width}x{height}")
    if not sizes:
        problems.append("no images")
    return sizes, frames, problems


def check_theme(theme: str, path: Path, expected: set[str]) -> list[str]:
    issues: list[str] = []
    cursors = path / "cursors"
    if not (path / "index.theme").is_file():
        issues.append("missing index.theme")
    if not (path / "cursor.theme").is_file():
        issues.append("missing cursor.theme")
    if not cursors.is_dir():
        return issues + [f"missing cursors directory: {cursors}"]

    entries = {entry.name for entry in cursors.iterdir()}
    for name in sorted(expected - entries):
        issues.append(f"missing cursor: {name}")
    for name in sorted(set(CURSORFONT) - entries):
        issues.append(f"missing cursorfont glyph: {name}")

    for entry in cursors.iterdir():
        if entry.is_symlink():
            if not entry.exists():
                issues.append(f"broken symlink: {entry.name}")
            continue
        sizes, frames, problems = parse_xcursor(entry)
        for problem in problems:
            issues.append(f"{entry.name}: {problem}")
        if entry.name in ANIMATED and frames <= 1:
            issues.append(f"{entry.name}: expected animation, got {frames} frame(s)")
        if len(sizes) < 5:
            issues.append(f"{entry.name}: only {len(sizes)} size(s)")

    print(f"{theme}: {len(entries)} entries")
    return issues


def main() -> int:
    expected = system_cursor_names()
    print(
        f"reference: {len(expected)} names from {SYSTEM_ICONS} "
        f"+ {len(CURSORFONT)} X11 cursorfont glyphs"
    )

    failed = False
    for theme, path in THEMES.items():
        if not path.is_dir():
            print(f"{theme}: not built ({path})")
            failed = True
            continue
        issues = check_theme(theme, path, expected)
        if issues:
            failed = True
            for issue in issues:
                print(f"  FAIL {issue}")
        else:
            print(
                f"  OK: all {len(expected)} reference names and "
                f"{len(CURSORFONT)} cursorfont glyphs present"
            )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
