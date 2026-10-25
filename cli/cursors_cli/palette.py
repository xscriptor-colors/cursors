"""Palette specification contract for cursors-cli.

A spec only describes the cursor colours; it does not know about base16 or
theme-sync. This keeps the integration surface small:

    {
      "name": "Xscriptor-X-berlin",
      "gradient": ["#0a0a0a", "#4d96ff", "#ff9f43", "#f59e0b", "#fce566"],
      "rim": "#ffe884",
      "contour": "#171717",
      "sizes": [24, 32, 48]
    }

``name``, ``rim``, ``contour`` and ``sizes`` are optional. The default name is
derived from the colours and sizes, so the same spec always maps to the same
theme.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

DEFAULT_SIZES = (24, 32, 48)
DEFAULT_RIM = "#ffe884"
DEFAULT_CONTOUR = "#171717"
DEFAULT_WEBSITE = "https://github.com/xscriptor-colors/cursors"
GRADIENT_OFFSETS = ("0%", "28%", "52%", "76%", "100%")

_HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class SpecError(ValueError):
    """Raised for malformed palette specs."""


@dataclass(frozen=True)
class PaletteSpec:
    name: str
    gradient: tuple[str, ...]
    rim: str
    contour: str
    sizes: tuple[int, ...]
    comment: str
    website: str

    @classmethod
    def load(cls, path: str | Path) -> "PaletteSpec":
        try:
            raw = Path(path).read_text(encoding="utf-8")
        except OSError as exc:
            raise SpecError(f"cannot read {path}: {exc}") from exc
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SpecError(f"invalid JSON in {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise SpecError("the spec root must be a JSON object")
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PaletteSpec":
        gradient_raw = data.get("gradient")
        if not isinstance(gradient_raw, list):
            raise SpecError("'gradient' must be an array of 5 colours")
        if len(gradient_raw) != 5:
            raise SpecError("'gradient' must contain exactly 5 colours")
        gradient = tuple(_hex(value, f"gradient[{i}]")
                         for i, value in enumerate(gradient_raw))

        rim = _hex(data.get("rim", DEFAULT_RIM), "rim")
        contour = _hex(data.get("contour", DEFAULT_CONTOUR), "contour")
        sizes = _sizes(data.get("sizes", DEFAULT_SIZES))

        raw_name = data.get("name")
        name = (_default_name(gradient, rim, contour, sizes)
                if raw_name is None else _name(raw_name))
        comment = str(data.get("comment") or f"{name} palette variant")
        website = str(data.get("website") or DEFAULT_WEBSITE)

        return cls(
            name=name,
            gradient=gradient,
            rim=rim,
            contour=contour,
            sizes=sizes,
            comment=comment,
            website=website,
        )

    def with_sizes(self, sizes: Iterable[int]) -> "PaletteSpec":
        return replace(self, sizes=_sizes(list(sizes)))

    def with_name(self, name: str) -> "PaletteSpec":
        return replace(self, name=_name(name))

    @property
    def stops(self) -> tuple[tuple[str, str], ...]:
        return tuple(zip(GRADIENT_OFFSETS, self.gradient))

    @property
    def spec_hash(self) -> str:
        payload = {
            "name": self.name,
            "gradient": list(self.gradient),
            "rim": self.rim,
            "contour": self.contour,
            "sizes": list(self.sizes),
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def _hex(value: Any, field: str) -> str:
    text = str(value or "")
    if not _HEX_RE.match(text):
        raise SpecError(f"'{field}' must be #rrggbb, got {text!r}")
    return text.lower()


def _name(value: Any) -> str:
    text = str(value or "")
    if not _NAME_RE.match(text):
        raise SpecError(
            "'name' must start with a letter or digit and contain only "
            "letters, digits, '.', '_' or '-' (max 128 chars)"
        )
    return text


def _sizes(value: Any) -> tuple[int, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
        raise SpecError("'sizes' must be an array of integers")
    sizes: list[int] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, int):
            raise SpecError("'sizes' must contain integers")
        if not 8 <= item <= 256:
            raise SpecError("'sizes' entries must be between 8 and 256")
        if item not in sizes:
            sizes.append(item)
    if not sizes:
        raise SpecError("'sizes' cannot be empty")
    return tuple(sorted(sizes))


def _default_name(
    gradient: Iterable[str], rim: str, contour: str, sizes: Iterable[int]
) -> str:
    payload = json.dumps(
        {
            "gradient": list(gradient),
            "rim": rim,
            "contour": contour,
            "sizes": list(sizes),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    suffix = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]
    return f"Xscriptor-X-{suffix}"
