"""Generate src/background.png: a dark navy canvas with blurred colour blobs.

qBittorrent cannot blur the real desktop behind its window, so the "glass"
look is faked by painting this image as the window background.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "background.png"

W, H = 1280, 800
BASE = (13, 16, 38)

# (centre x, centre y, radius x, radius y, colour) in fractions of the canvas
BLOBS = [
    (0.10, 0.20, 0.34, 0.40, (30, 64, 175)),    # blue, top left
    (0.50, 0.00, 0.36, 0.30, (91, 33, 182)),    # violet, top centre
    (0.92, 0.42, 0.24, 0.36, (232, 82, 62)),    # coral, right
    (0.72, 0.62, 0.22, 0.28, (168, 48, 120)),   # magenta, right centre
    (0.08, 0.95, 0.30, 0.34, (14, 140, 200)),   # cyan, bottom left
    (0.48, 0.85, 0.30, 0.28, (28, 110, 160)),   # teal, bottom centre
    (0.00, 0.60, 0.16, 0.24, (200, 70, 90)),    # warm accent, left edge
]


def main() -> None:
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    for cx, cy, rx, ry, colour in BLOBS:
        box = [
            (cx - rx) * W, (cy - ry) * H,
            (cx + rx) * W, (cy + ry) * H,
        ]
        draw.ellipse(box, fill=colour)
    img = img.filter(ImageFilter.GaussianBlur(120))

    # Dark veil so near-white text keeps its contrast everywhere.
    veil = Image.new("RGB", (W, H), (10, 13, 30))
    img = Image.blend(img, veil, 0.42)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
