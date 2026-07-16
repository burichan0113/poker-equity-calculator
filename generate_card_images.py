from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT_DIR = Path(__file__).parent / "cards"

CARD_WIDTH = 240
CARD_HEIGHT = 336

RANKS = [
    "A", "K", "Q", "J", "T",
    "9", "8", "7", "6",
    "5", "4", "3", "2",
]

SUITS = {
    "s": ("♠", "black"),
    "h": ("♥", "#d9272e"),
    "d": ("♦", "#d9272e"),
    "c": ("♣", "black"),
}


def load_font(size: int, bold: bool = False):
    """
    Windowsで利用可能なフォントを探す。
    見つからない場合はPillowの標準フォントを使う。
    """
    candidates = []

    if bold:
        candidates.extend([
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
        ])
    else:
        candidates.extend([
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ])

    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


RANK_FONT = load_font(55, bold=True)
SUIT_FONT = load_font(54, bold=True)
CENTER_FONT = load_font(125, bold=True)
BACK_FONT = load_font(38, bold=True)


def rounded_rectangle(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill,
    outline,
    width: int,
):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width,
    )


def create_card(rank: str, suit_code: str):
    suit_symbol, color = SUITS[suit_code]

    image = Image.new(
        "RGBA",
        (CARD_WIDTH, CARD_HEIGHT),
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(image)

    rounded_rectangle(
        draw,
        (4, 4, CARD_WIDTH - 5, CARD_HEIGHT - 5),
        radius=18,
        fill="white",
        outline="#222222",
        width=5,
    )

    # 左上
    draw.text(
        (22, 14),
        rank,
        font=RANK_FONT,
        fill=color,
    )

    draw.text(
        (22, 69),
        suit_symbol,
        font=SUIT_FONT,
        fill=color,
    )

    # 中央の大きなスート
    center_box = draw.textbbox(
        (0, 0),
        suit_symbol,
        font=CENTER_FONT,
    )

    center_width = center_box[2] - center_box[0]
    center_height = center_box[3] - center_box[1]

    draw.text(
        (
            (CARD_WIDTH - center_width) / 2,
            (CARD_HEIGHT - center_height) / 2 - 12,
        ),
        suit_symbol,
        font=CENTER_FONT,
        fill=color,
    )

    # 右下（180度回転）
    corner = Image.new(
        "RGBA",
        (90, 115),
        (0, 0, 0, 0),
    )

    corner_draw = ImageDraw.Draw(corner)

    corner_draw.text(
        (7, 0),
        rank,
        font=RANK_FONT,
        fill=color,
    )

    corner_draw.text(
        (7, 55),
        suit_symbol,
        font=SUIT_FONT,
        fill=color,
    )

    corner = corner.rotate(
        180,
        expand=False,
    )

    image.alpha_composite(
        corner,
        (
            CARD_WIDTH - 102,
            CARD_HEIGHT - 126,
        ),
    )

    output_path = OUTPUT_DIR / f"{rank}{suit_code}.png"
    image.save(output_path)


def create_back():
    image = Image.new(
        "RGBA",
        (CARD_WIDTH, CARD_HEIGHT),
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(image)

    rounded_rectangle(
        draw,
        (4, 4, CARD_WIDTH - 5, CARD_HEIGHT - 5),
        radius=18,
        fill="#f7f7f7",
        outline="#222222",
        width=5,
    )

    rounded_rectangle(
        draw,
        (17, 17, CARD_WIDTH - 18, CARD_HEIGHT - 18),
        radius=13,
        fill="#173b73",
        outline="#ffffff",
        width=4,
    )

    # シンプルなダイヤ柄
    spacing = 24

    for x in range(-CARD_HEIGHT, CARD_WIDTH + CARD_HEIGHT, spacing):
        draw.line(
            (x, 20, x + CARD_HEIGHT, CARD_HEIGHT - 20),
            fill="#4f79b7",
            width=3,
        )

        draw.line(
            (x, CARD_HEIGHT - 20, x + CARD_HEIGHT, 20),
            fill="#4f79b7",
            width=3,
        )

    text = "POKER"

    text_box = draw.textbbox(
        (0, 0),
        text,
        font=BACK_FONT,
    )

    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]

    rounded_rectangle(
        draw,
        (
            45,
            CARD_HEIGHT // 2 - 37,
            CARD_WIDTH - 45,
            CARD_HEIGHT // 2 + 37,
        ),
        radius=14,
        fill="#102b55",
        outline="white",
        width=3,
    )

    draw.text(
        (
            (CARD_WIDTH - text_width) / 2,
            (CARD_HEIGHT - text_height) / 2 - 6,
        ),
        text,
        font=BACK_FONT,
        fill="white",
    )

    image.save(OUTPUT_DIR / "back.png")


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for rank in RANKS:
        for suit_code in SUITS:
            create_card(
                rank,
                suit_code,
            )

    create_back()

    print(f"カード画像を作成しました: {OUTPUT_DIR}")
    print("52枚 + back.png")


if __name__ == "__main__":
    main()