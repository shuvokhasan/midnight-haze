# Glass theme for qBittorrent

A dark "frosted glass" theme for the qBittorrent desktop app (written against 5.2.3, macOS).
It follows `REFARENCES/THEME-THUMBRULE.md` as far as a `.qbtheme` allows.

## Install

1. Open qBittorrent, then **Preferences > Behavior > Interface**.
2. Tick **Use custom UI Theme** and pick `dist/glass.qbtheme`.
3. Restart qBittorrent.

For quick iteration you can pick `src/config.json` instead of the `.qbtheme` file.
qBittorrent then loads the `src/` folder directly, so edits only need an app restart, not a rebuild.

To remove the theme, untick **Use custom UI Theme** and restart.

## Build

```sh
python3 -m venv .venv
.venv/bin/pip install PySide6 Pillow
.venv/bin/python tools/build.py              # writes dist/glass.qbtheme
.venv/bin/python tools/build.py --background # also regenerates src/background.png
.venv/bin/python tools/preview.py            # writes build/preview-*.png
```

`tools/preview.py` renders the theme on a mock window that copies qBittorrent's widget classes.
It is a fast check while editing; the real app is the final check.

## Layout

| Path | Purpose |
| --- | --- |
| `src/stylesheet.qss` | All widget styling. Colour tokens are listed in the header comment. |
| `src/config.json` | qBittorrent colour IDs: palette, transfer list states, log, pieces bar. |
| `src/background.png` | Generated gradient that stands in for the wallpaper behind the glass. |
| `src/icons/` | Generated line icons, named after qBittorrent icon IDs. |
| `src/ui/` | Generated glyphs used by the stylesheet (check marks, arrows). |
| `tools/make_icons.py` | Icon definitions. Edit here, not the SVG files. |
| `tools/make_background.py` | Background blobs and colours. |
| `tools/make_capsule.py` | Toolbar search capsule and progress fill images (`src/ui/search-cap.png`, `src/ui/progress-chunk.png`). |
| `tools/icon_ids.txt`, `tools/color_ids.txt` | ID lists taken from qBittorrent 5.2.3 `uithemecommon.h`; the build validates against them. |

## What a theme cannot do

The reference mockups are concept renders. These parts are not possible from a `.qbtheme`:

- Real blur or wallpaper bleed-through. The gradient is baked into the window.
- Layout changes: search pill in the title bar, extra header buttons, a footer outside the window.
- Moving toolbar items. qBittorrent fixes the order: action buttons, flexible gap, search field, lock.
  The two toolbar capsules are assembled from the items themselves. The round ends of the left capsule
  match the first and last button by their English text (`Open`, `Preferences`); in another language
  those two ends are square.
- Clipping the progress fill to the track. The fill is a capsule image; when the fill is narrower than
  14px the two round ends overlap and the shape is not exact.
- Rounded tooltip windows. The border line is rounded, the window is not.
- The native macOS title bar and window corner radius.
- Rounded corners on a selected table row, and multi-line expansion of the selected row.
- A different fill for completed and in-progress bars. QSS cannot select on a bar's value.
- A QSS font on progress bars. It breaks the label position in the transfer list, so the bars use the default font.
- Tray icons are left as stock so the menu bar keeps the qBittorrent mark.
