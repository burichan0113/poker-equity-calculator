"""
Texas Hold'em エクイティ計算機

2人の特定の手札とボード（任意）から
Monte Carlo シミュレーションで勝率を計算します。
"""

from pokerkit import (
    Deck,
    StandardHighHand,
    calculate_equities,
    parse_range,
)

from cards import (
    parse_cards,
    normalize_cards_text,
)

# ボードとして許可する枚数（0=プリフロップ, 3=フロップ, 4=ターン, 5=リバー）
VALID_BOARD_SIZES = {0, 3, 4, 5}

# シミュレーション回数（多いほど精度が上がるが、時間もかかる）
SAMPLE_COUNT = 10000


def read_input(prompt: str) -> str:
    """ユーザーから1行入力を受け取り、前後の空白を除去して返す。"""
    return input(prompt).strip()



def validate_hand(cards: list, label: str, required_count: int) -> None:
    """手札が指定枚数（通常2枚）であることを確認する。"""
    actual_count = len(cards)
    if actual_count != required_count:
        raise ValueError(
            f"{label} は {required_count} 枚である必要があります（入力: {actual_count} 枚）"
        )


def validate_board(cards: list) -> None:
    """ボードの枚数が 0, 3, 4, 5 のいずれかであることを確認する。"""
    count = len(cards)
    if count not in VALID_BOARD_SIZES:
        raise ValueError(
            f"Board は 0, 3, 4, 5 枚である必要があります（入力: {count} 枚）"
        )


def validate_no_duplicates(
    hero_cards: list,
    opponent_cards: list,
    board_cards: list,
) -> None:
    """Hero / Opponent / Board 全体で同じカードが重複していないか確認する。"""
    all_cards = hero_cards + opponent_cards + board_cards

    if len(all_cards) != len(set(all_cards)):
        raise ValueError("同じカードが重複しています。各カードは1枚しか使えません。")


def cards_to_range_string(cards: list) -> str:
    """
    2枚のホールカードを parse_range 用の文字列に変換する。
    例: [Ah, Kh] → "AhKh"
    """
    return "".join(str(card) for card in cards)


def calculate_equity(
    hero_cards: list,
    opponent_cards: list,
    board_cards: list,
) -> tuple[float, float]:
    """
    Monte Carlo シミュレーションで Hero と Opponent のエクイティを計算する。

    戻り値: (hero_equity, opponent_equity)  ※ 0.0〜1.0 の小数
    """
    hero_range = parse_range(cards_to_range_string(hero_cards))
    opponent_range = parse_range(cards_to_range_string(opponent_cards))
    board = tuple(board_cards)

    equities = calculate_equities(
        (hero_range, opponent_range),
        board,
        2,  # ホールカード2枚
        5,  # ボード最大5枚
        Deck.STANDARD,
        (StandardHighHand,),
        sample_count=SAMPLE_COUNT,
    )

    return equities[0], equities[1]


def display_results(
    hero_text: str,
    opponent_text: str,
    board_text: str,
    hero_equity: float,
    opponent_equity: float,
) -> None:
    """計算結果を指定フォーマットで表示する。"""
    print("------------------")
    print(f"Hero: {hero_text}")
    print(f"Opponent: {opponent_text}")
    print(f"Board: {board_text}")
    print()
    print(f"Hero Equity: {hero_equity:.1%}")
    print(f"Opponent Equity: {opponent_equity:.1%}")
    print("------------------")


def main() -> None:
    """プログラムのメイン処理。"""
    print("Texas Hold'em エクイティ計算機")
    print("カード表記: ランク(A,2-9,T,J,Q,K) + スート(h,d,c,s)")
    print("例: Ah = ハートのA, Td = ダイヤの10")
    print()

    try:
        hero_text = read_input("Hero: ")
        opponent_text = read_input("Opponent: ")
        board_text = read_input("Board: ")

        hero_cards = parse_cards(hero_text, "Hero")
        opponent_cards = parse_cards(opponent_text, "Opponent")
        board_cards = parse_cards(board_text, "Board")

        validate_hand(hero_cards, "Hero", required_count=2)
        validate_hand(opponent_cards, "Opponent", required_count=2)
        validate_board(board_cards)
        validate_no_duplicates(hero_cards, opponent_cards, board_cards)

        hero_equity, opponent_equity = calculate_equity(
            hero_cards,
            opponent_cards,
            board_cards,
        )

        display_results(
            normalize_cards_text(hero_text),
            normalize_cards_text(opponent_text),
            normalize_cards_text(board_text),
            hero_equity,
            villain_equity,
        )

    except ValueError as error:
        print(f"エラー: {error}")


if __name__ == "__main__":
    main()
