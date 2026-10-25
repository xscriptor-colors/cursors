"""cursors-cli command line entry point."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__, design_version
from .builder import BuildError, DependencyError, TargetExistsError, build
from .palette import PaletteSpec, SpecError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cursors-cli",
        description=(
            "Build a palette-specific Xscriptor-X Xcursor theme from a JSON "
            "spec. Intermediate files stay in a temporary directory; the "
            "final theme is published atomically to --out-dir."
        ),
    )
    parser.add_argument(
        "--spec", required=True,
        help="path to the palette spec JSON",
    )
    parser.add_argument(
        "--out-dir", default="build/variants",
        help="directory that receives the built theme (default: build/variants)",
    )
    parser.add_argument(
        "--sizes", nargs="+", type=int, metavar="PX",
        help="override the nominal sizes from the spec (e.g. 24 32 48)",
    )
    parser.add_argument(
        "--name", help="override the theme name from the spec",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="replace an existing theme directory",
    )
    parser.add_argument(
        "--work-dir", help="parent directory for the temporary build directory",
    )
    parser.add_argument(
        "--keep-work", action="store_true",
        help="keep the intermediate SVGs, PNGs and manifest for debugging",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="validate the spec and print metadata without building",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="only print the final JSON metadata",
    )
    parser.add_argument(
        "--version", action="version",
        version=f"cursors-cli {__version__} (design {design_version()})",
    )
    args = parser.parse_args(argv)

    try:
        spec = PaletteSpec.load(args.spec)
        if args.sizes:
            spec = spec.with_sizes(args.sizes)
        if args.name:
            spec = spec.with_name(args.name)
        metadata = build(
            spec,
            args.out_dir,
            force=args.force,
            work_dir=args.work_dir,
            keep_work=args.keep_work,
            dry_run=args.dry_run,
            quiet=args.quiet,
        )
    except SpecError as exc:
        print(f"cursors-cli: invalid spec: {exc}", file=sys.stderr)
        return 2
    except DependencyError as exc:
        print(f"cursors-cli: {exc}", file=sys.stderr)
        return 3
    except TargetExistsError as exc:
        print(f"cursors-cli: {exc}", file=sys.stderr)
        return 5
    except BuildError as exc:
        print(f"cursors-cli: build failed: {exc}", file=sys.stderr)
        return 4
    except KeyboardInterrupt:
        print("cursors-cli: interrupted", file=sys.stderr)
        return 130

    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
