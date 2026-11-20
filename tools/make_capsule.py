"""Generate the images used by the toolbar and progress bar rules in stylesheet.qss.

search-cap.png (+ @2x): background of the filter container in the toolbar.
That container holds the filter field, the "Filter by:" label and the column
drop-down. The image paints, from left to right:
  - the round left end and the body of the right toolbar capsule
  - the right part of the inner search capsule (the line edit paints the
    left part and hides the seam)
It is anchored to the right edge of the container, so its width must match
the widths fixed in the `QToolBar > QWidget > ...` rules.

progress-chunk.png: fill of the progress bars.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
UI = ROOT / "src" / "ui"
SUPERSAMPLE = 4

# Right capsule, logical px. Layout inside the container, from the right edge:
# 6 margin, 100 drop-down, 8 gap, 65 label, 10 gap, 192 line edit, then
# 14px to the capsule end.
WIDTH, HEIGHT = 395, 34
CAPSULE_FILL = (30, 30, 36, 199)     # rgba(30,30,36,0.78), as the tool buttons
PILL_INSET = 3                       # search capsule: 28px high inside 34px
PILL_LEFT = 120                      # anywhere under the line edit
PILL_RIGHT_GAP = 2
PILL_FILL = (20, 21, 27, 255)        # #14151b, as the line edit
PILL_BORDER = (58, 60, 70, 255)      # #3a3c46, as the line edit


def render(scale: int) -> Image.Image:
    s = scale * SUPERSAMPLE
    w, h = WIDTH * s, HEIGHT * s
    clear = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # Outer capsule: round on the left, runs off the canvas on the right.
    outer = Image.new("L", (w, h), 0)
    ImageDraw.Draw(outer).rounded_rectangle([0, 0, w + h, h - 1], radius=h // 2, fill=255)
    img = clear.copy()
    img.paste(Image.new("RGBA", (w, h), CAPSULE_FILL), (0, 0), outer)

    # Search capsule: opaque, drawn over the body.
    x0, x1 = PILL_LEFT * s, (WIDTH - PILL_RIGHT_GAP) * s - 1
    y0, y1 = PILL_INSET * s, (HEIGHT - PILL_INSET) * s - 1
    r = (y1 - y0 + 1) // 2
    pill = Image.new("L", (w, h), 0)
    ImageDraw.Draw(pill).rounded_rectangle([x0, y0, x1, y1], radius=r, fill=255)
    pill_in = Image.new("L", (w, h), 0)
    ImageDraw.Draw(pill_in).rounded_rectangle([x0 + s, y0 + s, x1 - s, y1 - s], radius=r - s, fill=255)
    img.paste(Image.new("RGBA", (w, h), PILL_BORDER), (0, 0), pill)
    img.paste(Image.new("RGBA", (w, h), PILL_FILL), (0, 0), pill_in)
    return img.resize((WIDTH * scale, HEIGHT * scale), Image.LANCZOS)


# Progress bar fill: a short capsule in one flat colour, used as a
# border-image. The ends are half-discs; the middle is tiled, not stretched,
# because Qt paints a stretched middle mirrored when the fill is narrower
# than the two ends, and skips a tiled one.
CHUNK_R = 7                      # logical px; fill height = 2 * CHUNK_R
CHUNK_MIDDLE = 8
CHUNK_FILL = (82, 142, 216, 255)


def render_chunk(scale: int) -> Image.Image:
    s = scale * SUPERSAMPLE
    r = CHUNK_R * s
    w, h = (2 * CHUNK_R + CHUNK_MIDDLE) * s, 2 * r
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.paste(Image.new("RGBA", (w, h), CHUNK_FILL), (0, 0), mask)
    return img.resize((w // SUPERSAMPLE, h // SUPERSAMPLE), Image.LANCZOS)


# Hover / pressed highlight of a tool button: a disc on a transparent
# 34x34 canvas (the button size), so it can be centred or anchored left.
DISC_CANVAS, DISC_SIZE = 34, 26
HOVER = (255, 255, 255, 36)
PRESSED = (255, 255, 255, 64)


def render_disc(scale: int, colour: tuple) -> Image.Image:
    s = scale * SUPERSAMPLE
    n, d = DISC_CANVAS * s, DISC_SIZE * s
    o = (n - d) // 2
    mask = Image.new("L", (n, n), 0)
    ImageDraw.Draw(mask).ellipse([o, o, o + d - 1, o + d - 1], fill=255)
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    img.paste(Image.new("RGBA", (n, n), colour), (0, 0), mask)
    return img.resize((DISC_CANVAS * scale, DISC_CANVAS * scale), Image.LANCZOS)


def main() -> None:
    UI.mkdir(parents=True, exist_ok=True)
    render(1).save(UI / "search-cap.png")
    render(2).save(UI / "search-cap@2x.png")
    for name, colour in (("hover-disc", HOVER), ("pressed-disc", PRESSED)):
        render_disc(1, colour).save(UI / f"{name}.png")
        render_disc(2, colour).save(UI / f"{name}@2x.png")
    # One 2x image, no @2x pair: border-image cuts are in image pixels, so a
    # pair would need different cut values per screen.
    render_chunk(2).save(UI / "progress-chunk.png")
    print("wrote capsule images (search, progress, discs)")


if __name__ == "__main__":
    main()
