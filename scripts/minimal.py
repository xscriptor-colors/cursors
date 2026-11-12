"""Minimal cursor geometry for the X and Berlin packs.

Shapes use rounded corners, a thin dark contour and rim, the shared palette
gradient, and one small X outside the body. Coordinates stay on the 256x256
canvas used by the rest of the renderer.
"""

from __future__ import annotations

POINTER = (
    "M 168.00 42.00 L 168.00 142.00 Q 168.00 152.00 158.00 152.00 "
    "L 130.00 152.00 Q 120.00 152.00 112.93 144.93 L 103.07 135.07 "
    "Q 96.00 128.00 88.93 135.07 L 79.07 144.93 Q 72.00 152.00 78.25 144.19 "
    "L 161.75 39.81 Q 168.00 32.00 168.00 42.00 Z"
)
POINTER_TRANSFORM = "translate(256 0) scale(-1 1) rotate(20 128 128)"
XTERM = (
    "M 110 48 Q 110 40 118 40 L 138 40 Q 146 40 146 48 L 146 56 "
    "L 134 56 L 134 200 L 146 200 L 146 208 Q 146 216 138 216 "
    "L 118 216 Q 110 216 110 208 L 110 200 L 122 200 L 122 56 "
    "L 110 56 Z"
)
HAND_POINT = (
    "M 116 58 Q 116 46 126 46 Q 136 46 136 58 L 136 114 "
    "Q 146 108 158 112 Q 170 116 172 132 L 176 168 "
    "Q 180 198 154 204 L 116 204 Q 94 204 88 186 L 78 154 "
    "Q 74 138 86 132 Q 96 128 102 138 L 110 152 L 110 66 "
    "Q 110 56 116 58 Z"
)
HAND_OPEN = (
    "M 92 198 Q 78 196 72 180 Q 66 164 74 150 Q 80 140 90 142 "
    "L 94 144 L 94 86 Q 94 74 104 74 Q 114 74 114 86 L 114 116 "
    "L 118 116 L 118 66 Q 118 54 128 54 Q 138 54 138 66 L 138 116 "
    "L 142 116 L 142 78 Q 142 66 152 66 Q 162 66 162 78 L 162 116 "
    "L 166 116 L 166 92 Q 166 82 175 82 Q 184 82 184 92 L 184 152 "
    "Q 184 194 154 202 L 112 202 Q 96 202 92 198 Z"
)
HAND_FIST = (
    "M 94 198 Q 82 196 78 180 Q 74 166 82 154 Q 88 144 98 148 "
    "L 100 142 Q 100 128 112 126 Q 118 126 120 132 L 122 122 "
    "Q 124 112 134 112 Q 144 112 146 122 L 148 120 Q 150 110 160 110 "
    "Q 170 110 172 120 L 176 120 Q 178 110 188 112 Q 198 114 198 126 "
    "L 196 158 Q 196 198 162 204 L 116 204 Q 98 204 94 198 Z"
)
HAND_THUMB = (
    "M 94 168 Q 90 156 100 150 Q 110 144 116 154 L 126 166 "
    "Q 132 174 124 180 Q 116 186 108 178 L 98 172 Q 94 170 94 168 Z"
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
PENCIL = (
    "M 116 76 Q 116 68 124 68 L 132 68 Q 140 68 140 76 L 140 176 "
    "L 128 210 L 116 176 Z"
)
HOURGLASS = (
    "M 96 64 Q 96 56 104 56 L 152 56 Q 160 56 160 64 L 160 70 "
    "Q 160 76 156 82 L 136 106 L 156 130 Q 160 136 160 142 L 160 190 "
    "Q 160 198 152 198 L 104 198 Q 96 198 96 190 L 96 142 "
    "Q 96 136 100 130 L 120 106 L 100 82 Q 96 76 96 70 Z"
)
TEE = (
    "M 66 72 Q 66 62 76 62 L 180 62 Q 190 62 190 72 L 190 82 "
    "Q 190 92 180 92 L 138 92 L 138 174 Q 138 184 128 184 "
    "Q 118 184 118 174 L 118 92 L 76 92 Q 66 92 66 82 Z"
)


def _group(body: str, transform: str = "") -> str:
    if not transform:
        return body
    return f'<g transform="{transform}">{body}</g>'


def filled(d: str, pal: dict, transform: str = "") -> str:
    attrs = 'stroke-linejoin="round" stroke-linecap="round"'
    body = (
        f'<path d="{d}" fill="{pal["dark"]}" stroke="{pal["dark"]}" stroke-width="16" {attrs}/>'
        f'<path d="{d}" fill="{pal["rim"]}" stroke="{pal["rim"]}" stroke-width="8" {attrs}/>'
        f'<path d="{d}" fill="url(#gm)" stroke="none"/>'
    )
    return _group(body, transform)


def line(d: str, pal: dict, core: int = 7, pad: int = 3,
         dark_pad: int = 3, transform: str = "") -> str:
    attrs = 'fill="none" stroke-linejoin="round" stroke-linecap="round"'
    body = (
        f'<path d="{d}" stroke="{pal["dark"]}" stroke-width="{core + 2 * (pad + dark_pad)}" {attrs}/>'
        f'<path d="{d}" stroke="{pal["rim"]}" stroke-width="{core + 2 * pad}" {attrs}/>'
        f'<path d="{d}" stroke="url(#gm)" stroke-width="{core}" {attrs}/>'
    )
    return _group(body, transform)


def ring(cx: float, cy: float, r: float, pal: dict, core: int = 10,
         pad: int = 3, dark_pad: int = 3, transform: str = "") -> str:
    attrs = 'fill="none" stroke-linecap="round"'
    body = (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{pal["dark"]}" '
        f'stroke-width="{core + 2 * (pad + dark_pad)}" {attrs}/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{pal["rim"]}" '
        f'stroke-width="{core + 2 * pad}" {attrs}/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="url(#gm)" '
        f'stroke-width="{core}" {attrs}/>'
    )
    return _group(body, transform)


def xmark(cx: float, cy: float, pal: dict, arm: float = 7) -> str:
    path = (
        f"M {cx - arm} {cy - arm} L {cx + arm} {cy + arm} "
        f"M {cx + arm} {cy - arm} L {cx - arm} {cy + arm}"
    )
    return (
        f'<g fill="none" stroke-linecap="round">'
        f'<path d="{path}" stroke="{pal["dark"]}" stroke-width="9"/>'
        f'<path d="{path}" stroke="{pal["rim"]}" stroke-width="4"/>'
        "</g>"
    )


def pointer(pal: dict, transform: str = "") -> str:
    return filled(POINTER, pal, POINTER_TRANSFORM + " " + transform)


def left_ptr(pal: dict) -> str:
    return pointer(pal) + xmark(210, 72, pal)


def right_ptr(pal: dict) -> str:
    body = _group(pointer(pal), "translate(256 0) scale(-1 1)")
    return body + xmark(46, 72, pal)


def center_ptr(pal: dict) -> str:
    return filled(UP_ARROW, pal) + xmark(210, 72, pal)


def _copy_badge(pal: dict) -> str:
    d = (
        "M 178 172 Q 178 164 186 164 L 226 164 Q 234 164 234 172 "
        "L 234 224 Q 234 232 226 232 L 186 232 Q 178 232 178 224 Z "
        "M 188 154 Q 188 146 196 146 L 222 146 Q 230 146 230 154 L 230 162"
    )
    return line(d, pal, core=6, pad=2, dark_pad=2)


def _link_badge(pal: dict) -> str:
    d = (
        "M 186 204 L 198 192 M 210 180 L 222 168 "
        "M 182 198 L 196 212 Q 204 220 212 212 L 224 200 Q 232 192 224 184 "
        "L 214 174 Q 206 166 198 174 L 190 182 "
        "M 190 206 L 200 216 Q 208 224 216 216"
    )
    return line(d, pal, core=6, pad=2, dark_pad=2)


def _question_badge(pal: dict) -> str:
    d = (
        "M 192 176 Q 192 162 206 162 Q 220 162 220 176 "
        "Q 220 188 206 194 L 206 202"
    )
    return line(d, pal, core=6, pad=2, dark_pad=2) + (
        f'<circle cx="206" cy="214" r="5" fill="{pal["rim"]}"/>'
    )


def _no_drop_badge(pal: dict) -> str:
    return ring(204, 194, 22, pal, core=7, pad=2, dark_pad=2) + line(
        "M 190 208 L 218 180", pal, core=7, pad=2, dark_pad=2
    )


def copy_cursor(pal: dict) -> str:
    return pointer(pal) + _copy_badge(pal) + xmark(210, 72, pal)


def link_cursor(pal: dict) -> str:
    return pointer(pal) + _link_badge(pal) + xmark(210, 72, pal)


def no_drop(pal: dict) -> str:
    return pointer(pal) + _no_drop_badge(pal) + xmark(210, 72, pal)


def question_arrow(pal: dict) -> str:
    return pointer(pal) + _question_badge(pal) + xmark(210, 72, pal)


def xterm(pal: dict, angle: float = 0) -> str:
    return filled(XTERM, pal, f"rotate({angle} 128 128)") + xmark(210, 72, pal)


def crosshair(pal: dict) -> str:
    return line("M 78 128 L 178 128 M 128 78 L 128 178", pal) + xmark(210, 72, pal)


def cross(pal: dict) -> str:
    return line("M 88 128 L 168 128 M 128 88 L 128 168", pal, core=14) + xmark(210, 72, pal)


def tcross(pal: dict) -> str:
    return line("M 82 86 L 174 86 M 128 86 L 128 178", pal, core=12) + xmark(210, 72, pal)


def x_cursor(pal: dict) -> str:
    return line("M 80 80 L 176 176 M 176 80 L 80 176", pal, core=10) + xmark(210, 72, pal)


def hand_point(pal: dict) -> str:
    return filled(HAND_POINT, pal) + xmark(210, 72, pal)


def hand_open(pal: dict) -> str:
    return filled(HAND_OPEN, pal) + xmark(210, 72, pal)


def hand_fist(pal: dict) -> str:
    return filled(HAND_FIST, pal) + filled(HAND_THUMB, pal) + xmark(210, 72, pal)


def move(pal: dict) -> str:
    body = "".join(
        filled(
            STUB,
            pal,
            f"rotate({angle} 128 128) translate(128 128) scale(0.82) translate(-128 -128)",
        )
        for angle in (0, 90, 180, 270)
    )
    return body + xmark(210, 58, pal)


def up_arrow(pal: dict, angle: float = 0) -> str:
    return filled(UP_ARROW, pal, f"rotate({angle} 128 128)") + xmark(210, 72, pal)


def double_arrow(pal: dict, angle: float = 0) -> str:
    transform = f"rotate({angle} 128 128) translate(128 128) scale(0.92) translate(-128 -128)"
    return filled(DOUBLE_H, pal, transform) + xmark(210, 72, pal)


def circle(pal: dict) -> str:
    return ring(128, 128, 70, pal) + xmark(210, 72, pal)


def crossed_circle(pal: dict) -> str:
    return (
        ring(128, 128, 70, pal)
        + line("M 84 172 L 172 84", pal, core=10)
        + xmark(210, 72, pal)
    )


def pencil(pal: dict) -> str:
    return filled(PENCIL, pal, "rotate(-45 128 128)") + xmark(210, 72, pal)


def plus_cursor(pal: dict) -> str:
    return line("M 90 128 L 166 128 M 128 90 L 128 166", pal, core=16, pad=4, dark_pad=4) + xmark(210, 72, pal)


def tee(pal: dict, angle: float = 0, spark_points=None) -> str:
    return filled(TEE, pal, f"rotate({angle} 128 128)") + xmark(210, 72, pal)


def corner_l(pal: dict, d: str, spark_points=None) -> str:
    return line(d, pal, core=14, pad=4, dark_pad=4) + xmark(210, 72, pal)


def pointer_move(pal: dict) -> str:
    badge = line(
        "M 204 176 L 204 204 M 192 190 L 216 190",
        pal, core=5, pad=2, dark_pad=2,
    )
    return pointer(pal) + badge + xmark(210, 72, pal)


def context_menu(pal: dict) -> str:
    badge = line(
        "M 178 176 Q 178 168 186 168 L 226 168 Q 234 168 234 176 "
        "L 234 208 Q 234 216 226 216 L 186 216 Q 178 216 178 208 Z "
        "M 188 188 L 222 188 M 188 198 L 222 198 M 188 208 L 210 208",
        pal, core=5, pad=2, dark_pad=2,
    )
    return pointer(pal) + badge + xmark(210, 72, pal)


def zoom(pal: dict, sign: str) -> str:
    lens = ring(118, 118, 50, pal, core=9, pad=3, dark_pad=3)
    handle = line("M 154 154 L 198 198", pal, core=12, pad=3, dark_pad=3)
    symbol = "M 104 118 L 132 118"
    if sign == "+":
        symbol += " M 118 104 L 118 132"
    return lens + handle + line(symbol, pal, core=7, pad=2, dark_pad=2) + xmark(210, 72, pal)


def wait(pal: dict) -> str:
    return filled(HOURGLASS, pal) + xmark(210, 72, pal)


def left_ptr_watch(pal: dict) -> str:
    badge = filled(
        HOURGLASS,
        pal,
        "translate(204 190) scale(0.26) translate(-128 -128)",
    )
    return pointer(pal) + badge + xmark(210, 72, pal)


def wayland(pal: dict) -> str:
    return left_ptr(pal)
