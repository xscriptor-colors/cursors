"""Original cursor artwork, drawn from scratch as SVG fragments.

The whole set shares one visual language:
  * a gradient body (palette colours),
  * a bright rim (gold for X, white for Berlin),
  * a dark outer contour so the cursor survives both light and dark desktops,
  * small X glyphs placed in the empty corners around the glyph.

Every coordinate lives on a 256x256 canvas.  clickgen downscales the rendered
PNG to the requested nominal sizes.
"""

from __future__ import annotations

import math
from typing import Iterable

PALETTES = {
    "x": {
        "stops": [
            ("0%", "#4328a8"),
            ("28%", "#7c3aed"),
            ("52%", "#4d96ff"),
            ("76%", "#ff9f43"),
            ("100%", "#f59e0b"),
        ],
        "rim": "#ffe884",
        "dark": "#171717",
    },
    "berlin": {
        "stops": [("0%", "#0a0a0a"), ("100%", "#4b4b55")],
        "rim": "#ffffff",
        "dark": "#000000",
    },
}

DARK_W = 48
RIM_W = 24


def svg_document(body: str, pal: dict) -> str:
    stops = "".join(
        f'<stop offset="{offset}" stop-color="{color}"/>'
        for offset, color in pal["stops"]
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" '
        'viewBox="0 0 256 256">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">{stops}'
        "</linearGradient></defs>"
        f"{body}"
        "</svg>"
    )


def _group(body: str, transform: str | None) -> str:
    if not transform:
        return body
    return f'<g transform="{transform}">{body}</g>'


def ofill(d: str, pal: dict, transform: str | None = None) -> str:
    """Filled shape: dark contour -> bright rim -> gradient interior."""
    attrs = 'stroke-linejoin="round" stroke-linecap="round"'
    body = (
        f'<path d="{d}" fill="{pal["dark"]}" stroke="{pal["dark"]}" '
        f'stroke-width="{DARK_W}" {attrs}/>'
        f'<path d="{d}" fill="{pal["rim"]}" stroke="{pal["rim"]}" '
        f'stroke-width="{RIM_W}" {attrs}/>'
        f'<path d="{d}" fill="url(#g)" stroke="none"/>'
    )
    return _group(body, transform)


def osolid(d: str, pal: dict, color: str) -> str:
    """Flat-colour shape with a thin dark contour (pencil wood/graphite)."""
    attrs = 'stroke-linejoin="round" stroke-linecap="round"'
    return (
        f'<path d="{d}" fill="{pal["dark"]}" stroke="{pal["dark"]}" '
        f'stroke-width="14" {attrs}/>'
        f'<path d="{d}" fill="{color}" stroke="none"/>'
    )


def oring(cx: float, cy: float, r: float, pal: dict, core: float = 12,
              pad: float = 5, dark_pad: float = 5,
              transform: str | None = None) -> str:
    """Circle outline built with the same contour/rim/gradient stack."""
    body = (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
        f'stroke="{pal["dark"]}" stroke-width="{core + 2 * (pad + dark_pad)}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
        f'stroke="{pal["rim"]}" stroke-width="{core + 2 * pad}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
        f'stroke="url(#g)" stroke-width="{core}"/>'
    )
    return _group(body, transform)


def oline(d: str, pal: dict, core: float = 12, pad: float = 5,
          dark_pad: float = 5, transform: str | None = None) -> str:
    """Open path / line stack.  ``d`` may contain several subpaths so that an
    X glyph gets its three layers applied globally instead of per stroke."""
    attrs = 'fill="none" stroke-linejoin="round" stroke-linecap="round"'
    body = (
        f'<path d="{d}" stroke="{pal["dark"]}" '
        f'stroke-width="{core + 2 * (pad + dark_pad)}" {attrs}/>'
        f'<path d="{d}" stroke="{pal["rim"]}" '
        f'stroke-width="{core + 2 * pad}" {attrs}/>'
        f'<path d="{d}" stroke="url(#g)" stroke-width="{core}" {attrs}/>'
    )
    return _group(body, transform)


def spark(cx: float, cy: float, r: float, rot: float, pal: dict,
          core: float = 8) -> str:
    # Long, thin arms read as an "X" even at 24 px; a 1:1 arm/width ratio
    # turns into an unreadable dot.
    r = max(r, 14)
    a = r * 0.90
    d = (
        f"M {cx - a:.1f} {cy - a:.1f} L {cx + a:.1f} {cy + a:.1f} "
        f"M {cx + a:.1f} {cy - a:.1f} L {cx - a:.1f} {cy + a:.1f}"
    )
    return oline(d, pal, core=core, pad=4, dark_pad=4,
                 transform=f"rotate({rot} {cx} {cy})")


def sparks(pal: dict, points: Iterable[tuple[float, float, float, float]]) -> str:
    return "".join(spark(x, y, r, rot, pal) for x, y, r, rot in points)


# --------------------------------------------------------------------------
# Shared glyph contours
# --------------------------------------------------------------------------

POINTER = (
    "M 40 32 L 40 192 Q 40 206 52 197 L 92 164 L 116 218 "
    "Q 121 229 132 224 L 154 215 Q 165 211 160 200 L 138 146 "
    "L 186 146 Q 199 146 190 136 Z"
)

XTERM = (
    "M 86 44 L 170 44 L 170 62 L 145 62 L 145 194 L 170 194 "
    "L 170 212 L 86 212 L 86 194 L 111 194 L 111 62 L 86 62 Z"
)

UP_ARROW = (
    "M 128 44 L 92 104 L 115 104 L 115 198 Q 115 210 128 210 "
    "Q 141 210 141 198 L 141 104 L 164 104 Z"
)

STUB = (
    "M 128 48 L 96 102 L 116 102 L 116 120 Q 116 128 128 128 "
    "Q 140 128 140 120 L 140 102 L 160 102 Z"
)

DOUBLE_H = (
    "M 36 128 L 84 88 L 84 114 L 172 114 L 172 88 L 220 128 "
    "L 172 168 L 172 142 L 84 142 L 84 168 Z"
)

HAND_POINT = (
    "M 112 52 C 112 38 144 38 144 52 L 144 120 L 156 114 "
    "C 168 108 180 118 178 132 L 170 172 C 166 198 150 212 126 212 "
    "L 102 212 C 82 212 70 200 66 182 L 56 146 C 52 130 64 120 78 126 "
    "L 92 134 L 92 76 C 92 64 112 64 112 76 Z"
)

HAND_OPEN = (
    "M 74 218 C 60 204 62 184 68 170 L 80 128 C 82 116 96 118 96 130 "
    "L 96 84 C 96 72 110 72 110 84 L 110 122 L 112 66 C 112 54 126 54 126 66 "
    "L 126 120 L 130 76 C 130 64 144 64 144 76 L 144 124 L 148 92 "
    "C 148 80 162 80 162 92 L 162 142 C 176 136 186 146 188 160 L 192 186 "
    "C 194 210 178 222 156 222 L 106 222 C 92 222 82 222 74 218 Z"
)

HAND_FIST = (
    "M 72 156 C 72 138 84 128 100 132 L 104 116 C 106 104 122 104 126 116 "
    "L 130 108 C 134 96 150 98 152 110 L 158 104 C 166 94 180 102 180 114 "
    "L 188 156 C 196 190 178 216 148 218 L 112 218 C 86 218 68 198 68 174 Z"
)

PENCIL_BODY = (
    "M 114 96 Q 114 88 122 88 L 134 88 Q 142 88 142 96 "
    "L 142 184 L 114 184 Z"
)
PENCIL_WOOD = "M 114 184 L 142 184 L 128 212 Z"
PENCIL_GRAPHITE = "M 122 197 L 134 197 L 128 212 Z"
PENCIL_CAP = (
    "M 108 72 Q 108 62 118 62 L 138 62 Q 148 62 148 72 L 148 88 L 108 88 Z"
)

TEE = (
    "M 66 72 Q 66 62 76 62 L 180 62 Q 190 62 190 72 L 190 82 "
    "Q 190 92 180 92 L 138 92 L 138 174 Q 138 184 128 184 "
    "Q 118 184 118 174 L 118 92 L 76 92 Q 66 92 66 82 Z"
)

CORNER_L = "M 62 122 L 62 62 L 122 62"


# --------------------------------------------------------------------------
# Cursor drawings
# --------------------------------------------------------------------------

def left_ptr(pal: dict) -> str:
    return ofill(POINTER, pal) + sparks(
        pal, [(203, 62, 22, 12), (206, 120, 12, 28)]
    )


def right_ptr(pal: dict) -> str:
    return ofill(POINTER, pal, "translate(256 0) scale(-1 1)") + sparks(
        pal, [(53, 62, 22, 12), (50, 120, 12, 28)]
    )


def center_ptr(pal: dict) -> str:
    return ofill(UP_ARROW, pal) + sparks(
        pal, [(58, 190, 14, 18), (200, 190, 18, 8)]
    )


def up_arrow(pal: dict, angle: float = 0) -> str:
    return ofill(UP_ARROW, pal, f"rotate({angle} 128 128)") + sparks(
        pal, [(56, 190, 14, 18), (200, 190, 18, 8)]
    )


def double_arrow(pal: dict, angle: float = 0) -> str:
    return ofill(DOUBLE_H, pal, f"rotate({angle} 128 128)") + sparks(
        pal, [(52, 54, 12, 10), (204, 202, 12, 10)]
    )


def move(pal: dict) -> str:
    body = "".join(
        ofill(STUB, pal, f"rotate({a} 128 128)") for a in (0, 90, 180, 270)
    )
    return body + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])


def hand_point(pal: dict) -> str:
    return ofill(HAND_POINT, pal) + sparks(
        pal, [(54, 76, 16, 18), (204, 72, 18, 10), (204, 198, 10, 24)]
    )


def hand_open(pal: dict) -> str:
    return ofill(HAND_OPEN, pal) + sparks(
        pal, [(54, 74, 14, 14), (204, 66, 16, 22)]
    )


def hand_fist(pal: dict) -> str:
    return ofill(HAND_FIST, pal) + sparks(
        pal, [(52, 66, 16, 12), (204, 64, 14, 26)]
    )


def xterm(pal: dict, angle: float = 0) -> str:
    return ofill(XTERM, pal, f"rotate({angle} 128 128)") + sparks(
        pal, [(54, 54, 11, 8), (202, 202, 11, 8)]
    )


def crosshair(pal: dict) -> str:
    return oline("M 74 128 L 182 128 M 128 74 L 128 182", pal, core=13) + sparks(
        pal, [(54, 54, 12, 10), (202, 54, 12, 20),
              (54, 202, 12, 20), (202, 202, 12, 10)]
    )


def cross(pal: dict) -> str:
    return oline("M 82 128 L 174 128 M 128 82 L 128 174", pal, core=30) + sparks(
        pal, [(54, 54, 10, 10), (202, 202, 10, 10)]
    )


def tcross(pal: dict) -> str:
    return oline("M 80 88 L 176 88 M 128 88 L 128 180", pal, core=18) + sparks(
        pal, [(54, 66, 11, 14), (202, 66, 11, 14), (202, 196, 10, 20)]
    )


def x_cursor(pal: dict) -> str:
    return oline("M 74 74 L 182 182 M 182 74 L 74 182", pal, core=28) + sparks(
        pal, [(52, 128, 10, 20), (204, 128, 10, 20)]
    )


def circle(pal: dict) -> str:
    return oring(128, 128, 62, pal, core=22) + sparks(
        pal, [(54, 54, 10, 10), (202, 202, 10, 10)]
    )


def crossed_circle(pal: dict) -> str:
    body = oring(128, 128, 62, pal, core=22)
    return body + oline("M 84 172 L 172 84", pal, core=22) + sparks(
        pal, [(52, 60, 10, 10), (204, 196, 10, 10)]
    )


def badge(cx: float, cy: float, r: float, pal: dict) -> str:
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{pal["dark"]}" '
        f'stroke="{pal["dark"]}" stroke-width="32"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{pal["rim"]}" '
        f'stroke="{pal["rim"]}" stroke-width="16"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g)"/>'
    )


def question_mark(cx: float, cy: float, scale: float, pal: dict) -> str:
    d = (
        f"M {cx - 10 * scale:.1f} {cy - 8 * scale:.1f} "
        f"Q {cx - 10 * scale:.1f} {cy - 20 * scale:.1f} "
        f"{cx:.1f} {cy - 20 * scale:.1f} "
        f"Q {cx + 10 * scale:.1f} {cy - 20 * scale:.1f} "
        f"{cx + 10 * scale:.1f} {cy - 8 * scale:.1f} "
        f"Q {cx + 10 * scale:.1f} {cy:.1f} {cx:.1f} {cy + 4 * scale:.1f} "
        f"L {cx:.1f} {cy + 10 * scale:.1f}"
    )
    return (
        f'<path d="{d}" fill="none" stroke="{pal["dark"]}" '
        f'stroke-width="{7 * scale:.1f}" stroke-linecap="round"/>'
        f'<circle cx="{cx}" cy="{cy + 22 * scale:.1f}" '
        f'r="{4.5 * scale:.1f}" fill="{pal["dark"]}"/>'
    )


def question_arrow(pal: dict) -> str:
    return (
        ofill(POINTER, pal)
        + badge(196, 88, 30, pal)
        + question_mark(196, 88, 1.0, pal)
        + sparks(pal, [(204, 206, 11, 14)])
    )


def copy_cursor(pal: dict) -> str:
    badge_body = (
        ofill(
            "M 150 146 h 42 a 9 9 0 0 1 9 9 v 42 a 9 9 0 0 1 -9 9 "
            "h -42 a 9 9 0 0 1 -9 -9 v -42 a 9 9 0 0 1 9 -9 z",
            pal,
        )
        + ofill(
            "M 166 162 h 42 a 9 9 0 0 1 9 9 v 42 a 9 9 0 0 1 -9 9 "
            "h -42 a 9 9 0 0 1 -9 -9 v -42 a 9 9 0 0 1 9 -9 z",
            pal,
        )
    )
    return (
        ofill(POINTER, pal)
        + f'<g transform="rotate(-8 200 200)">{badge_body}</g>'
        + sparks(pal, [(204, 60, 16, 12)])
    )


def pointer_move(pal: dict) -> str:
    arrow = ofill(POINTER, pal, "translate(40 32) scale(0.78) translate(-40 -32)")
    badge_body = (
        f'<circle cx="204" cy="92" r="36" fill="{pal["dark"]}" '
        f'stroke="{pal["dark"]}" stroke-width="28"/>'
        f'<circle cx="204" cy="92" r="36" fill="{pal["rim"]}" stroke="none"/>'
    )
    mini = (
        f'<path d="M 204 64 L 192 82 L 199 82 L 199 102 L 192 102 '
        f'L 204 120 L 216 102 L 209 102 L 209 82 L 216 82 Z" '
        f'fill="{pal["dark"]}"/>'
        f'<path d="M 176 92 L 194 80 L 194 87 L 214 87 L 214 80 '
        f'L 232 92 L 214 104 L 214 97 L 194 97 L 194 104 Z" '
        f'fill="{pal["dark"]}"/>'
    )
    return arrow + badge_body + mini + sparks(pal, [(204, 212, 11, 14)])


def link_cursor(pal: dict) -> str:
    ring = 'fill="none" stroke-linejoin="round" stroke-linecap="round"'
    chain = (
        f'<rect x="-42" y="-16" width="50" height="32" rx="16" {ring} '
        f'stroke="{pal["dark"]}" stroke-width="30"/>'
        f'<rect x="-8" y="-16" width="50" height="32" rx="16" {ring} '
        f'stroke="{pal["dark"]}" stroke-width="30"/>'
        f'<rect x="-42" y="-16" width="50" height="32" rx="16" {ring} '
        f'stroke="{pal["rim"]}" stroke-width="18"/>'
        f'<rect x="-8" y="-16" width="50" height="32" rx="16" {ring} '
        f'stroke="{pal["rim"]}" stroke-width="18"/>'
        f'<rect x="-42" y="-16" width="50" height="32" rx="16" {ring} '
        f'stroke="url(#g)" stroke-width="10"/>'
        f'<rect x="-8" y="-16" width="50" height="32" rx="16" {ring} '
        f'stroke="url(#g)" stroke-width="10"/>'
    )
    return (
        ofill(POINTER, pal)
        + f'<g transform="translate(196 190) rotate(-45)">{chain}</g>'
        + sparks(pal, [(204, 58, 15, 12)])
    )


def no_drop(pal: dict) -> str:
    badge_art = oring(0, 0, 34, pal, core=18) + oline(
        "M -24 24 L 24 -24", pal, core=18
    )
    return (
        ofill(POINTER, pal)
        + f'<g transform="translate(196 190)">{badge_art}</g>'
        + sparks(pal, [(204, 58, 15, 12)])
    )


def context_menu(pal: dict) -> str:
    badge_body = (
        ofill(
            "M 150 164 h 52 a 10 10 0 0 1 10 10 v 40 a 10 10 0 0 1 -10 10 "
            "h -52 a 10 10 0 0 1 -10 -10 v -40 a 10 10 0 0 1 10 -10 z",
            pal,
        )
        + oline(
            "M 162 186 L 204 186 M 162 200 L 204 200 M 162 214 L 190 214",
            pal, core=7, pad=2, dark_pad=2,
        )
    )
    return (
        ofill(POINTER, pal)
        + badge_body
        + sparks(pal, [(204, 58, 15, 12), (206, 226, 10, 24)])
    )


def tee(pal: dict, angle: float, spark_points: tuple) -> str:
    return ofill(TEE, pal, f"rotate({angle} 128 128)") + sparks(pal, spark_points)


def corner_l(pal: dict, d: str, spark_points: tuple) -> str:
    return oline(d, pal, core=24) + sparks(pal, spark_points)


def pencil(pal: dict) -> str:
    body = (
        ofill(PENCIL_BODY, pal)
        + osolid(PENCIL_WOOD, pal, pal["rim"])
        + osolid(PENCIL_GRAPHITE, pal, pal["dark"])
        + ofill(PENCIL_CAP, pal)
        + oline("M 108 88 L 148 88", pal, core=6, pad=3, dark_pad=3)
    )
    return (
        f'<g transform="rotate(-24 128 212)">{body}</g>'
        + sparks(pal, [(198, 84, 16, 10), (58, 202, 11, 24)])
    )


def plus_cursor(pal: dict) -> str:
    return oline("M 82 128 L 174 128 M 128 82 L 128 174", pal, core=32) + sparks(
        pal, [(54, 54, 10, 10), (202, 54, 10, 20),
              (54, 202, 10, 20), (202, 202, 10, 10)]
    )


def dotbox(pal: dict) -> str:
    brackets = (
        "M 62 100 L 62 62 L 100 62 M 194 62 L 156 62 L 156 100 "
        "M 62 156 L 62 194 L 100 194 M 194 156 L 194 194 L 156 194"
    )
    dots = "".join(
        ofill_circle(x, y, 6, pal) for x, y in ((128, 58), (198, 128),
                                                (128, 198), (58, 128))
    )
    return oline(brackets, pal, core=15) + dots + sparks(
        pal, [(54, 54, 9, 10), (202, 202, 9, 10)]
    )


def ofill_circle(cx: float, cy: float, r: float, pal: dict,
                 dark_w: float = 20, rim_w: float = 10) -> str:
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{pal["dark"]}" '
        f'stroke="{pal["dark"]}" stroke-width="{dark_w}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{pal["rim"]}" '
        f'stroke="{pal["rim"]}" stroke-width="{rim_w}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g)"/>'
    )


def ofill_ellipse(cx: float, cy: float, rx: float, ry: float, pal: dict,
                  dark_w: float = 44, rim_w: float = 22) -> str:
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="{pal["dark"]}" stroke="{pal["dark"]}" '
        f'stroke-width="{dark_w}"/>'
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="{pal["rim"]}" stroke="{pal["rim"]}" stroke-width="{rim_w}"/>'
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#g)"/>'
    )


def star_path(cx: float, cy: float, outer: float, inner: float,
              points: int = 5, rot: float = -90) -> str:
    coords = []
    for i in range(points * 2):
        radius = outer if i % 2 == 0 else inner
        angle = math.radians(rot + i * 180 / points)
        coords.append(
            f"{cx + radius * math.cos(angle):.1f} "
            f"{cy + radius * math.sin(angle):.1f}"
        )
    return "M " + " L ".join(coords) + " Z"


def zoom(pal: dict, sign: str) -> str:
    body = (
        oring(106, 106, 46, pal, core=18)
        + oline("M 139 139 L 204 204", pal, core=22)
        + oline("M 88 106 L 124 106", pal, core=11)
    )
    if sign == "+":
        body += oline("M 106 88 L 106 124", pal, core=11)
    return body + sparks(pal, [(202, 62, 14, 18), (60, 196, 10, 10)])


def skull_frames(pal: dict, frame_count: int = 12) -> list[str]:
    cranium = (
        "M 128 40 C 82 40 48 74 48 118 C 48 150 62 172 88 184 "
        "L 88 190 Q 88 198 98 198 L 158 198 Q 168 198 168 190 "
        "L 168 184 C 194 172 208 150 208 118 C 208 74 174 40 128 40 Z"
    )
    jaw = (
        "M 98 198 Q 98 230 128 230 Q 158 230 158 198 L 144 198 "
        "Q 144 216 128 216 Q 112 216 112 198 Z"
    )
    mouth = '<rect x="92" y="184" width="72" height="92" rx="22" fill="{dark}"/>'
    frames: list[str] = []
    for i in range(frame_count):
        phase = i / frame_count
        travel = (0.5 - 0.5 * math.cos(2 * math.pi * phase)) * 40
        tilt = math.sin(2 * math.pi * phase) * 2.0
        jaw_d = (
            f'<g transform="translate(0 {travel:.1f})">'
            + ofill(jaw, pal)
            + "".join(
                f'<rect x="{x0}" y="200" width="10" height="15" rx="3" '
                f'fill="{pal["rim"]}" stroke="{pal["dark"]}" stroke-width="3"/>'
                for x0 in (106, 119, 132, 145)
            )
            + "</g>"
        )
        teeth = "".join(
            f'<rect x="{x0}" y="192" width="10" height="16" rx="3" '
            f'fill="{pal["rim"]}" stroke="{pal["dark"]}" stroke-width="3"/>'
            for x0 in (104, 117, 130, 143)
        )
        eyes = (
            f'<ellipse cx="97" cy="112" rx="22" ry="27" fill="{pal["dark"]}" '
            f'transform="rotate(-8 97 112)"/>'
            f'<ellipse cx="159" cy="112" rx="22" ry="27" fill="{pal["dark"]}" '
            f'transform="rotate(8 159 112)"/>'
            f'<circle cx="90" cy="104" r="4" fill="{pal["rim"]}"/>'
            f'<circle cx="152" cy="104" r="4" fill="{pal["rim"]}"/>'
        )
        nose = (
            f'<path d="M 128 138 L 117 164 Q 128 171 139 164 Z" '
            f'fill="{pal["dark"]}"/>'
        )
        cheeks = (
            f'<path d="M 74 150 q 8 10 6 20 M 182 150 q -8 10 -6 20" '
            f'fill="none" stroke="{pal["dark"]}" stroke-width="5" '
            f'stroke-linecap="round"/>'
        )
        body = (
            mouth.format(dark=pal["dark"])
            + jaw_d
            + ofill(cranium, pal)
            + teeth
            + eyes
            + nose
            + cheeks
        )
        frames.append(
            f'<g transform="translate(128 124) scale(0.72) '
            f'translate(-128 -128) rotate({tilt:.2f} 128 128)">{body}</g>'
        )
    return frames


def wait(pal: dict) -> list[str]:
    return [
        frame + sparks(pal, [(54, 58, 12, 10), (202, 202, 12, 20)])
        for frame in skull_frames(pal)
    ]


def left_ptr_watch(pal: dict) -> list[str]:
    arrow = ofill(POINTER, pal, "translate(40 32) scale(0.80) translate(-40 -32)")
    frames = []
    for skull in skull_frames(pal):
        frames.append(
            arrow
            + f'<g transform="translate(198 80) scale(0.50) translate(-128 -122)">'
            f"{skull}</g>"
            + sparks(pal, [(66, 222, 10, 24)])
        )
    return frames


def wayland(pal: dict) -> str:
    return left_ptr(pal)


# --------------------------------------------------------------------------
# Legacy X11 cursorfont glyphs (original artwork for the old cursor slots)
# --------------------------------------------------------------------------

MOUSE_TOP = (
    "M 94 138 L 94 128 Q 94 86 128 86 Q 162 86 162 128 L 162 138 Z"
)
MOUSE_BOTTOM = (
    "M 94 138 L 162 138 L 162 182 Q 162 216 128 216 Q 94 216 94 182 Z"
)


def dot(pal: dict) -> str:
    return (
        ofill_circle(128, 128, 34, pal, dark_w=48, rim_w=24)
        + sparks(pal, [(198, 64, 10, 12), (58, 192, 10, 20)])
    )


def heart(pal: dict) -> str:
    d = (
        "M 128 202 C 88 172 54 142 54 106 C 54 80 74 62 98 62 "
        "C 114 62 126 73 128 88 C 130 73 142 62 158 62 "
        "C 182 62 202 80 202 106 C 202 142 168 172 128 202 Z"
    )
    return ofill(d, pal) + sparks(pal, [(54, 54, 12, 10), (202, 202, 12, 10)])


def star(pal: dict) -> str:
    return (
        ofill(star_path(128, 128, 84, 36), pal)
        + sparks(pal, [(54, 54, 12, 10), (202, 202, 12, 10)])
    )


def iron_cross(pal: dict) -> str:
    d = (
        "M 102 62 L 154 62 L 148 106 L 194 106 L 194 150 L 148 150 "
        "L 154 194 L 102 194 L 108 150 L 62 150 L 62 106 L 108 106 Z"
    )
    return ofill(d, pal) + sparks(pal, [(54, 54, 12, 10), (202, 202, 12, 10)])


def rtl_logo(pal: dict) -> str:
    left = (
        "M 54 128 L 92 98 L 92 116 L 124 116 L 124 140 L 92 140 "
        "L 92 158 Z"
    )
    right = (
        "M 202 128 L 164 98 L 164 116 L 132 116 L 132 140 L 164 140 "
        "L 164 158 Z"
    )
    return (
        ofill(left, pal)
        + ofill(right, pal)
        + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])
    )


def boat(pal: dict) -> str:
    hull = (
        "M 44 162 L 212 162 L 188 204 Q 184 212 174 212 L 82 212 "
        "Q 72 212 68 204 Z"
    )
    return (
        ofill(hull, pal)
        + oline("M 84 180 L 172 180", pal, core=6, pad=3, dark_pad=3)
        + sparks(pal, [(54, 60, 11, 12), (202, 60, 11, 12)])
    )


def sailboat(pal: dict) -> str:
    hull = "M 52 174 Q 52 210 88 210 L 168 210 Q 204 210 204 174 Z"
    main = "M 138 64 L 138 152 L 194 152 Z"
    jib = "M 126 84 L 126 150 L 82 150 Z"
    return (
        ofill(hull, pal)
        + oline("M 132 174 L 132 54", pal, core=10, pad=4, dark_pad=4)
        + ofill(main, pal)
        + ofill(jib, pal)
        + sparks(pal, [(54, 60, 10, 10), (202, 60, 10, 10)])
    )


def coffee_mug(pal: dict) -> str:
    body = (
        "M 88 100 L 160 100 L 152 206 Q 151 218 138 218 L 110 218 "
        "Q 97 218 96 206 Z"
    )
    lip = (
        "M 82 90 Q 82 80 94 80 L 154 80 Q 166 80 166 90 L 166 102 "
        "L 82 102 Z"
    )
    return (
        ofill(body, pal)
        + ofill(lip, pal)
        + oline(
            "M 160 118 Q 202 118 202 152 Q 202 186 160 186",
            pal, core=14,
        )
        + oline(
            "M 108 68 Q 98 54 108 40 M 128 68 Q 118 54 128 40 "
            "M 148 68 Q 138 54 148 40",
            pal, core=5, pad=3, dark_pad=3,
        )
        + sparks(pal, [(206, 60, 10, 12)])
    )


def spraycan(pal: dict) -> str:
    body = (
        "M 96 96 Q 96 86 106 86 L 152 86 Q 162 86 162 96 L 162 208 "
        "Q 162 218 152 218 L 106 218 Q 96 218 96 208 Z"
    )
    cap = "M 112 66 L 146 66 L 146 86 L 112 86 Z"
    nozzle = "M 122 50 L 136 50 L 136 66 L 122 66 Z"
    dots = "".join(
        ofill_circle(x, y, r, pal, dark_w=14, rim_w=7)
        for x, y, r in ((180, 64, 7), (194, 82, 5), (180, 100, 4),
                        (200, 102, 3))
    )
    return (
        ofill(body, pal)
        + ofill(cap, pal)
        + ofill(nozzle, pal)
        + dots
        + sparks(pal, [(54, 54, 10, 10)])
    )


def gumby(pal: dict) -> str:
    hat = "M 102 56 L 154 56 L 146 70 L 110 70 Z"
    torso = (
        "M 104 108 Q 104 98 114 98 L 142 98 Q 152 98 152 108 "
        "L 152 160 L 104 160 Z"
    )
    return (
        ofill(hat, pal)
        + ofill_circle(128, 84, 24, pal, dark_w=40, rim_w=20)
        + ofill(torso, pal)
        + oline("M 106 120 L 80 148 M 150 120 L 176 148", pal, core=12)
        + oline("M 116 160 L 106 204 M 140 160 L 150 204", pal, core=12)
        + f'<circle cx="120" cy="82" r="3.5" fill="{pal["dark"]}"/>'
        + f'<circle cx="136" cy="82" r="3.5" fill="{pal["dark"]}"/>'
        + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])
    )


def man(pal: dict) -> str:
    return (
        ofill_circle(128, 62, 22, pal, dark_w=40, rim_w=20)
        + oline(
            "M 128 84 L 128 146 M 94 108 L 128 100 L 162 108 "
            "M 128 146 L 104 196 M 128 146 L 152 196",
            pal, core=13,
        )
        + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])
    )


def gobbler(pal: dict) -> str:
    body = (
        "M 120 108 C 80 108 52 130 52 158 C 52 188 80 208 112 208 "
        "C 146 208 168 188 168 158 C 168 132 150 112 120 108 Z"
    )
    tail = (
        "M 80 130 L 48 112 L 68 148 Z "
        "M 72 148 L 40 144 L 62 166 Z "
        "M 76 166 L 48 178 L 74 184 Z"
    )
    return (
        ofill(tail, pal)
        + ofill(body, pal)
        + ofill_circle(174, 102, 20, pal, dark_w=40, rim_w=20)
        + ofill("M 192 96 L 214 104 L 192 112 Z", pal)
        + oline("M 112 204 L 104 224 M 144 204 L 152 224", pal, core=10)
        + f'<circle cx="180" cy="98" r="3.5" fill="{pal["dark"]}"/>'
        + sparks(pal, [(54, 54, 10, 10), (206, 206, 10, 10)])
    )


def bogosity(pal: dict) -> str:
    fist = (
        "M 92 78 Q 92 70 100 70 L 148 70 Q 156 70 156 78 "
        "L 156 136 Q 156 144 148 144 L 100 144 Q 92 144 92 136 Z"
    )
    thumb = (
        "M 140 138 Q 172 138 172 162 L 172 184 Q 172 202 154 202 "
        "Q 142 202 140 190 L 138 160 Q 137 146 140 138 Z"
    )
    cuff = "M 96 144 L 148 144 L 148 166 L 96 166 Z"
    return (
        ofill(fist, pal)
        + ofill(thumb, pal)
        + ofill(cuff, pal)
        + oline("M 108 82 L 108 132 M 124 82 L 124 132 M 140 82 L 140 132",
                pal, core=4, pad=2, dark_pad=2)
        + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])
    )


def box_spiral(pal: dict) -> str:
    d = (
        "M 72 184 L 72 72 L 184 72 L 184 168 L 88 168 L 88 88 "
        "L 168 88 L 168 152 L 104 152 L 104 104 L 150 104"
    )
    return (
        oline(d, pal, core=14)
        + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])
    )


def shuttle(pal: dict) -> str:
    d = (
        "M 128 44 C 136 56 140 72 140 88 L 176 140 L 176 160 "
        "L 140 148 L 140 180 L 154 196 L 154 206 L 128 196 "
        "L 102 206 L 102 196 L 116 180 L 116 148 L 80 160 "
        "L 80 140 L 116 88 C 116 72 120 56 128 44 Z"
    )
    return ofill(d, pal) + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])


def trek(pal: dict) -> str:
    delta = "M 128 52 L 190 194 L 128 162 L 66 194 Z"
    return (
        ofill(delta, pal)
        + ofill(star_path(128, 112, 18, 8), pal)
        + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])
    )


def spider(pal: dict) -> str:
    legs = (
        "M 104 130 L 70 112 L 50 122 M 100 150 L 60 148 L 42 160 "
        "M 104 168 L 68 184 L 52 202 M 112 180 L 96 208 L 82 222 "
        "M 152 130 L 186 112 L 206 122 M 156 150 L 196 148 L 214 160 "
        "M 152 168 L 188 184 L 204 202 M 144 180 L 160 208 L 174 222"
    )
    return (
        oline(legs, pal, core=9)
        + ofill_ellipse(128, 150, 30, 38, pal)
        + ofill_circle(128, 100, 20, pal, dark_w=40, rim_w=20)
        + f'<circle cx="121" cy="96" r="3.5" fill="{pal["dark"]}"/>'
        + f'<circle cx="135" cy="96" r="3.5" fill="{pal["dark"]}"/>'
        + sparks(pal, [(54, 54, 10, 10), (202, 54, 10, 10)])
    )


def umbrella(pal: dict) -> str:
    canopy = (
        "M 52 132 Q 52 60 128 60 Q 204 60 204 132 Q 180 118 156 132 "
        "Q 128 118 100 132 Q 76 118 52 132 Z"
    )
    return (
        ofill(canopy, pal)
        + oline(
            "M 128 132 L 128 192 Q 128 210 110 210 Q 96 210 96 196",
            pal, core=12,
        )
        + sparks(pal, [(54, 54, 10, 10), (202, 202, 10, 10)])
    )


def _mouse_base(pal: dict, highlight: str | None) -> str:
    body = ofill(MOUSE_TOP, pal) + ofill(MOUSE_BOTTOM, pal)
    if highlight == "left":
        body += osolid(
            "M 96 136 L 96 128 Q 96 90 126 88 L 126 136 Z", pal, pal["rim"]
        )
        body += (
            f'<rect x="121" y="100" width="14" height="26" rx="7" '
            f'fill="{pal["dark"]}"/>'
        )
    elif highlight == "right":
        body += osolid(
            "M 130 88 Q 160 90 160 128 L 160 136 L 130 136 Z",
            pal, pal["rim"],
        )
        body += (
            f'<rect x="121" y="100" width="14" height="26" rx="7" '
            f'fill="{pal["dark"]}"/>'
        )
    elif highlight == "middle":
        body += osolid(
            "M 119 96 Q 128 90 137 96 L 137 134 L 119 134 Z",
            pal, pal["rim"],
        )
    else:
        body += (
            f'<rect x="121" y="100" width="14" height="26" rx="7" '
            f'fill="{pal["dark"]}"/>'
        )
        body += oline("M 128 88 L 128 138", pal, core=4, pad=2, dark_pad=2)
    return body + sparks(pal, [(54, 62, 12, 10), (202, 202, 12, 10)])


def mouse(pal: dict) -> str:
    return _mouse_base(pal, None)


def leftbutton(pal: dict) -> str:
    return _mouse_base(pal, "left")


def middlebutton(pal: dict) -> str:
    return _mouse_base(pal, "middle")


def rightbutton(pal: dict) -> str:
    return _mouse_base(pal, "right")
