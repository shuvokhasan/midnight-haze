"""Generate the monochrome line icon set into src/icons and src/ui.

Every icon is drawn on a 24x24 grid with a 1.8px rounded stroke. File names
in src/icons match qBittorrent's icon IDs (see tools/icon_ids.txt).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "src" / "icons"
UI = ROOT / "src" / "ui"

WHITE = "#E6ECF8"
MUTED = "#8E9AB8"
CYAN = "#64D2FF"
GREEN = "#30D158"
YELLOW = "#FFD60A"
RED = "#FF453A"


def p(d: str) -> str:
    return f'<path d="{d}"/>'


def c(x: float, y: float, r: float) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}"/>'


def dot(x: float, y: float, r: float = 1.2) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{{c}}" stroke="none"/>'


def r(x: float, y: float, w: float, h: float, rx: float = 2) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'


RING = c(12, 12, 9)
FOLDER = p("M3 7a2 2 0 0 1 2-2h4l2 2.5h8a2 2 0 0 1 2 2V17a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z")
DOC = p("M7 3h7l5 5v11a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z") + p("M14 3v5h5")
SHIELD = p("M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z")
WIFI = p("M3 9a13 13 0 0 1 18 0") + p("M6 12.5a9 9 0 0 1 12 0") + p("M9 16a5 5 0 0 1 6 0") + dot(12, 19)
TRIANGLE = p("M12 4l9.5 16h-19z") + p("M12 10v4.5") + dot(12, 17.3, 1.1)
REFRESH = p("M20 12a8 8 0 1 1-2.3-5.6") + p("M20 4v4h-4")
ARROW_DOWN = p("M12 5v14") + p("M6 13l6 6 6-6")
ARROW_UP = p("M12 19V5") + p("M6 11l6-6 6 6")
CHEVRONS_DOWN = p("M6 6l6 6 6-6") + p("M6 13l6 6 6-6")
CHEVRONS_UP = p("M6 11l6-6 6 6") + p("M6 18l6-6 6 6")
UPDOWN = p("M8 20V5") + p("M4 9l4-4 4 4") + p("M16 4v15") + p("M12 15l4 4 4-4")
CHECK = p("M5 12.5l4.5 4.5L19 7.5")
CROSS = p("M6 6l12 12") + p("M18 6L6 18")
USER = c(10, 8, 3) + p("M4 20a6 6 0 0 1 12 0")
GAUGE = p("M4 17a8 8 0 1 1 16 0")

# id -> (body, colour)
ICON_DEFS: dict[str, tuple[str, str]] = {
    "application-exit": (p("M14 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4") + p("M10 8l-4 4 4 4") + p("M6 12h10"), WHITE),
    "application-rss": (p("M5 5a14 14 0 0 1 14 14") + p("M5 11a8 8 0 0 1 8 8") + dot(6, 18, 1.6), WHITE),
    "application-url": (RING + p("M3 12h18") + p("M12 3c3 3 3 15 0 18") + p("M12 3c-3 3-3 15 0 18"), WHITE),
    "browser-cookies": (RING + dot(9, 9) + dot(14.5, 10.5) + dot(10, 14.5) + dot(15, 15.5), WHITE),
    "chart-line": (p("M4 4v16h16") + p("M7 15l4-5 3 3 5-7"), WHITE),
    "checked-completed": (RING + p("M8 12.5l3 3 5-6"), CYAN),
    "configure": (p("M4 7h10") + p("M18 7h2") + p("M4 17h2") + p("M10 17h10") + c(16, 7, 2) + c(8, 17, 2), WHITE),
    "connected": (WIFI, GREEN),
    "dialog-warning": (TRIANGLE, YELLOW),
    "directory": (FOLDER, WHITE),
    "disconnected": (WIFI + p("M4 4l16 16"), RED),
    "download": (p("M12 4v11") + p("M7 11l5 5 5-5") + p("M5 20h14"), WHITE),
    "downloading": (ARROW_DOWN, GREEN),
    "edit-clear": (p("M9 6h10a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H9l-6-6z") + p("M12 10l4 4") + p("M16 10l-4 4"), WHITE),
    "edit-copy": (r(8, 8, 12, 12) + p("M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"), WHITE),
    "edit-find": (c(11, 11, 6) + p("M20 20l-4.5-4.5"), WHITE),
    "edit-rename": (p("M4 20h4L19 9l-4-4L4 16z") + p("M13 7l4 4"), WHITE),
    "error": (RING + p("M12 7.5v5.5") + dot(12, 16.3), RED),
    "fileicon": (DOC, WHITE),
    "filter-active": (UPDOWN, GREEN),
    "filter-all": (p("M12 4l9 5-9 5-9-5z") + p("M3 14l9 5 9-5"), WHITE),
    "filter-inactive": (UPDOWN, MUTED),
    "filter-stalled": (CHEVRONS_DOWN, MUTED),
    "firewalled": (SHIELD + p("M12 8v5") + dot(12, 16), YELLOW),
    "folder-documents": (FOLDER + p("M8 12h8") + p("M8 15.5h5"), WHITE),
    "folder-new": (FOLDER + p("M12 10.5v6") + p("M9 13.5h6"), WHITE),
    "folder-remote": (FOLDER + c(12, 13.5, 2.5), WHITE),
    "force-recheck": (REFRESH + p("M9 12l2.2 2.2L15 10.5"), WHITE),
    "go-bottom": (p("M12 4v11") + p("M7 10l5 5 5-5") + p("M5 20h14"), WHITE),
    "go-down": (ARROW_DOWN, WHITE),
    "go-top": (p("M12 20V9") + p("M7 14l5-5 5 5") + p("M5 4h14"), WHITE),
    "go-up": (ARROW_UP, WHITE),
    "hash": (p("M9 4L7 20") + p("M17 4l-2 16") + p("M4 9h17") + p("M3 15h17"), WHITE),
    "help-about": (RING + p("M12 11v6") + dot(12, 7.7), WHITE),
    "help-contents": (RING + p("M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7") + dot(12, 16.8), WHITE),
    "insert-link": (p("M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1") + p("M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"), WHITE),
    "ip-blocked": (RING + p("M5.6 5.6l12.8 12.8"), RED),
    "list-add": (p("M12 5v14") + p("M5 12h14"), WHITE),
    "list-remove": (p("M5 12h14"), WHITE),
    "loading": (p("M12 3v4") + p("M12 17v4") + p("M3 12h4") + p("M17 12h4") + p("M5.6 5.6l2.9 2.9") + p("M15.5 15.5l2.9 2.9") + p("M5.6 18.4l2.9-2.9") + p("M15.5 8.5l2.9-2.9"), WHITE),
    "mail-inbox": (p("M3 13l3-8h12l3 8v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z") + p("M3 13h5l1 3h6l1-3h5"), WHITE),
    "name": (p("M5 6h14") + p("M12 6v13") + p("M9 19h6"), WHITE),
    "network-connect": (p("M9 3v5") + p("M15 3v5") + p("M6 8h12v3a6 6 0 0 1-12 0z") + p("M12 17v4"), WHITE),
    "network-server": (r(4, 4, 16, 7) + r(4, 13, 16, 7) + dot(7.5, 7.5) + dot(7.5, 16.5), WHITE),
    "object-locked": (r(5, 11, 14, 9) + p("M8 11V8a4 4 0 0 1 8 0v3"), WHITE),
    "pause-session": (RING + p("M10 9v6") + p("M14 9v6"), WHITE),
    "paused": (p("M9 5v14") + p("M15 5v14"), MUTED),
    "peers": (c(9, 8, 3) + p("M3 20a6 6 0 0 1 12 0") + p("M16 5.5a3 3 0 0 1 0 5.5") + p("M17.5 14.5A6 6 0 0 1 21 20"), WHITE),
    "peers-add": (USER + p("M19 8v6") + p("M16 11h6"), WHITE),
    "peers-remove": (USER + p("M16 11h6"), WHITE),
    "plugins": (r(4, 4, 7, 7, 1.5) + r(13, 4, 7, 7, 1.5) + r(4, 13, 7, 7, 1.5) + p("M16.5 13v7") + p("M13 16.5h7"), WHITE),
    "preferences-advanced": (c(12, 12, 3.5) + p("M12 3v3") + p("M12 18v3") + p("M3 12h3") + p("M18 12h3") + p("M5.6 5.6l2.1 2.1") + p("M16.3 16.3l2.1 2.1") + p("M5.6 18.4l2.1-2.1") + p("M16.3 7.7l2.1-2.1"), WHITE),
    "preferences-bittorrent": (c(6, 12, 2.5) + c(18, 6, 2.5) + c(18, 18, 2.5) + p("M8.2 10.9l7.6-3.8") + p("M8.2 13.1l7.6 3.8"), WHITE),
    "preferences-desktop": (r(3, 4, 18, 12) + p("M9 20h6") + p("M12 16v4"), WHITE),
    "preferences-webui": (r(3, 4, 18, 16) + p("M3 9h18") + dot(6, 6.5, 0.9) + dot(8.8, 6.5, 0.9), WHITE),
    "queued": (RING + p("M12 7v5l3 2"), YELLOW),
    "ratio": (p("M6 18L18 6") + c(7, 7, 2.2) + c(17, 17, 2.2), WHITE),
    "reannounce": (p("M4 12a8 8 0 0 1 14-5.3") + p("M20 4v4h-4") + p("M20 12a8 8 0 0 1-14 5.3") + p("M4 20v-4h4"), WHITE),
    "rss_read_article": (DOC + p("M9 13h6") + p("M9 16.5h4"), MUTED),
    "rss_unread_article": (DOC + p("M9 13h6") + p("M9 16.5h4"), CYAN),
    "security-high": (SHIELD + p("M8.5 12l2.5 2.5 4.5-5"), GREEN),
    "security-low": (SHIELD + p("M9.5 9.5l5 5") + p("M14.5 9.5l-5 5"), YELLOW),
    "set-location": (p("M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z") + c(12, 10, 2.5), WHITE),
    "slow": (GAUGE + p("M12 17l-4.5-4"), YELLOW),
    "slow_off": (GAUGE + p("M12 17l3.5-6"), WHITE),
    "speedometer": (GAUGE + p("M12 17l3.5-6") + dot(12, 17, 1.4), WHITE),
    "stalledDL": (CHEVRONS_DOWN, "#8FDCAA"),
    "stalledUP": (CHEVRONS_UP, "#7C9CFF"),
    "stopped": (r(6, 6, 12, 12), MUTED),
    "system-log-out": (p("M10 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h4") + p("M14 8l4 4-4 4") + p("M18 12H8"), WHITE),
    "tags": (p("M3 12V5a2 2 0 0 1 2-2h7l9 9-9 9z") + dot(8, 8, 1.4), WHITE),
    "task-complete": (CHECK, GREEN),
    "task-reject": (CROSS, RED),
    "torrent-creator": (DOC + p("M12 11.5v6") + p("M9 14.5h6"), WHITE),
    "torrent-magnet": (p("M6 4v8a6 6 0 0 0 12 0V4h-4v8a2 2 0 0 1-4 0V4z") + p("M6 8h4") + p("M14 8h4"), WHITE),
    "torrent-start": (p("M8 5l11 7-11 7z"), WHITE),
    "torrent-start-forced": (p("M4 6l8 6-8 6z") + p("M13 6l8 6-8 6z"), WHITE),
    "torrent-stop": (r(6, 6, 12, 12), WHITE),
    "tracker-error": (RING + p("M9 9l6 6") + p("M15 9l-6 6"), RED),
    "tracker-warning": (TRIANGLE, YELLOW),
    "trackerless": (RING + p("M5.6 5.6l12.8 12.8"), MUTED),
    "trackers": (c(12, 12, 2) + p("M8 8a5.5 5.5 0 0 0 0 8") + p("M16 8a5.5 5.5 0 0 1 0 8") + p("M5 5a10 10 0 0 0 0 14") + p("M19 5a10 10 0 0 1 0 14"), WHITE),
    "upload": (ARROW_UP, CYAN),
    "view-categories": (p("M9 6h11") + p("M9 12h11") + p("M9 18h11") + dot(5, 6) + dot(5, 12) + dot(5, 18), WHITE),
    "view-preview": (p("M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z") + c(12, 12, 3), WHITE),
    "view-refresh": (REFRESH, WHITE),
    "view-statistics": (p("M5 20v-9") + p("M12 20V4") + p("M19 20v-6"), WHITE),
    "wallet-open": (p("M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"), WHITE),
}

# Small glyphs referenced from stylesheet.qss (not qBittorrent icon IDs).
UI_DEFS: dict[str, tuple[str, str, float]] = {
    "check": (p("M5.5 12.5l4 4 9-9.5"), "#FFFFFF", 2.6),
    "dash": (p("M6 12h12"), "#FFFFFF", 2.6),
    "radio": ('<circle cx="12" cy="12" r="5" fill="{c}" stroke="none"/>', "#FFFFFF", 0),
    "arrow-down": (p("M7 10l5 5 5-5"), "#C9D3E8", 2.2),
    "arrow-up": (p("M7 14l5-5 5 5"), "#C9D3E8", 2.2),
    "arrow-right": (p("M10 7l5 5-5 5"), "#C9D3E8", 2.2),
    "arrow-left": (p("M14 7l-5 5 5 5"), "#C9D3E8", 2.2),
}

# Icons shown in the main toolbar capsule: drawn with a heavier stroke.
TOOLBAR_ICONS = {
    "insert-link", "list-add", "list-remove", "torrent-start", "torrent-stop",
    "go-top", "go-up", "go-down", "go-bottom", "torrent-creator", "configure",
    "object-locked", "edit-find",
}
TOOLBAR_STROKE = 2.4

# Stock icons deliberately kept: they are the app's brand mark in the menu bar.
KEEP_STOCK = {"qbittorrent-tray", "qbittorrent-tray-dark", "qbittorrent-tray-light"}


def svg(body: str, colour: str, width: float = 1.8) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        f'fill="none" stroke="{colour}" stroke-width="{width}" '
        'stroke-linecap="round" stroke-linejoin="round">'
        + body.replace("{c}", colour)
        + "</svg>\n"
    )


def main() -> None:
    ICONS.mkdir(parents=True, exist_ok=True)
    UI.mkdir(parents=True, exist_ok=True)
    for name, (body, colour) in ICON_DEFS.items():
        width = TOOLBAR_STROKE if name in TOOLBAR_ICONS else 1.8
        (ICONS / f"{name}.svg").write_text(svg(body, colour, width))
    for name, (body, colour, width) in UI_DEFS.items():
        (UI / f"{name}.svg").write_text(svg(body, colour, width))
    print(f"wrote {len(ICON_DEFS)} icons, {len(UI_DEFS)} ui glyphs")


if __name__ == "__main__":
    main()
