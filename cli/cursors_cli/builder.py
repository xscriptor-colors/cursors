"""Build a single palette-specific Xscriptor-X Xcursor theme.

The pipeline mirrors scripts/build.py but keeps every intermediate file in a
temporary directory and publishes an atomic copy to ``--out-dir``. The curated
``src/`` tree is never modified.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import art
import spec as cursor_spec

from . import design_version
from .palette import PaletteSpec

CANVAS = 256
DELAY_MS = 70
PACK = "x"


class DependencyError(RuntimeError):
    """A required external tool is missing."""


class BuildError(RuntimeError):
    """The theme could not be built."""


class TargetExistsError(BuildError):
    """The output theme already exists and --force was not used."""


def _log(quiet: bool, message: str) -> None:
    if not quiet:
        print(f"cursors-cli: {message}", file=sys.stderr)


def _require_tools() -> None:
    missing = [name for name in ("ctgen", "rsvg-convert")
               if shutil.which(name) is None]
    if missing:
        raise DependencyError(
            "missing required tool(s): " + ", ".join(missing)
            + " (install clickgen and librsvg)"
        )


def _write_svgs(pal: dict, src_dir: Path) -> int:
    count = 0
    for cursor in cursor_spec.CURSORS:
        frames = cursor.draw(pal)
        if len(frames) == 1:
            names = [f"{cursor.key}.svg"]
        else:
            names = [f"{cursor.key}-{i:03d}.svg" for i in range(len(frames))]
        for name, body in zip(names, frames):
            (src_dir / name).write_text(
                art.svg_document(body, pal), encoding="utf-8"
            )
            count += 1
    return count


def _render_pngs(src_dir: Path, png_dir: Path) -> int:
    svgs = sorted(src_dir.glob("*.svg"))

    def render(svg: Path) -> None:
        png = png_dir / f"{svg.stem}.png"
        try:
            subprocess.run(
                ["rsvg-convert", "-w", str(CANVAS), "-h", str(CANVAS),
                 "-o", str(png), str(svg)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or "").strip().splitlines()
            raise BuildError(
                f"rsvg-convert failed for {svg.name}: "
                f"{detail[-1] if detail else 'unknown error'}"
            ) from exc

    with ThreadPoolExecutor() as pool:
        list(pool.map(render, svgs))
    return len(svgs)


def _q(value: Any) -> str:
    """JSON string literals are valid TOML basic strings for our values."""
    return json.dumps(str(value), ensure_ascii=False)


def manifest_text(
    theme_name: str,
    bitmaps_dir: Path,
    themes_dir: Path,
    sizes: tuple[int, ...],
    comment: str,
    website: str,
) -> str:
    lines = [
        "[theme]",
        f"name = {_q(theme_name)}",
        f"comment = {_q(comment)}",
        f"website = {_q(website)}",
        "",
        "[config]",
        f"bitmaps_dir = {_q(bitmaps_dir)}",
        f"out_dir = {_q(themes_dir)}",
        'platforms = ["x11"]',
        "",
        "[cursors]",
        "",
        "[cursors.fallback_settings]",
        f"x11_sizes = {list(sizes)}",
        "x_hotspot = 128",
        "y_hotspot = 128",
        f"x11_delay = {DELAY_MS}",
        "",
    ]
    for cursor in cursor_spec.CURSORS:
        lines.append(f'[cursors."{cursor.key}"]')
        lines.append(f"png = {_q(cursor.png)}")
        lines.append(f"x_hotspot = {cursor.hotspot[0]}")
        lines.append(f"y_hotspot = {cursor.hotspot[1]}")
        lines.append(f"x11_name = {_q(cursor.key)}")
        if cursor.aliases:
            links = ", ".join(_q(alias) for alias in cursor.aliases)
            lines.append(f"x11_symlinks = [{links}]")
        lines.append("")
    return "\n".join(lines)


def _run_ctgen(manifest: Path) -> None:
    try:
        subprocess.run(
            ["ctgen", str(manifest)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip().splitlines()
        raise BuildError(
            "ctgen failed: " + (detail[-1] if detail else "unknown error")
        ) from exc


def _validate_theme(theme_dir: Path) -> int:
    if not (theme_dir / "index.theme").is_file():
        raise BuildError(f"missing index.theme in {theme_dir}")
    if not (theme_dir / "cursor.theme").is_file():
        raise BuildError(f"missing cursor.theme in {theme_dir}")

    cursors_dir = theme_dir / "cursors"
    if not cursors_dir.is_dir():
        raise BuildError(f"missing cursors directory in {theme_dir}")

    entries = list(cursors_dir.iterdir())
    for entry in entries:
        if entry.is_symlink():
            if not entry.exists():
                raise BuildError(f"broken symlink: {entry.name}")
            continue
        try:
            magic = entry.read_bytes()[:4]
        except OSError as exc:
            raise BuildError(f"cannot read {entry.name}: {exc}") from exc
        if magic != b"Xcur":
            raise BuildError(f"{entry.name} is not an XCursor file")
    return len(entries)


def _publish(theme_src: Path, target: Path, force: bool) -> None:
    if target.exists() or target.is_symlink():
        if not force:
            raise TargetExistsError(
                f"{target} already exists; pass --force to replace it"
            )
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.parent / f".{target.name}.tmp-{os.getpid()}"
    if staging.exists():
        shutil.rmtree(staging, ignore_errors=True)
    try:
        shutil.copytree(theme_src, staging, symlinks=True)
        os.replace(staging, target)
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


def _tree_size(root: Path) -> int:
    total = 0
    for path in root.rglob("*"):
        if path.is_file() and not path.is_symlink():
            try:
                total += path.stat().st_size
            except OSError:
                pass
    return total


def _entry_count() -> int:
    return sum(1 + len(cursor.aliases) for cursor in cursor_spec.CURSORS)


def build(
    spec: PaletteSpec,
    out_dir: str | Path,
    *,
    theme_name: str | None = None,
    force: bool = False,
    work_dir: str | Path | None = None,
    keep_work: bool = False,
    dry_run: bool = False,
    quiet: bool = False,
) -> dict[str, Any]:
    if theme_name:
        spec = spec.with_name(theme_name)

    out_root = Path(out_dir).expanduser().resolve()
    target = out_root / spec.name

    if not dry_run and (target.exists() or target.is_symlink()) and not force:
        raise TargetExistsError(
            f"{target} already exists; pass --force to replace it"
        )

    if dry_run:
        return {
            "theme": spec.name,
            "path": None,
            "sizes": list(spec.sizes),
            "gradient": list(spec.gradient),
            "rim": spec.rim,
            "contour": spec.contour,
            "design_version": design_version(),
            "spec_hash": spec.spec_hash,
            "cursors": len(cursor_spec.CURSORS),
            "entries": _entry_count(),
            "bytes": 0,
            "dry_run": True,
            "build_seconds": 0.0,
        }

    _require_tools()

    base = Path(work_dir).expanduser().resolve() if work_dir else None
    if base is not None:
        base.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="cursors-cli-",
                                 dir=str(base) if base else None))
    started = time.monotonic()
    try:
        src_dir = work / "src"
        png_dir = work / "bitmaps"
        themes_dir = work / "themes"
        src_dir.mkdir()
        png_dir.mkdir()
        themes_dir.mkdir()

        pal = {"stops": list(spec.stops), "rim": spec.rim, "dark": spec.contour}
        art.PALETTES[PACK] = pal

        _log(quiet, f"generating SVG frames for {spec.name}")
        frame_count = _write_svgs(pal, src_dir)
        _log(quiet, f"{frame_count} SVG frames; rendering PNGs")
        png_count = _render_pngs(src_dir, png_dir)
        _log(quiet, f"{png_count} PNG frames; writing clickgen manifest")

        manifest = work / "manifest.toml"
        manifest.write_text(
            manifest_text(spec.name, png_dir, themes_dir, spec.sizes,
                          spec.comment, spec.website),
            encoding="utf-8",
        )
        _log(quiet, "running ctgen")
        _run_ctgen(manifest)

        built = themes_dir / spec.name
        entries = _validate_theme(built)
        _publish(built, target, force)

        elapsed = time.monotonic() - started
        _log(quiet, f"published {target} ({entries} entries, {elapsed:.2f}s)")
        return {
            "theme": spec.name,
            "path": str(target),
            "sizes": list(spec.sizes),
            "gradient": list(spec.gradient),
            "rim": spec.rim,
            "contour": spec.contour,
            "design_version": design_version(),
            "spec_hash": spec.spec_hash,
            "cursors": len(cursor_spec.CURSORS),
            "entries": entries,
            "bytes": _tree_size(target),
            "dry_run": False,
            "build_seconds": round(elapsed, 3),
        }
    finally:
        if keep_work:
            print(f"cursors-cli: work directory kept at {work}", file=sys.stderr)
        else:
            shutil.rmtree(work, ignore_errors=True)
