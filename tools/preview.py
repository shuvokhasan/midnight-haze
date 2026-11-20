"""Render the built theme on a mock qBittorrent window and save screenshots.

The mock mirrors the widget classes qBittorrent uses (so selectors such as
`TransferListFiltersWidget` and `PropertiesWidget` match) and paints table
progress bars the same way ProgressBarPainter does. It is a preview aid only;
the real app is the final check.

Usage: .venv/bin/python tools/preview.py   -> build/preview-*.png
"""
import json
import sys
from pathlib import Path

from PySide6.QtCore import QFile, QResource, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPalette, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QProgressBar, QProxyStyle, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpinBox, QSplitter, QStackedWidget, QStyle,
    QStyledItemDelegate, QStyleOptionProgressBar, QTabWidget, QToolBar,
    QTreeView, QVBoxLayout, QWidget,
)

ROOT = Path(__file__).resolve().parent.parent
THEME = ROOT / "dist" / "glass.qbtheme"
OUT = ROOT / "build"

# qBittorrent hides the four queue buttons when torrent queueing is off.
QUEUEING = "--queueing" in sys.argv


def icon(name: str) -> QIcon:
    return QIcon(f":/uitheme/icons/{name}.svg")


def load_theme(app: QApplication) -> dict:
    if not QResource.registerResource(str(THEME), "/uitheme"):
        sys.exit(f"cannot register {THEME}")
    for required in ("stylesheet.qss", "config.json", "background.png", "icons/filter-all.svg"):
        if not QFile.exists(f":/uitheme/{required}"):
            sys.exit(f"missing in theme: {required}")

    f = QFile(":/uitheme/config.json")
    f.open(QFile.ReadOnly)
    colors = json.loads(bytes(f.readAll()).decode())["colors"]

    palette = app.palette()
    for key, value in colors.items():
        if not key.startswith("Palette."):
            continue
        role_name = key.removeprefix("Palette.")
        group = QPalette.Normal
        if role_name.endswith("Disabled"):
            role_name = role_name.removesuffix("Disabled")
            group = QPalette.Disabled
        role = getattr(QPalette, role_name)
        if group == QPalette.Normal:
            palette.setColor(QPalette.Active, role, QColor(value))
            palette.setColor(QPalette.Inactive, role, QColor(value))
        else:
            palette.setColor(group, role, QColor(value))
    app.setPalette(palette)

    f = QFile(":/uitheme/stylesheet.qss")
    f.open(QFile.ReadOnly)
    app.setStyleSheet(bytes(f.readAll()).decode())
    return colors


class ProgressDelegate(QStyledItemDelegate):
    """Same drawing path as qBittorrent's ProgressBarPainter."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dummy = QProgressBar()
        fusion = QProxyStyle("fusion")
        fusion.setParent(self.dummy)
        self.dummy.setStyle(fusion)

    def paint(self, painter, option, index):
        progress = int(index.data(Qt.UserRole) or 0)
        opt = QStyleOptionProgressBar()
        opt.initFrom(self.dummy)
        opt.maximum = 100
        opt.minimum = 0
        opt.progress = progress
        opt.text = f"{progress}%"
        opt.textVisible = True
        opt.rect = option.rect.adjusted(0, 1, 0, -1)
        opt.state = option.state | QStyle.State_Horizontal
        painter.save()
        style = self.dummy.style()
        style.drawPrimitive(QStyle.PE_PanelItemViewItem, option, painter, option.widget)
        style.drawControl(QStyle.CE_ProgressBar, opt, painter, self.dummy)
        painter.restore()


class TransferListFiltersWidget(QWidget):
    def __init__(self):
        super().__init__()
        inner = QWidget()
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(0, 2, 0, 0)
        lay.setSpacing(2)
        lay.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        sections = {
            "Status": [("filter-all", "All (21)"), ("downloading", "Downloading (0)"),
                       ("upload", "Seeding (21)"), ("checked-completed", "Completed (21)"),
                       ("torrent-start", "Running (21)"), ("stopped", "Stopped (0)"),
                       ("filter-active", "Active (2)"), ("filter-inactive", "Inactive (19)"),
                       ("filter-stalled", "Stalled (19)"), ("error", "Errored (0)")],
            "Categories": [("view-categories", "All (21)"), ("view-categories", "Uncategorized (21)")],
            "Tags": [("tags", "All (21)"), ("tags", "Untagged (21)")],
            "Trackers": [("trackers", "All (21)"), ("trackerless", "Trackerless (0)")],
        }
        for n, (title, rows) in enumerate(sections.items()):
            box = QCheckBox(title)
            box.setChecked(True)
            lay.addWidget(box)
            lst = QListWidget()
            lst.setFrameShape(QFrame.NoFrame)
            lst.setIconSize(QSize(16, 16))
            lst.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            lst.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            for ic, text in rows:
                lst.addItem(QListWidgetItem(icon(ic), text))
            lst.setFixedHeight(lst.sizeHintForRow(0) * len(rows) + 4)
            if n == 0:
                lst.setCurrentRow(0)
            lay.addWidget(lst)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(inner)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)


def transfer_list(colors: dict) -> QTreeView:
    rows = [
        ("Ubuntu 26.04 LTS desktop amd64.iso", "5.91 GiB", 100, "Seeding", "0 (3)", "0 (0)", "0 B/s", "Uploading", "upload"),
        ("Fedora Workstation Live 44 x86_64", "2.31 GiB", 100, "Seeding", "0 (5)", "0 (0)", "0 B/s", "StalledUploading", "stalledUP"),
        ("Debian 13.2.0 amd64 netinst", "1.41 GiB", 62, "Downloading", "12 (798)", "4 (20)", "2.1 MiB/s", "Downloading", "downloading"),
        ("Arch Linux 2026.11.01 x86_64", "1.21 GiB", 18, "Stalled", "0 (2)", "0 (0)", "0 B/s", "StalledDownloading", "stalledDL"),
        ("Blender Open Movie Collection 4K", "16.84 GiB", 100, "Seeding", "0 (33)", "0 (3)", "0 B/s", "StalledUploading", "stalledUP"),
        ("LibreOffice 26.2 offline help pack", "939.1 MiB", 0, "Queued", "0 (11)", "0 (0)", "0 B/s", "QueuedDownloading", "queued"),
        ("Project Gutenberg DVD image", "8.72 GiB", 45, "Stopped", "0 (1)", "0 (0)", "0 B/s", "StoppedDownloading", "stopped"),
        ("OpenStreetMap planet extract", "78.88 GiB", 7, "Errored", "0 (695)", "0 (1)", "0 B/s", "Error", "error"),
        ("Wikipedia offline archive (ZIM)", "3.82 GiB", 100, "Completed", "0 (6)", "0 (6)", "0 B/s", "StoppedUploading", "checked-completed"),
    ]
    headers = ["Name", "Size", "Progress", "Status", "Seeds", "Peers", "Up Speed"]
    model = QStandardItemModel(0, len(headers))
    model.setHorizontalHeaderLabels(headers)
    for name, size, prog, status, seeds, peers, speed, state, ic in rows:
        colour = QColor(colors[f"TransferList.{state}"])
        items = [QStandardItem(icon(ic), name), QStandardItem(size), QStandardItem(),
                 QStandardItem(status), QStandardItem(seeds), QStandardItem(peers), QStandardItem(speed)]
        items[2].setData(prog, Qt.UserRole)
        for i, it in enumerate(items):
            it.setForeground(colour)
            it.setEditable(False)
            if i in (1, 4, 5, 6):
                it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        model.appendRow(items)

    view = QTreeView()
    view.setModel(model)
    view.setRootIsDecorated(False)
    view.setAlternatingRowColors(True)
    view.setUniformRowHeights(True)
    view.setSelectionMode(QTreeView.ExtendedSelection)
    view.setItemDelegateForColumn(2, ProgressDelegate(view))
    view.setColumnWidth(0, 330)
    view.setColumnWidth(2, 130)
    view.setCurrentIndex(model.index(1, 0))
    return view


class PropertiesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()

        # General page
        page = QWidget()
        pv = QVBoxLayout(page)
        bar = QHBoxLayout()
        bar.addWidget(QLabel("Progress:"))
        pb = QProgressBar()
        pb.setValue(100)
        pb.setTextVisible(False)
        bar.addWidget(pb, 1)
        bar.addWidget(QLabel("100.0%"))
        pv.addLayout(bar)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        pv.addWidget(line)
        group = QGroupBox("Transfer")
        grid = QGridLayout(group)
        data = [("Time Active:", "27d 21h (seeded for 27d 21h)"), ("ETA:", "∞"), ("Connections:", "0 (100 max)"),
                ("Downloaded:", "2.04 GiB (0 B this session)"), ("Uploaded:", "1.96 GiB (0 B this session)"), ("Seeds:", "0 (3 total)"),
                ("Download Speed:", "0 B/s (1.5 MiB/s avg.)"), ("Upload Speed:", "0 B/s (874 B/s avg.)"), ("Peers:", "0 (0 total)"),
                ("Share Ratio:", "0.96"), ("Reannounce In:", "10m"), ("Last Seen Complete:", "20/10/26 2:36 PM")]
        for i, (k, v) in enumerate(data):
            key = QLabel(k)
            key.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(key, i // 3, (i % 3) * 2)
            grid.addWidget(QLabel(v), i // 3, (i % 3) * 2 + 1)
        pv.addWidget(group)
        pv.addStretch(1)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(page)
        self.stack.addWidget(scroll)

        # Trackers page
        model = QStandardItemModel(0, 6)
        model.setHorizontalHeaderLabels(["URL/Announce Endpoint", "Tier", "BT Protocol", "Status", "Peers", "Seeds"])
        for row in (["** [DHT] **", "", "N/A", "Disabled for this torrent", "N/A", "0"],
                    ["** [PeX] **", "", "N/A", "Disabled for this torrent", "N/A", "0"],
                    ["** [LSD] **", "", "N/A", "Disabled for this torrent", "N/A", "0"],
                    ["https://tracker.example.org/announce", "0", "N/A", "Working", "0", "3"]):
            model.appendRow([QStandardItem(t) for t in row])
        trackers = QTreeView()
        trackers.setModel(model)
        trackers.setAlternatingRowColors(True)
        trackers.setColumnWidth(0, 330)
        trackers.header().setSortIndicatorShown(True)
        trackers.header().setSortIndicator(0, Qt.AscendingOrder)
        self.stack.addWidget(trackers)

        self.buttons = []
        tabs = QHBoxLayout()
        for name in ("General", "Trackers", "Peers", "HTTP Sources", "Content"):
            b = QPushButton(name)
            tabs.addWidget(b)
            self.buttons.append(b)
        tabs.addStretch(1)
        speed = QPushButton("Speed")
        tabs.addWidget(speed)
        self.buttons.append(speed)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.stack)
        lay.addLayout(tabs)

    def select(self, index: int) -> None:
        for i, b in enumerate(self.buttons):
            b.setDown(i == index)
        self.stack.setCurrentIndex(index)


def main_window(colors: dict) -> tuple[QMainWindow, PropertiesWidget]:
    win = QMainWindow()
    win.setWindowTitle("qBittorrent v5.2.3")

    # Same structure as MainWindow on macOS: separators are fixed spacer
    # widgets, and the filter field, label and drop-down share one container.
    def fixed_spacer(width: int) -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        w.setMinimumWidth(width)
        return w

    def expanding_spacer() -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return w

    bar = QToolBar()
    bar.setMovable(False)
    bar.addWidget(fixed_spacer(8))
    # (icon, QToolButton text). Order and texts as in qBittorrent 5.2.3 on macOS.
    actions = (("list-add", "Open"), ("insert-link", "Add Torrent Link..."), ("list-remove", "Remove"), None,
               ("torrent-start", "Start"), ("torrent-stop", "Stop"), None,
               ("go-top", "Move to top"), ("go-up", "Move up"), ("go-down", "Move down"),
               ("go-bottom", "Move to bottom"), None,
               ("torrent-creator", "Torrent Creator"), ("configure", "Preferences"))
    for entry in actions:
        if entry is None:
            bar.addWidget(fixed_spacer(16))
        else:
            ic, text = entry
            bar.addAction(icon(ic), text).setVisible(QUEUEING or not ic.startswith("go-"))
    bar.addWidget(expanding_spacer())
    search = QLineEdit()
    search.setPlaceholderText("Filter torrents...")
    search.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    search.setFixedWidth(200)
    search.addAction(icon("edit-find"), QLineEdit.LeadingPosition)
    search.setClearButtonEnabled(True)
    column = QComboBox()
    column.addItems(["Name", "Save path"])
    filter_box = QWidget()
    filter_lay = QHBoxLayout(filter_box)
    filter_lay.setContentsMargins(0, 0, 0, 0)
    for w in (expanding_spacer(), search, QLabel("Filter by:"), column):
        filter_lay.addWidget(w)
    bar.addWidget(filter_box)
    lock = bar.addAction(icon("object-locked"), "lock")
    lock.setMenu(QMenu(win))
    bar.addWidget(fixed_spacer(8))
    win.addToolBar(bar)

    props = PropertiesWidget()
    right = QSplitter(Qt.Vertical)
    right.addWidget(transfer_list(colors))
    right.addWidget(props)
    right.setSizes([330, 300])

    split = QSplitter(Qt.Horizontal)
    split.addWidget(TransferListFiltersWidget())
    split.addWidget(right)
    split.setSizes([210, 890])

    central = QWidget()
    lay = QVBoxLayout(central)
    lay.setContentsMargins(0, 0, 6, 0)
    lay.addWidget(split)
    win.setCentralWidget(central)

    status = win.statusBar()
    box = QWidget()
    h = QHBoxLayout(box)
    h.setContentsMargins(0, 0, 4, 0)

    def sep():
        f = QFrame()
        f.setFrameShape(QFrame.VLine)
        return f

    h.addWidget(QLabel("DHT: 361 nodes"))
    h.addWidget(sep())
    for ic, text in (("connected", ""), ("slow_off", "")):
        b = QPushButton(icon(ic), text)
        b.setFlat(True)
        h.addWidget(b)
        h.addWidget(sep())
    for ic, text in (("downloading", "2.1 MiB/s (4.20 GiB)"), ("upload", "0 B/s (321.7 KiB)")):
        b = QPushButton(icon(ic), text)
        b.setFlat(True)
        h.addWidget(b)
    status.addPermanentWidget(box)

    win.resize(1180, 760)
    return win, props


def options_dialog() -> QDialog:
    dlg = QDialog()
    dlg.setWindowTitle("Options")
    tabs = QTabWidget()
    page = QWidget()
    v = QVBoxLayout(page)

    g1 = QGroupBox("Saving Management")
    f = QFormLayout(g1)
    combo = QComboBox()
    combo.addItems(["Manual", "Automatic"])
    f.addRow("Default Torrent Management Mode:", combo)
    f.addRow("Default Save Path:", QLineEdit("/Users/me/Downloads"))
    spin = QSpinBox()
    spin.setValue(500)
    spin.setSuffix(" KiB/s")
    f.addRow("Global upload limit:", spin)
    disabled = QLineEdit("disabled field")
    disabled.setEnabled(False)
    f.addRow("Proxy:", disabled)
    v.addWidget(g1)

    g2 = QGroupBox("When adding a torrent")
    g2.setCheckable(True)
    gv = QVBoxLayout(g2)
    for text, state in (("Display torrent content and some options", Qt.Checked),
                        ("Do not start the download automatically", Qt.Unchecked),
                        ("Keep incomplete torrents in a temp folder", Qt.PartiallyChecked)):
        cb = QCheckBox(text)
        cb.setTristate(True)
        cb.setCheckState(state)
        gv.addWidget(cb)
    r1, r2 = QRadioButton("Original layout"), QRadioButton("Create subfolder")
    r1.setChecked(True)
    gv.addWidget(r1)
    gv.addWidget(r2)
    v.addWidget(g2)

    tabs.addTab(page, "Downloads")
    for name in ("Connection", "Speed", "BitTorrent", "WebUI", "Advanced"):
        tabs.addTab(QWidget(), name)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
    buttons.button(QDialogButtonBox.Ok).setDefault(True)
    buttons.button(QDialogButtonBox.Apply).setEnabled(False)

    lay = QVBoxLayout(dlg)
    lay.addWidget(tabs)
    lay.addWidget(buttons)
    dlg.resize(640, 520)
    return dlg


def main() -> None:
    app = QApplication(sys.argv)
    colors = load_theme(app)
    OUT.mkdir(exist_ok=True)

    win, props = main_window(colors)
    for index, name in ((0, "general"), (1, "trackers")):
        props.select(index)
        app.processEvents()
        path = OUT / f"preview-{name}.png"
        win.grab().save(str(path))
        print(f"wrote {path.relative_to(ROOT)}")

    dlg = options_dialog()
    path = OUT / "preview-options.png"
    dlg.grab().save(str(path))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
