"""Build dist/glass.qbtheme from src/.

Steps: regenerate icons and background, validate config.json and icon
coverage against the ID lists taken from qBittorrent 5.2.3, then pack
everything with pyside6-rcc.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
BUILD = ROOT / "build"
DIST = ROOT / "dist"
OUT = DIST / "glass.qbtheme"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_background  # noqa: E402
import make_capsule  # noqa: E402
import make_icons  # noqa: E402


def read_ids(name: str) -> set[str]:
    return set((ROOT / "tools" / name).read_text().split())


def validate_config() -> None:
    config = json.loads((SRC / "config.json").read_text())
    known = read_ids("color_ids.txt")
    unknown = []
    for section in ("colors", "colors.dark"):
        unknown += [k for k in config.get(section, {}) if k not in known]
    if unknown:
        sys.exit(f"config.json has unknown colour IDs: {', '.join(sorted(unknown))}")


def report_icons() -> None:
    wanted = read_ids("icon_ids.txt")
    have = {f.stem for f in (SRC / "icons").glob("*.svg")}
    extra = have - wanted
    if extra:
        sys.exit(f"icons with no matching qBittorrent ID: {', '.join(sorted(extra))}")
    missing = wanted - have - make_icons.KEEP_STOCK
    if missing:
        print(f"note: {len(missing)} icon IDs fall back to stock: {', '.join(sorted(missing))}")


def find_rcc() -> str:
    local = Path(sys.executable).parent / "pyside6-rcc"
    rcc = str(local) if local.exists() else shutil.which("pyside6-rcc") or shutil.which("rcc")
    if not rcc:
        sys.exit("pyside6-rcc not found. Run: .venv/bin/pip install PySide6")
    return rcc


def main() -> None:
    make_icons.main()
    make_capsule.main()
    if "--background" in sys.argv or not (SRC / "background.png").exists():
        make_background.main()
    validate_config()
    report_icons()

    files = sorted(f for f in SRC.rglob("*") if f.is_file() and f.name != ".DS_Store")
    BUILD.mkdir(exist_ok=True)
    DIST.mkdir(exist_ok=True)
    qrc = BUILD / "glass.qrc"
    entries = "\n".join(
        f'    <file alias="{escape(f.relative_to(SRC).as_posix())}">{escape(str(f))}</file>'
        for f in files
    )
    qrc.write_text(f'<RCC>\n  <qresource prefix="/">\n{entries}\n  </qresource>\n</RCC>\n')

    subprocess.run([find_rcc(), "--binary", "-o", str(OUT), str(qrc)], check=True)
    print(f"built {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KiB, {len(files)} files)")


if __name__ == "__main__":
    main()
