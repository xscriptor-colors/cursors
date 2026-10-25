# Manual

Everything you need to install, apply, customize and troubleshoot the Xscriptor
cursor themes.

## Contents

1. [What this repository provides](#1-what-this-repository-provides)
2. [Requirements](#2-requirements)
3. [Installation](#3-installation)
4. [Applying the theme](#4-applying-the-theme)
5. [Using the packs](#5-using-the-packs)
6. [Customizing](#6-customizing)
7. [Build pipeline](#7-build-pipeline)
8. [Validation](#8-validation)
9. [Troubleshooting](#9-troubleshooting)
10. [License and trademarks](#10-license-and-trademarks)

## 1. What this repository provides

Two original X11/Xcursor themes for Linux:

| Theme | Look |
|-------|------|
| `Xscriptor-X` | Violet → blue → orange gradient body, gold rim, dark contour, X sparks |
| `Xscriptor-Berlin` | Monochrome body, white rim, dark contour, X sparks |

Both packs contain the same 78 cursor shapes and 101 standard aliases
(179 entries per pack), in 10 nominal sizes from 16 to 96 px. The `wait` and
`left_ptr_watch` cursors are animated: a skull opens and closes its jaw over
12 frames at 70 ms per frame.

The repository ships the full SVG sources and the Python pipeline that turns
them into Xcursor binaries, so nothing has to be reverse-engineered later.

## 2. Requirements

To use the prebuilt themes you only need a Linux desktop that supports Xcursor.
The themes also work on Wayland compositors (Hyprland, Sway, etc.) and on
XWayland.

To build from source:

| Requirement | Why |
|-------------|-----|
| Python 3.10+ | Runs the generators and validators |
| `clickgen` | Provides `ctgen`, which writes the Xcursor files |
| Pillow | Renders and inspects the PNG bitmaps |
| `rsvg-convert` (`librsvg`) | Converts SVG sources to PNG |

Install the Python packages:

```bash
pip install -r scripts/requirements.txt
```

Install `rsvg-convert` from your distribution, for example:

```bash
sudo pacman -S librsvg       # Arch
sudo apt install librsvg2-bin # Debian/Ubuntu
sudo dnf install librsvg2-tools # Fedora
```

## 3. Installation

### 3.1 Build and install

```bash
git clone https://github.com/xscriptor-colors/cursors.git
cd cursors
make install
```

`make install` regenerates the SVG sources, builds both themes and copies them
to:

```
~/.local/share/icons/Xscriptor-X
~/.local/share/icons/Xscriptor-Berlin
```

### 3.2 Manual copy

If you already built the themes or received the folders, copy them directly:

```bash
mkdir -p ~/.local/share/icons
cp -r build/themes/Xscriptor-X ~/.local/share/icons/
cp -r build/themes/Xscriptor-Berlin ~/.local/share/icons/
```

`~/.icons` also works if your desktop searches that path.

### 3.3 Verify the install

```bash
ls ~/.local/share/icons/Xscriptor-X/cursors | head
readlink ~/.local/share/icons/Xscriptor-X/cursors/default
```

The second command should print `left_ptr`, which confirms that the alias
symlinks are intact.

### 3.4 Uninstall

```bash
rm -rf ~/.local/share/icons/Xscriptor-X
rm -rf ~/.local/share/icons/Xscriptor-Berlin
```

Then switch back to another cursor theme in your desktop settings.

## 4. Applying the theme

### Hyprland

Apply immediately in the running session:

```bash
hyprctl setcursor Xscriptor-X 24
# or:
hyprctl setcursor Xscriptor-Berlin 24
```

Make it persistent. With the Lua configuration (Hyprland 0.55+), set the
environment in `~/.config/hypr/env.lua`:

```lua
hl.env("XCURSOR_THEME", "Xscriptor-X")
hl.env("XCURSOR_SIZE", "24")
```

Also update the cursor autostart in `~/.config/hypr/autostart.lua`. Otherwise a
`gsettings` call can restore the previous theme at the next login:

```lua
hl.exec_cmd("hyprctl setcursor Xscriptor-X 24")
hl.exec_cmd("gsettings set org.gnome.desktop.interface cursor-theme 'Xscriptor-X'")
hl.exec_cmd("gsettings set org.gnome.desktop.interface cursor-size 24")
```

With the legacy hyprlang configuration, use:

```ini
env = XCURSOR_THEME,Xscriptor-X
env = XCURSOR_SIZE,24
exec-once = hyprctl setcursor Xscriptor-X 24
```

A logout/login applies the environment variables to every process.

### Other Wayland compositors

Export the variables for the whole session. A portable option is
`~/.config/environment.d/90-cursors.conf`:

```ini
XCURSOR_THEME=Xscriptor-X
XCURSOR_SIZE=24
```

Log out and back in. Some compositors also expose a runtime command:

```bash
# Sway
swaymsg seat seat0 xcursor_theme Xscriptor-X 24
```

### GNOME

```bash
gsettings set org.gnome.desktop.interface cursor-theme 'Xscriptor-X'
gsettings set org.gnome.desktop.interface cursor-size 24
```

You can also use GNOME Tweaks → Appearance → Cursor.

### KDE Plasma

Use System Settings → Appearance → Cursors, or set it from a terminal.
Plasma 6:

```bash
kwriteconfig6 --file kdeglobals --group General --key cursorTheme Xscriptor-X
```

Plasma 5:

```bash
kwriteconfig5 --file kdeglobals --group General --key cursorTheme Xscriptor-X
```

Log out and back in.

### Xfce

Settings → Mouse and Touchpad → Theme, or:

```bash
xfconf-query -c xsettings -p /Gtk/CursorThemeName -s Xscriptor-X
xfconf-query -c xsettings -p /Gtk/CursorThemeSize -s 24
```

### X11 / i3 / other window managers

Add to `~/.Xresources`:

```
Xcursor.theme: Xscriptor-X
Xcursor.size: 24
```

Merge it:

```bash
xrdb -merge ~/.Xresources
```

Export the theme for new processes in `~/.xprofile` or `~/.xsession`:

```bash
export XCURSOR_THEME=Xscriptor-X
export XCURSOR_SIZE=24
```

### GTK apps

Some GTK apps read their own configuration instead of `gsettings`. Set the
theme in both files:

```ini
# ~/.config/gtk-3.0/settings.ini
# ~/.config/gtk-4.0/settings.ini
[Settings]
gtk-cursor-theme-name=Xscriptor-X
gtk-cursor-theme-size=24
```

Restart the app after editing.

### Qt apps

On Wayland, Qt normally follows the compositor cursor. On X11 you can set it
with qt5ct/qt6ct:

```ini
# ~/.config/qt5ct/qt5ct.conf or ~/.config/qt6ct/qt6ct.conf
[cursor]
cursor_theme=Xscriptor-X
cursor_size=24
```

The `XCURSOR_THEME` and `XCURSOR_SIZE` environment variables also cover most Qt
setups.

### Electron, Chromium and Java

These applications usually follow the session `XCURSOR_THEME`. Restart the
application after changing the theme. If it was started before the environment
variable existed, it keeps the old cursor until restarted.

### Flatpak and Snap

Flatpak applications may need the theme exported into their sandbox:

```bash
flatpak override --user --env=XCURSOR_THEME=Xscriptor-X
flatpak override --user --env=XCURSOR_SIZE=24
```

If the theme is not visible inside the sandbox, expose the icon directory:

```bash
flatpak override --user --filesystem=~/.local/share/icons:ro
```

Snap confinement varies by application; exporting the environment variables is
usually enough.

## 5. Using the packs

### Cursor coverage

Each pack ships 78 real cursors and 101 aliases, including the complete
`X11/cursorfont.h` set. Aliases are symlinks, so one change to a cursor also
updates every name that points to it.

### Sizes

The theme includes these nominal sizes:

```
16, 20, 22, 24, 28, 32, 40, 48, 64, 96
```

The desktop picks the closest size to `XCURSOR_SIZE` or the compositor setting.
24 px is a good default; 32 px suits high-density displays.

### Animated cursors

`wait` and `left_ptr_watch` are the only animated entries. They contain 12
frames at 70 ms. The animation is part of the Xcursor file, so no extra daemon
is required.

## 6. Customizing

### Change the palette

For a one-off variant that should not touch the committed sources, use
[`cursors-cli`](#palette-variants-cursors-cli) instead. To change the default X
and Berlin packs, open `scripts/art.py` and edit `PALETTES`:

```python
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
```

Then rebuild:

```bash
make generate
make build
make install
make preview
```

### Add or edit a cursor

1. Add a drawing function to `scripts/art.py`. It must return an SVG fragment
   string, or a list of fragments for an animated cursor.
2. Add an entry to `scripts/spec.py`:

```python
Cursor(
    "my_cursor",
    (128, 128),              # hotspot on the 256x256 canvas
    one(art.my_cursor),      # or art.my_animated_cursor
    ("alias1", "alias2"),    # standard names that symlink to it
)
```

3. Rebuild and validate:

```bash
make generate build validate install
```

### Add a new pack

A pack is a palette plus a theme name:

1. Add a palette to `PALETTES` in `scripts/art.py`.
2. Add the pack name to `PACKS` in `scripts/generate.py`.
3. Add the theme metadata to `PACKS` in `scripts/build.py`.
4. Add the pack to the loops in `scripts/preview.py` and `scripts/validate.py`
   if you want previews and validation for it.
5. Run `make generate build validate preview install`.

### Hotspots

All coordinates live on a 256×256 canvas. The dark contour extends roughly
24 px beyond the path, so keep artwork at least 24 px away from the canvas edge.
The hotspot is converted automatically to every nominal size by `clickgen`.

### Animated frames

Return a list of SVG fragments from the drawing function. Files are written as
`name-000.svg`, `name-001.svg`, and so on. The manifest uses the glob
`name-*.png`, and the frame delay is `x11_delay` in `scripts/build.py` (70 ms by
default).

### Aliases

Aliases are declared in the `Cursor` entry in `scripts/spec.py`. `ctgen`
creates them as relative symlinks inside the theme's `cursors/` directory.

## 7. Build pipeline

### Commands

| Command | Action |
|---------|--------|
| `make` | Generate, build, validate and render previews |
| `make generate` | Write SVG sources to `src/` |
| `make build` | Render PNGs, write manifests, run `ctgen` |
| `make install` | Build and copy both themes to `~/.local/share/icons` |
| `make preview` | Full contact sheets in `preview/` and `docs/` |
| `make validate` | Coverage, format, hotspot and animation checks |
| `make clean` | Remove `build/` and `preview/` |

### Dependencies check

`make` starts with a `check` target that verifies `ctgen`, `rsvg-convert` and
Pillow. It stops with a clear message if something is missing.

### Output

```
build/bitmaps/<pack>/       rendered PNG frames
build/manifests/<pack>.toml clickgen manifests
build/themes/<theme>/       Xcursor themes ready to install
```

`build/` is not committed; it is fully reproducible from `src/`.

### Palette variants (`cursors-cli`)

`cli/` is a self-contained builder for palette-specific themes. It never
modifies `src/`: every intermediate file goes to a temporary directory and the
final theme is published atomically to `--out-dir`. Variants use the **X**
pack only; Berlin is monochrome and is installed once.

```bash
python3 cli/cursors-cli \
  --spec cli/examples/cursor-spec.json \
  --out-dir build/variants \
  --sizes 24 32 48
```

The spec is deliberately small:

```json
{
  "name": "Xscriptor-X-berlin",
  "gradient": ["#0a0a0a", "#4d96ff", "#ff9f43", "#f59e0b", "#fce566"],
  "rim": "#ffe884",
  "contour": "#171717",
  "sizes": [24, 32, 48]
}
```

Only `gradient` (exactly five `#rrggbb` colours) is required. The five colours
map to the 0%, 28%, 52%, 76% and 100% stops. `name`, `rim`,
`contour`, `sizes`, `comment` and `website` are optional. If `name` is
omitted, the CLI derives a stable name from the colours and sizes
(`Xscriptor-X-<hash8>`). Defaults are `rim=#ffe884`, `contour=#171717` and
`sizes=[24, 32, 48]`.

| Flag | Meaning |
|------|---------|
| `--spec FILE` | Palette spec JSON (required) |
| `--out-dir DIR` | Where the built theme is published (default `build/variants`) |
| `--sizes PX...` | Override the spec sizes |
| `--name NAME` | Override the spec theme name |
| `--force` | Replace an existing output theme |
| `--dry-run` | Validate the spec and print metadata without building |
| `--work-dir DIR` | Parent directory for the temporary build |
| `--keep-work` | Keep the intermediate SVGs/PNGs/manifest |
| `--quiet` | Suppress progress messages (JSON only) |

The command prints one JSON object to stdout and progress messages to stderr:

```json
{"theme":"Xscriptor-X-berlin","path":"/abs/...","sizes":[24,32,48],
 "design_version":"...","spec_hash":"...","cursors":78,"entries":179,
 "bytes":1577427,"dry_run":false,"build_seconds":0.43}
```

Exit codes: `2` invalid spec, `3` missing `ctgen`/`rsvg-convert`, `4` build
failure, `5` output exists without `--force`.

This is the contract for theme-sync: write a spec, call the CLI, cache the
result by `design_version` + `spec_hash` + sizes, and switch the active theme
with `hyprctl setcursor` / `gsettings`. The CLI does not touch the running
session or the user's configuration.

## 8. Validation

Run:

```bash
make validate
```

The validator checks:

- every cursor name shipped by the system themes in `/usr/share/icons`,
- every glyph from `X11/cursorfont.h`,
- the Xcursor magic and image chunks,
- that every hotspot is inside its bitmap,
- that `wait` and `left_ptr_watch` really contain multiple frames,
- that every theme has `index.theme`, `cursor.theme` and no broken symlinks.

Run `make test-cli` to check the palette-spec parser and manifest contract
without building a theme.

A successful run ends with:

```
Xscriptor-X: 179 entries
  OK: all 151 reference names and 75 cursorfont glyphs present
```

## 9. Troubleshooting

### The theme is installed but nothing changes

1. Apply it at runtime: `hyprctl setcursor Xscriptor-X 24`.
2. Make sure `XCURSOR_THEME` is exported to the session, not only to the
   terminal where you ran the command.
3. Check that the autostart does not reset it with `gsettings`.
4. Log out and back in so already-running applications inherit the variable.

### Only some applications use the old cursor

- GTK apps: check `~/.config/gtk-3.0/settings.ini` and
  `~/.config/gtk-4.0/settings.ini`.
- Qt apps: check qt5ct/qt6ct or the environment variables.
- Electron/Chromium/Java: restart the application.
- Flatpak: export the env vars inside the sandbox with `flatpak override`.

### The cursor is too small or too large

Set `XCURSOR_SIZE` to the desired value and re-login. The theme includes sizes
from 16 to 96 px; 24 px is the default used by the examples.

### `ctgen: command not found`

```bash
pip install -r scripts/requirements.txt
```

### `rsvg-convert: command not found`

Install `librsvg` with your package manager (see
[Requirements](#2-requirements)).

### `FileExistsError` while building

An old theme directory is interfering. `scripts/build.py` removes it
automatically; if you built manually, remove `build/themes/<theme>` and run
`make build` again.

### A cursor looks clipped

Its artwork is too close to the 256×256 canvas edge. Keep at least 24 px of
margin for the dark contour and rebuild.

### `make validate` reports a missing cursor

A system theme ships a name that is not in `scripts/spec.py`. Add it as a new
entry or as an alias to an existing cursor, then rebuild.

## 10. License and trademarks

- Code (`scripts/`, `Makefile`): MIT. See [LICENSE](LICENSE).
- Artwork (`src/`, generated cursors, `docs/` previews): CC BY 4.0. See
  [LICENSE-ART](LICENSE-ART).
- Names and logos: see [TRADEMARKS.md](TRADEMARKS.md).

The cursor slot names (`left_ptr`, `watch`, `crosshair`, `X_cursor`, etc.) are
functional identifiers from the X11/Xcursor conventions and are not claimed.
