from pokerkit import Card

def normalize_cards_text(cards_text: str) -> str:
    """
    カード文字列を正規化する。
    例: "Ah Kh" → "AhKh"
    """
    return cards_text.replace(" ", "")


def parse_cards(cards_text: str, label: str) -> list:
    """
    カード文字列を Card オブジェクトのリストに変換する。
    """
    normalized = normalize_cards_text(cards_text)

    if not normalized:
        return []

    try:
        return list(Card.parse(normalized))
    except ValueError as error:
        raise ValueError(f"{label} に無効なカードがあります: {error}") from error