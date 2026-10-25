#!/usr/bin/env python3
"""Render the cursor catalogue into SVG sources (one directory per pack)."""

from __future__ import annotations

import sys
from pathlib import Path

import art
import spec

ROOT = Path(__file__).resolve().parents[1]
PACKS = ("x", "berlin")


def main() -> int:
    for pack in PACKS:
        out_dir = ROOT / "src" / pack
        out_dir.mkdir(parents=True, exist_ok=True)
        for stale in out_dir.glob("*.svg"):
            stale.unlink()

        pal = art.PALETTES[pack]
        written = 0
        for cursor in spec.CURSORS:
            frames = cursor.draw(pal)
            if len(frames) == 1:
                names = [f"{cursor.key}.svg"]
            else:
                names = [
                    f"{cursor.key}-{i:03d}.svg" for i in range(len(frames))
                ]
            for name, body in zip(names, frames):
                (out_dir / name).write_text(art.svg_document(body, pal))
                written += 1
        print(f"{pack}: {written} SVG frames -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
