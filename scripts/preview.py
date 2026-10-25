#!/usr/bin/env python3
"""Build contact sheets so the cursors can be judged at real sizes."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "bitmaps"
OUT = ROOT / "preview"
DOCS = ROOT / "docs"
FEATURED = [
    "left_ptr", "right_ptr", "hand2", "grabbing",
    "xterm", "crosshair", "move", "question_arrow",
    "pencil", "X_cursor", "pointer-move", "wait",
    "left_ptr_watch", "star", "heart", "spider",
]

BACKGROUNDS = {"light": "#f4f4f5", "dark": "#111113"}
INK = {"light": "#18181b", "dark": "#e4e4e7"}
FONT = "/usr/share/fonts/Adwaita/AdwaitaSans-Regular.ttf"

COLS = 6
CELL_W, CELL_H = 156, 148
MARGIN = 24
HEADER = 54


def font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def sheet(pack: str, mode: str, files: list[Path]) -> Image.Image:
    rows = math.ceil(len(files) / COLS)
    width = MARGIN * 2 + COLS * CELL_W
    height = HEADER + MARGIN + rows * CELL_H
    img = Image.new("RGB", (width, height), BACKGROUNDS[mode])
    draw = ImageDraw.Draw(img)

    draw.text((MARGIN, 16), f"Xscriptor / {pack}  ({mode})", font=font(20),
              fill=INK[mode])
    draw.text(
        (MARGIN, HEADER - 8),
        "64 px detail, 32 px and 24 px rendered from the same SVG",
        font=font(11),
        fill=INK[mode],
    )

    for i, path in enumerate(files):
        col, row = i % COLS, i // COLS
        x = MARGIN + col * CELL_W
        y = HEADER + row * CELL_H
        src = Image.open(path).convert("RGBA")

        big = src.resize((64, 64), Image.LANCZOS)
        mid = src.resize((32, 32), Image.LANCZOS)
        small = src.resize((24, 24), Image.LANCZOS)
        img.paste(big, (x + 14, y + 8), big)
        img.paste(mid, (x + 92, y + 20), mid)
        img.paste(small, (x + 100, y + 60), small)

        label = path.stem
        draw.text((x + 10, y + CELL_H - 26), label[:20], font=font(10),
                  fill=INK[mode])
    return img


def wait_sheet(pack: str) -> Image.Image:
    files = sorted((BUILD / pack).glob("wait-*.png"))
    width = MARGIN * 2 + len(files) * 104
    height = 150
    img = Image.new("RGB", (width, height), BACKGROUNDS["dark"])
    draw = ImageDraw.Draw(img)
    draw.text((MARGIN, 12), f"Xscriptor / {pack} / wait animation", font=font(16),
              fill=INK["dark"])
    for i, path in enumerate(files):
        src = Image.open(path).convert("RGBA")
        for j, size in enumerate((64, 24)):
            frame = src.resize((size, size), Image.LANCZOS)
            img.paste(frame, (MARGIN + i * 104 + (64 - size) // 2, 48 + j * 48),
                      frame)
    return img


def docs_sheet(pack: str, mode: str) -> Image.Image:
    rows = math.ceil(len(FEATURED) / 4)
    width = MARGIN * 2 + 4 * 176
    height = HEADER + MARGIN + rows * 156
    img = Image.new("RGB", (width, height), BACKGROUNDS[mode])
    draw = ImageDraw.Draw(img)
    draw.text((MARGIN, 16), f"Xscriptor / {pack}  ({mode})", font=font(20),
              fill=INK[mode])
    for i, name in enumerate(FEATURED):
        col, row = i % 4, i // 4
        x = MARGIN + col * 176
        y = HEADER + row * 156
        path = BUILD / pack / f"{name}.png"
        if not path.exists():
            frames = sorted((BUILD / pack).glob(f"{name}-*.png"))
            path = frames[len(frames) // 2] if frames else None
        if path is None:
            continue
        src = Image.open(path).convert("RGBA")
        big = src.resize((64, 64), Image.LANCZOS)
        small = src.resize((24, 24), Image.LANCZOS)
        img.paste(big, (x + 10, y), big)
        img.paste(small, (x + 88, y + 20), small)
        draw.text((x + 8, y + 74), name, font=font(11), fill=INK[mode])
    return img


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    for pack in ("x", "berlin"):
        files = [
            p for p in sorted((BUILD / pack).glob("*.png"))
            if not p.stem.startswith(("wait-", "left_ptr_watch-"))
        ]
        for mode in ("light", "dark"):
            img = sheet(pack, mode, files)
            path = OUT / f"{pack}-{mode}.png"
            img.save(path)
            print(path)
        wait = wait_sheet(pack)
        path = OUT / f"{pack}-wait.png"
        wait.save(path)
        print(path)
        for mode in ("light", "dark"):
            docs = docs_sheet(pack, mode)
            path = DOCS / f"preview-{pack}-{mode}.png"
            docs.save(path)
            print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
