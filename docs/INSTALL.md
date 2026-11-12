# Installing Xscriptor Cursors on Linux

`Xscriptor-X` and `Xscriptor-Berlin` are standard Xcursor themes. The theme
files and the install paths are the same on every Linux distribution. The
distribution only changes how the build dependencies are installed and which
desktop settings are used to select the theme.

Both themes work on X11, on Wayland compositors that read Xcursor themes
(Hyprland, Sway, GNOME, KDE Plasma and Xfce), and in XWayland applications.

## 1. Choose a theme

| Theme | Look |
|-------|------|
| `Xscriptor-X` | Full 16-colour palette gradient, gold rim, dark contour, X outside |
| `Xscriptor-Berlin` | Monochrome body, white rim, dark contour, X outside |

Both packs contain 78 cursor shapes and 101 standard aliases, for 179 entries
per pack, in sizes from 16 to 96 px. You can install both themes side by side
and select one at a time.

## 2. Install a prebuilt theme

Use this method when you already have the theme folders, either from a release
archive or from `build/themes/` after running the build. It does not require
Python, clickgen or librsvg.

### Per-user installation

```bash
mkdir -p "$HOME/.local/share/icons"

cp -rT Xscriptor-X "$HOME/.local/share/icons/Xscriptor-X"
cp -rT Xscriptor-Berlin "$HOME/.local/share/icons/Xscriptor-Berlin"
```

If you are copying from a clone of this repository:

```bash
cp -rT build/themes/Xscriptor-X "$HOME/.local/share/icons/Xscriptor-X"
cp -rT build/themes/Xscriptor-Berlin "$HOME/.local/share/icons/Xscriptor-Berlin"
```

The legacy `~/.icons` directory also works on desktops that still search it,
but `~/.local/share/icons` is the recommended XDG location.

### System-wide installation

Install to `/usr/share/icons` when the theme must be available to the login
manager, to applications running as root, or to every user on the machine:

```bash
sudo mkdir -p /usr/share/icons

sudo cp -rT build/themes/Xscriptor-X /usr/share/icons/Xscriptor-X
sudo cp -rT build/themes/Xscriptor-Berlin /usr/share/icons/Xscriptor-Berlin

sudo find /usr/share/icons/Xscriptor-X -type d -exec chmod 755 {} +
sudo find /usr/share/icons/Xscriptor-X -type f -exec chmod 644 {} +
sudo find /usr/share/icons/Xscriptor-Berlin -type d -exec chmod 755 {} +
sudo find /usr/share/icons/Xscriptor-Berlin -type f -exec chmod 644 {} +
```

A system-wide install makes the theme available, but the login manager may
still have its own cursor setting. GDM, SDDM and other greeters are configured
separately.

## 3. Build and install from source

### Requirements

| Requirement | Why |
|-------------|-----|
| Linux with Xcursor support | Runs the installed themes |
| Python 3.10 or newer | Runs the generators, builders and validators |
| `clickgen` (`ctgen`) | Writes the Xcursor files |
| Pillow | Renders and inspects the PNG bitmaps |
| `rsvg-convert` (`librsvg`) | Converts the SVG sources to PNG |

Install `rsvg-convert` with the package manager of your distribution:

| Distribution | Package |
|--------------|---------|
| Arch Linux | `librsvg` |
| Debian / Ubuntu | `librsvg2-bin` |
| Fedora | `librsvg2-tools` |
| openSUSE | `librsvg` or the package that provides `rsvg-convert` |

Install the Python dependencies in a virtual environment. This avoids the
externally managed environment restrictions of recent distributions:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r scripts/requirements.txt
```

### Build and copy

```bash
make install
```

`make install` regenerates the SVG sources from `scripts/`, builds both themes
in `build/themes/`, and copies them to:

```text
~/.local/share/icons/Xscriptor-X
~/.local/share/icons/Xscriptor-Berlin
```

If you only want the built folders without installing them:

```bash
make build
```

Then copy `build/themes/Xscriptor-X` and `build/themes/Xscriptor-Berlin` with
the commands from section 2.

The generated binaries are not committed. The SVG sources in `src/` are the
single source of truth, and `build/themes` is reproducible from them.

## 4. Activate the theme

### Hyprland

Apply the theme immediately in the running session:

```bash
hyprctl setcursor Xscriptor-X 24
```

Or use `Xscriptor-Berlin` instead of `Xscriptor-X`.

To make it persistent with the Lua configuration used by Hyprland 0.55 and
newer, add the environment variables to `~/.config/hypr/env.lua`:

```lua
hl.env("XCURSOR_THEME", "Xscriptor-X")
hl.env("XCURSOR_SIZE", "24")
```

Add the runtime command to `~/.config/hypr/autostart.lua`:

```lua
hl.exec_cmd("hyprctl setcursor Xscriptor-X 24")
hl.exec_cmd("gsettings set org.gnome.desktop.interface cursor-theme 'Xscriptor-X'")
hl.exec_cmd("gsettings set org.gnome.desktop.interface cursor-size 24")
```

The `gsettings` lines prevent a GTK or GNOME setting from restoring the
previous cursor theme at the next login.

With the legacy hyprlang configuration, use:

```ini
env = XCURSOR_THEME,Xscriptor-X
env = XCURSOR_SIZE,24
exec-once = hyprctl setcursor Xscriptor-X 24
```

Hyprland reads Xcursor themes directly. Hyprcursor is optional and is not
required by these themes.

### Other Wayland compositors

Set the variables for the whole session in
`~/.config/environment.d/90-cursors.conf`:

```ini
XCURSOR_THEME=Xscriptor-X
XCURSOR_SIZE=24
```

Log out and back in. For Sway, the theme can also be changed at runtime:

```bash
swaymsg seat seat0 xcursor_theme Xscriptor-X 24
```

### GNOME

```bash
gsettings set org.gnome.desktop.interface cursor-theme 'Xscriptor-X'
gsettings set org.gnome.desktop.interface cursor-size 24
```

The same options are available in GNOME Tweaks under Appearance and Cursors.

### KDE Plasma

Use System Settings, Appearance, Cursors. From a terminal, Plasma 6 uses:

```bash
kwriteconfig6 --file kdeglobals --group General --key cursorTheme Xscriptor-X
kwriteconfig6 --file kdeglobals --group General --key cursorSize 24
```

Plasma 5 uses the same command with `kwriteconfig5`. Log out and back in.

### Xfce

Use Settings, Mouse and Touchpad, Theme, or run:

```bash
xfconf-query -c xsettings -p /Gtk/CursorThemeName -s Xscriptor-X
xfconf-query -c xsettings -p /Gtk/CursorThemeSize -s 24
```

### X11, i3, bspwm and other window managers

Add the theme to `~/.Xresources`:

```text
Xcursor.theme: Xscriptor-X
Xcursor.size: 24
```

Merge the file and export the variables for new processes:

```bash
xrdb -merge "$HOME/.Xresources"
```

Add the export to `~/.xprofile` or `~/.xsession`:

```bash
export XCURSOR_THEME=Xscriptor-X
export XCURSOR_SIZE=24
```

Log out and back in so the session and the window manager inherit the values.

### GTK applications

Some GTK applications read their own configuration instead of `gsettings`.
Set the theme in both files:

```ini
# ~/.config/gtk-3.0/settings.ini
# ~/.config/gtk-4.0/settings.ini
[Settings]
gtk-cursor-theme-name=Xscriptor-X
gtk-cursor-theme-size=24
```

Restart the application after editing the files.

### Qt applications

On Wayland, Qt normally follows the compositor cursor. On X11, set the theme
with qt5ct or qt6ct:

```ini
# ~/.config/qt5ct/qt5ct.conf or ~/.config/qt6ct/qt6ct.conf
[cursor]
cursor_theme=Xscriptor-X
cursor_size=24
```

The `XCURSOR_THEME` and `XCURSOR_SIZE` environment variables also cover most
Qt setups.

### Electron, Chromium and Java applications

These applications usually follow `XCURSOR_THEME` from the session. Restart
the application after changing the theme. An application started before the
variable was exported keeps the old cursor until it is restarted.

### Flatpak and Snap

Flatpak applications may need the theme exported inside their sandbox:

```bash
flatpak override --user --env=XCURSOR_THEME=Xscriptor-X
flatpak override --user --env=XCURSOR_SIZE=24
```

If the theme is not visible inside the sandbox, expose the icon directory:

```bash
flatpak override --user --filesystem="$HOME/.local/share/icons:ro"
```

Snap confinement varies by application. Exporting the environment variables is
usually enough; restart the application afterwards.

## 5. Verify the installation

Check that the theme is complete and that the alias symlinks are intact:

```bash
ls "$HOME/.local/share/icons/Xscriptor-X/cursors" | wc -l
readlink "$HOME/.local/share/icons/Xscriptor-X/cursors/default"
```

The first command should print `179`. The second command should print
`left_ptr`.

Then apply the theme at runtime, or log out and back in:

```bash
hyprctl setcursor Xscriptor-X 24
```

## 6. Update or uninstall

To update, build the new version and copy it over the installed folder:

```bash
make build

cp -rT build/themes/Xscriptor-X "$HOME/.local/share/icons/Xscriptor-X"
cp -rT build/themes/Xscriptor-Berlin "$HOME/.local/share/icons/Xscriptor-Berlin"
```

Then apply the theme again or log out and back in.

To uninstall a per-user installation:

```bash
rm -rf "$HOME/.local/share/icons/Xscriptor-X"
rm -rf "$HOME/.local/share/icons/Xscriptor-Berlin"
```

For a system-wide installation, remove the same directories from
`/usr/share/icons` with `sudo`. Select another cursor theme in your desktop
settings before removing the one that is currently active.

## 7. Palette variants

Xcursor themes are static files: a theme cannot recolor itself while the
session is running. To make the cursors follow a palette, generate one theme
per palette and switch the theme name when the palette changes.

The `cursors-cli` tool builds a variant from a JSON specification without
touching the curated `src/` tree:

```bash
python3 cli/cursors-cli --spec cli/examples/cursor-spec.json --out-dir build/variants
```

Each variant is a complete theme with its own name. Install the variants side
by side and switch them at runtime:

```bash
hyprctl setcursor Xscriptor-X-Madrid 24
```

Use the same command in the palette-change hook after the terminal, editor and
desktop colours have been updated. See the palette variants section in the
[README](../README.md#palette-variants-cursors-cli) for the specification
format.

## 8. Troubleshooting

### The theme is installed but nothing changes

1. Apply it at runtime with `hyprctl setcursor Xscriptor-X 24`.
2. Make sure `XCURSOR_THEME` is exported to the whole session, not only to the
   terminal where you ran the command.
3. Check that the login autostart does not reset it with `gsettings`.
4. Log out and back in so running applications inherit the new environment.

### Only some applications use the old cursor

- GTK applications: check `~/.config/gtk-3.0/settings.ini` and
  `~/.config/gtk-4.0/settings.ini`.
- Qt applications: check qt5ct or qt6ct, or the environment variables.
- Electron, Chromium and Java applications: restart the application.
- Flatpak applications: export the variables inside the sandbox with
  `flatpak override`.

### The cursor is too small or too large

Set `XCURSOR_SIZE` to the required value and log out and back in. The themes
include sizes from 16 to 96 px. The examples use 24 px.

### `ctgen: command not found`

Activate the virtual environment and install the Python dependencies:

```bash
. .venv/bin/activate
pip install -r scripts/requirements.txt
```

### `rsvg-convert: command not found`

Install `librsvg` with the package manager of your distribution. See the table
in section 3.

### A cursor looks clipped or a name is missing

Run the validator after building:

```bash
make validate
```

The validator checks coverage, Xcursor format, hotspots and clipped frames.
See the [manual](MANUAL.md#9-troubleshooting) for the complete troubleshooting
guide.

## 9. License and trademarks

- Code in `scripts/` and the `Makefile` is MIT. See [LICENSE](../LICENSE).
- Artwork in `src/` and the generated cursors is CC BY 4.0. See
  [LICENSE-ART](../LICENSE-ART).
- Names and logos are covered by [TRADEMARKS.md](../TRADEMARKS.md).
