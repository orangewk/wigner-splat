"""Generate the repository's GitHub social-preview card.

The card is intentionally assembled from repository-local assets so it can be
regenerated without a network connection or an image-generation service.

Run from the repository root with::

    python docs/assets/generate_social_preview.py
"""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1280
HEIGHT = 640
ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = Path(__file__).resolve().parent
SOURCE_FIGURE = ROOT / "experiments" / "14_gkp_rank" / "gkp_rank_marginals.png"
OUTPUT = ASSET_DIR / "social-preview.png"

NAVY = (10, 19, 42)
NAVY_LIGHT = (18, 38, 64)
WHITE = (247, 249, 252)
MUTED = (169, 186, 204)
ORANGE = (246, 145, 72)
TEAL = (73, 202, 190)
CARD = (247, 249, 252)
CARD_TEXT = (18, 31, 52)


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a common sans-serif font, with a Pillow fallback for CI."""

    windows_fonts = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    candidates = (
        [windows_fonts / "segoeuib.ttf", windows_fonts / "arialbd.ttf"]
        if bold
        else [windows_fonts / "segoeui.ttf", windows_fonts / "arial.ttf"]
    )
    candidates += [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        if bold
        else Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def _rounded_shadow(base: Image.Image, box: tuple[int, int, int, int]) -> None:
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(box, radius=24, fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    base.alpha_composite(shadow, (0, 12))


def _fit_figure(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_width, target_height = size
    figure = source.convert("RGB")
    figure.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, CARD)
    offset = ((target_width - figure.width) // 2, (target_height - figure.height) // 2)
    canvas.paste(figure, offset)
    return canvas


def build_card() -> Image.Image:
    if not SOURCE_FIGURE.exists():
        raise FileNotFoundError(f"Missing source figure: {SOURCE_FIGURE}")

    card = Image.new("RGBA", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(card)

    # A restrained vertical gradient gives the dark background some depth while
    # keeping white text and the scientific figure legible in link previews.
    for y in range(HEIGHT):
        fraction = y / (HEIGHT - 1)
        color = tuple(
            int(NAVY[channel] * (1 - fraction) + NAVY_LIGHT[channel] * fraction)
            for channel in range(3)
        )
        draw.line((0, y, WIDTH, y), fill=color)

    # Decorative glow and a small phase-space-inspired dotted motif.
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((720, -170, 1320, 380), fill=(*TEAL, 34))
    glow_draw.ellipse((-170, 470, 380, 850), fill=(*ORANGE, 22))
    card.alpha_composite(glow.filter(ImageFilter.GaussianBlur(80)))
    draw = ImageDraw.Draw(card)
    for x, y, radius, color in (
        (580, 82, 4, TEAL),
        (601, 102, 3, ORANGE),
        (579, 125, 2, MUTED),
        (603, 142, 4, TEAL),
    ):
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    # Left-hand message, kept inside GitHub's recommended safe area.
    draw.rounded_rectangle((72, 74, 210, 80), radius=3, fill=ORANGE)
    draw.text(
        (72, 96),
        "REPRODUCIBLE RESEARCH PROTOTYPE",
        font=_font(16, bold=True),
        fill=TEAL,
        spacing=2,
    )
    draw.text((72, 130), "wigner-splat", font=_font(54, bold=True), fill=WHITE)
    draw.multiline_text(
        (72, 214),
        "Gaussian splatting\nmeets quantum optics",
        font=_font(43, bold=True),
        fill=WHITE,
        spacing=2,
    )
    draw.multiline_text(
        (72, 344),
        "Continuous-variable\nquantum-state tomography",
        font=_font(25),
        fill=MUTED,
        spacing=5,
    )
    draw.text(
        (72, 438),
        "measured data  •  physical models  •  honest scope limits",
        font=_font(15),
        fill=(196, 207, 220),
    )

    doi_box = (72, 515, 481, 563)
    draw.rounded_rectangle(doi_box, radius=12, fill=(22, 44, 68), outline=ORANGE, width=2)
    draw.text((91, 529), "DOI", font=_font(16, bold=True), fill=ORANGE)
    draw.text(
        (143, 527),
        "10.5281/zenodo.21387212",
        font=_font(19, bold=True),
        fill=WHITE,
    )

    # Right-hand figure card. The source is fit rather than cropped so both
    # measured marginals and reconstructions remain visible.
    figure_box = (626, 76, 1208, 566)
    _rounded_shadow(card, figure_box)
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle(figure_box, radius=24, fill=CARD)
    draw.rounded_rectangle((626, 76, 1208, 86), radius=5, fill=TEAL)

    figure = _fit_figure(Image.open(SOURCE_FIGURE), (540, 252))
    card.paste(figure, (647, 121))
    draw = ImageDraw.Draw(card)
    draw.text((647, 397), "MEASURED GKP MARGINALS", font=_font(17, bold=True), fill=CARD_TEXT)
    draw.text(
        (647, 425),
        "Physical-model reconstructions from public homodyne data",
        font=_font(16),
        fill=(67, 84, 105),
    )
    draw.rounded_rectangle((647, 475, 840, 519), radius=10, fill=(226, 242, 241))
    draw.text((665, 488), "GKP  /  EXPERIMENT 14", font=_font(14, bold=True), fill=(26, 102, 98))
    draw.text((1036, 490), "REAL DATA", font=_font(14, bold=True), fill=ORANGE)

    return card.convert("RGB")


def main() -> None:
    image = build_card()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)
    print(f"Wrote {OUTPUT} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
