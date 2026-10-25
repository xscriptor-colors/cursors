from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CLI_ROOT))

from cursors_cli import design_version  # noqa: E402
from cursors_cli.builder import build, manifest_text  # noqa: E402
from cursors_cli.palette import (  # noqa: E402
    DEFAULT_SIZES,
    PaletteSpec,
    SpecError,
)

BASE = {
    "gradient": ["#4328a8", "#7c3aed", "#4d96ff", "#ff9f43", "#f59e0b"],
}


class PaletteSpecTests(unittest.TestCase):
    def test_defaults(self) -> None:
        spec = PaletteSpec.from_dict(BASE)
        self.assertTrue(spec.name.startswith("Xscriptor-X-"))
        self.assertEqual(spec.sizes, DEFAULT_SIZES)
        self.assertEqual(spec.rim, "#ffe884")
        self.assertEqual(spec.contour, "#171717")
        self.assertEqual(len(spec.stops), 5)
        self.assertEqual(len(spec.spec_hash), 12)

    def test_explicit_fields(self) -> None:
        spec = PaletteSpec.from_dict({
            **BASE,
            "name": "Xscriptor-X-berlin",
            "sizes": [48, 24, 32, 24],
            "rim": "#FFFFFF",
            "contour": "#000000",
            "comment": "test",
            "website": "https://example.test",
        })
        self.assertEqual(spec.name, "Xscriptor-X-berlin")
        self.assertEqual(spec.sizes, (24, 32, 48))
        self.assertEqual(spec.rim, "#ffffff")
        self.assertEqual(spec.contour, "#000000")
        self.assertEqual(spec.comment, "test")
        self.assertEqual(spec.website, "https://example.test")

    def test_bad_hex(self) -> None:
        with self.assertRaises(SpecError):
            PaletteSpec.from_dict({"gradient": ["red"] * 5})
        with self.assertRaises(SpecError):
            PaletteSpec.from_dict({**BASE, "rim": "#fff"})

    def test_bad_gradient_length(self) -> None:
        with self.assertRaises(SpecError):
            PaletteSpec.from_dict({"gradient": ["#000000"] * 4})
        with self.assertRaises(SpecError):
            PaletteSpec.from_dict({"gradient": "not-a-list"})

    def test_bad_sizes(self) -> None:
        for sizes in ([], [24, 300], [24, "32"], [True]):
            with self.assertRaises(SpecError):
                PaletteSpec.from_dict({**BASE, "sizes": sizes})

    def test_bad_name(self) -> None:
        for name in ("", "../escape", "has space", "a" * 129):
            with self.assertRaises(SpecError):
                PaletteSpec.from_dict({**BASE, "name": name})

    def test_hash_is_stable_and_changes(self) -> None:
        one = PaletteSpec.from_dict(BASE)
        two = PaletteSpec.from_dict(dict(BASE))
        three = PaletteSpec.from_dict({
            **BASE,
            "gradient": ["#000000"] * 5,
        })
        self.assertEqual(one.spec_hash, two.spec_hash)
        self.assertNotEqual(one.spec_hash, three.spec_hash)
        self.assertEqual(len(design_version()), 12)

    def test_with_overrides(self) -> None:
        spec = PaletteSpec.from_dict(BASE)
        self.assertEqual(spec.with_sizes([32, 24]).sizes, (24, 32))
        self.assertEqual(spec.with_name("Xscriptor-X-test").name, "Xscriptor-X-test")
        with self.assertRaises(SpecError):
            spec.with_name("bad name")

    def test_example_file(self) -> None:
        spec = PaletteSpec.load(CLI_ROOT / "examples" / "cursor-spec.json")
        self.assertEqual(spec.name, "Xscriptor-X-example")
        self.assertEqual(spec.sizes, (24, 32, 48))

    def test_manifest_contract(self) -> None:
        text = manifest_text(
            "Xscriptor-X-test",
            Path("/tmp/bitmaps"),
            Path("/tmp/themes"),
            (24, 32, 48),
            "test comment",
            "https://example.test",
        )
        self.assertIn('name = "Xscriptor-X-test"', text)
        self.assertIn('comment = "test comment"', text)
        self.assertIn("x11_sizes = [24, 32, 48]", text)
        self.assertIn('[cursors."left_ptr"]', text)
        self.assertIn('png = "left_ptr.png"', text)
        self.assertIn(
            'x11_symlinks = ["arrow", "default", "top_left_arrow"]', text
        )
        self.assertIn('png = "wait-*.png"', text)

    def test_dry_run(self) -> None:
        spec = PaletteSpec.from_dict(BASE)
        with tempfile.TemporaryDirectory() as tmp:
            meta = build(spec, tmp, dry_run=True)
        self.assertTrue(meta["dry_run"])
        self.assertIsNone(meta["path"])
        self.assertEqual(meta["cursors"], 78)
        self.assertEqual(meta["entries"], 179)


if __name__ == "__main__":
    unittest.main()
