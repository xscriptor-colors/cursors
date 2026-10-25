"""Cursor catalogue: artwork, hotspots and X11 name/alias table.

Kept in code so the SVG output, the clickgen manifest and the size checks all
read the same coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import art


def one(fn: Callable[[dict], str]) -> Callable[[dict], list[str]]:
    def draw(pal: dict) -> list[str]:
        return [fn(pal)]

    return draw


def rotated(fn: Callable[[dict, float], str], angle: float) -> Callable[[dict], list[str]]:
    return one(lambda pal: fn(pal, angle))


@dataclass(frozen=True)
class Cursor:
    key: str
    hotspot: tuple[int, int]
    draw: Callable[[dict], list[str]]
    aliases: tuple[str, ...] = field(default_factory=tuple)

    @property
    def animated(self) -> bool:
        return len(self.draw(art.PALETTES["x"])) > 1

    @property
    def png(self) -> str:
        return f"{self.key}-*.png" if self.animated else f"{self.key}.png"


CURSORS: tuple[Cursor, ...] = (
    Cursor(
        "left_ptr",
        (40, 32),
        one(art.left_ptr),
        ("arrow", "default", "top_left_arrow"),
    ),
    Cursor(
        "right_ptr",
        (216, 32),
        one(art.right_ptr),
        ("draft_large", "draft_small"),
    ),
    Cursor("center_ptr", (128, 44), one(art.center_ptr)),
    Cursor(
        "left_ptr_watch",
        (40, 32),
        art.left_ptr_watch,
        (
            "00000000000000020006000e7e9ffc3f",
            "08e8e1c95fe2fc01f976f1e063a24ccd",
            "3ecb610c1bf2410f44200f48c40d3599",
            "half-busy",
            "progress",
        ),
    ),
    Cursor("wait", (128, 128), art.wait, ("clock", "watch")),
    Cursor(
        "hand2",
        (128, 42),
        one(art.hand_point),
        (
            "9d800788f1b08800ae810202380a0822",
            "e29285e634086352946a0e7090d73106",
            "hand",
            "pointer",
            "pointing_hand",
        ),
    ),
    Cursor("hand1", (128, 140), one(art.hand_open), ("grab", "openhand")),
    Cursor(
        "grabbing",
        (128, 150),
        one(art.hand_fist),
        ("closedhand", "dnd-move", "dnd-none", "fcf21c00b30f7e3f83fe0dfd12e71cff"),
    ),
    Cursor("xterm", (128, 128), one(art.xterm), ("ibeam", "text")),
    Cursor(
        "vertical-text",
        (128, 128),
        rotated(art.xterm, 90),
    ),
    Cursor("crosshair", (128, 128), one(art.crosshair)),
    Cursor("cross", (128, 128), one(art.cross), ("cross_reverse", "diamond_cross")),
    Cursor("tcross", (128, 128), one(art.tcross), ("color-picker",)),
    Cursor("X_cursor", (128, 128), one(art.x_cursor), ("pirate", "x-cursor")),
    Cursor(
        "move",
        (128, 128),
        one(art.move),
        (
            "4498f0e0c1937ffe01fd06f973665830",
            "9081237383d90e509aa00f00170e968f",
            "all-resize",
            "all-scroll",
            "exchange",
            "fleur",
            "size_all",
        ),
    ),
    Cursor(
        "question_arrow",
        (40, 32),
        one(art.question_arrow),
        (
            "5c6cd98b3f3ebcb1f9c7f1c204630408",
            "d9ce0ab605698f320427677b458ad60b",
            "help",
            "left_ptr_help",
            "whats_this",
        ),
    ),
    Cursor(
        "crossed_circle",
        (128, 128),
        one(art.crossed_circle),
        ("03b6e0fcb3499374a867c041f52298f0", "not-allowed"),
    ),
    Cursor("circle", (128, 128), one(art.circle), ("forbidden",)),
    Cursor(
        "copy",
        (40, 32),
        one(art.copy_cursor),
        (
            "1081e37283d90000800003c07f3ef6bf",
            "6407b0e94181790501fd1e167b474872",
            "b66166c04f8c3109214a4fbd64a50fc8",
        ),
    ),
    Cursor(
        "link",
        (40, 32),
        one(art.link_cursor),
        (
            "3085a0e285430894940527032f8b26df",
            "640fb0e74195791501fd1ed57b41487f",
            "a2a266d0498c3104214a47bd64ab0fc8",
        ),
    ),
    Cursor("dnd-ask", (40, 32), one(art.question_arrow)),
    Cursor("dnd-copy", (40, 32), one(art.copy_cursor)),
    Cursor("dnd-link", (40, 32), one(art.link_cursor), ("alias",)),
    Cursor(
        "dnd_no_drop",
        (40, 32),
        one(art.no_drop),
        ("dnd-no-drop", "no-drop"),
    ),
    Cursor("pointer-move", (40, 32), one(art.pointer_move)),
    Cursor("context-menu", (40, 32), one(art.context_menu)),
    Cursor("pencil", (128, 212), one(art.pencil), ("draft",)),
    Cursor("plus", (128, 128), one(art.plus_cursor), ("cell",)),
    Cursor(
        "dotbox",
        (128, 128),
        one(art.dotbox),
        ("dot_box_mask", "draped_box", "icon", "target"),
    ),
    Cursor("zoom-in", (106, 106), one(lambda p: art.zoom(p, "+"))),
    Cursor("zoom-out", (106, 106), one(lambda p: art.zoom(p, "-"))),
    Cursor("wayland-cursor", (40, 32), one(art.wayland)),
    Cursor(
        "sb_up_arrow",
        (128, 44),
        one(art.up_arrow),
        ("based_arrow_up", "up-arrow", "up_arrow"),
    ),
    Cursor(
        "sb_down_arrow",
        (128, 212),
        rotated(art.up_arrow, 180),
        ("based_arrow_down", "down-arrow"),
    ),
    Cursor("sb_left_arrow", (44, 128), rotated(art.up_arrow, -90), ("left-arrow",)),
    Cursor("sb_right_arrow", (212, 128), rotated(art.up_arrow, 90), ("right-arrow",)),
    Cursor(
        "sb_h_double_arrow",
        (128, 128),
        one(art.double_arrow),
        (
            "028006030e0e7ebffc7f7070c0600140",
            "14fef782d02440884392942c1120523",
            "col-resize",
            "ew-resize",
            "h_double_arrow",
            "size-hor",
            "size_hor",
            "split_h",
        ),
    ),
    Cursor(
        "sb_v_double_arrow",
        (128, 128),
        rotated(art.double_arrow, 90),
        (
            "00008160000006810000408080010102",
            "2870a09082c103050810ffdffffe0204",
            "double_arrow",
            "ns-resize",
            "row-resize",
            "size-ver",
            "size_ver",
            "split_v",
            "v_double_arrow",
        ),
    ),
    Cursor(
        "fd_double_arrow",
        (128, 128),
        rotated(art.double_arrow, -45),
        (
            "fcf1c3c7cd4491d801f1e1c78f100000",
            "nesw-resize",
            "size-bdiag",
            "size_bdiag",
        ),
    ),
    Cursor(
        "bd_double_arrow",
        (128, 128),
        rotated(art.double_arrow, 45),
        (
            "c7088f0f3e6c8088236ef8e1e3e70000",
            "nwse-resize",
            "size-fdiag",
            "size_fdiag",
        ),
    ),
    Cursor("top_side", (128, 128), rotated(art.double_arrow, 90), ("n-resize",)),
    Cursor("bottom_side", (128, 128), rotated(art.double_arrow, 90), ("s-resize",)),
    Cursor("left_side", (128, 128), one(art.double_arrow), ("w-resize",)),
    Cursor("right_side", (128, 128), one(art.double_arrow), ("e-resize",)),
    Cursor("top_left_corner", (128, 128), rotated(art.double_arrow, 45), ("nw-resize",)),
    Cursor("top_right_corner", (128, 128), rotated(art.double_arrow, -45), ("ne-resize",)),
    Cursor("bottom_left_corner", (128, 128), rotated(art.double_arrow, -45), ("sw-resize",)),
    Cursor(
        "bottom_right_corner",
        (128, 128),
        rotated(art.double_arrow, 45),
        ("se-resize", "sizing"),
    ),
    Cursor(
        "top_tee",
        (128, 77),
        one(lambda p: art.tee(p, 0, ((54, 200, 12, 10), (202, 200, 12, 10)))),
    ),
    Cursor(
        "bottom_tee",
        (128, 179),
        one(lambda p: art.tee(p, 180, ((54, 56, 12, 10), (202, 56, 12, 10)))),
    ),
    Cursor(
        "left_tee",
        (77, 128),
        one(lambda p: art.tee(p, -90, ((202, 54, 12, 10), (202, 202, 12, 10)))),
    ),
    Cursor(
        "right_tee",
        (179, 128),
        one(lambda p: art.tee(p, 90, ((54, 54, 12, 10), (54, 202, 12, 10)))),
    ),
    Cursor(
        "ul_angle",
        (62, 62),
        one(lambda p: art.corner_l(p, art.CORNER_L, ((198, 198, 12, 10),))),
    ),
    Cursor(
        "ur_angle",
        (194, 62),
        one(
            lambda p: art.corner_l(
                p, "M 194 122 L 194 62 L 134 62", ((58, 198, 12, 10),)
            )
        ),
    ),
    Cursor(
        "ll_angle",
        (62, 194),
        one(
            lambda p: art.corner_l(
                p, "M 62 134 L 62 194 L 122 194", ((198, 58, 12, 10),)
            )
        ),
    ),
    Cursor(
        "lr_angle",
        (194, 194),
        one(
            lambda p: art.corner_l(
                p, "M 194 134 L 194 194 L 134 194", ((58, 58, 12, 10),)
            )
        ),
    ),
    # Legacy X11 cursorfont glyphs, redrawn from scratch.
    Cursor("dot", (128, 128), one(art.dot)),
    Cursor("heart", (128, 128), one(art.heart)),
    Cursor("star", (128, 128), one(art.star)),
    Cursor("iron_cross", (128, 128), one(art.iron_cross)),
    Cursor("rtl_logo", (128, 128), one(art.rtl_logo)),
    Cursor("boat", (128, 128), one(art.boat)),
    Cursor("sailboat", (128, 128), one(art.sailboat)),
    Cursor("coffee_mug", (128, 128), one(art.coffee_mug)),
    Cursor("spraycan", (128, 128), one(art.spraycan)),
    Cursor("gumby", (128, 128), one(art.gumby)),
    Cursor("man", (128, 128), one(art.man)),
    Cursor("gobbler", (128, 128), one(art.gobbler)),
    Cursor("bogosity", (128, 128), one(art.bogosity)),
    Cursor("box_spiral", (128, 128), one(art.box_spiral)),
    Cursor("shuttle", (128, 128), one(art.shuttle)),
    Cursor("trek", (128, 128), one(art.trek)),
    Cursor("spider", (128, 128), one(art.spider)),
    Cursor("umbrella", (128, 128), one(art.umbrella)),
    Cursor("mouse", (128, 96), one(art.mouse)),
    Cursor("leftbutton", (128, 96), one(art.leftbutton)),
    Cursor("middlebutton", (128, 96), one(art.middlebutton)),
    Cursor("rightbutton", (128, 96), one(art.rightbutton)),
)

# remove accidental duplicate keys while keeping order
_seen: set[str] = set()
CURSORS = tuple(c for c in CURSORS if not (c.key in _seen or _seen.add(c.key)))
