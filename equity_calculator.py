from pokerkit import Deck, StandardHighHand, calculate_equities, parse_range
from cards import parse_cards, normalize_cards_text

VALID_BOARD_SIZES = {0, 3, 4, 5}
SAMPLE_COUNT = 10000


def validate_hand(cards, label, count):
    if len(cards) != count:
        raise ValueError(f"{label}は{count}枚必要です")


def validate_board(cards):
    if len(cards) not in VALID_BOARD_SIZES:
        raise ValueError("Boardは0,3,4,5枚のみ対応")


def validate_no_duplicates(*groups):
    cards = sum(groups, [])
    if len(cards) != len(set(cards)):
        raise ValueError("カードが重複しています")


def cards_to_string(cards):
    return "".join(
        card.rank.value + card.suit.value
        for card in cards
    )


def calculate_equity(hero, opponent, board):
    result = calculate_equities(
        (
            parse_range(cards_to_string(hero)),
            parse_range(cards_to_string(opponent))
        ),
        tuple(board),
        2,
        5,
        Deck.STANDARD,
        (StandardHighHand,),
        sample_count=SAMPLE_COUNT
    )

    return result[0], result[1]


def main():
    print("Texas Hold'em Equity Calculator")

    try:
        hero_text = input("Hero: ").strip()
        opp_text = input("Opponent: ").strip()
        board_text = input("Board: ").strip()

        hero = parse_cards(hero_text, "Hero")
        opponent = parse_cards(opp_text, "Opponent")
        board = parse_cards(board_text, "Board")

        validate_hand(hero, "Hero", 2)
        validate_hand(opponent, "Opponent", 2)
        validate_board(board)
        validate_no_duplicates(hero, opponent, board)

        hero_eq, opp_eq = calculate_equity(
            hero,
            opponent,
            board
        )

        print()
        print("-" * 30)
        print(f"Hero     : {normalize_cards_text(hero_text)}")
        print(f"Opponent : {normalize_cards_text(opp_text)}")
        print(f"Board    : {normalize_cards_text(board_text)}")
        print()
        print(f"Hero Equity     : {hero_eq:.2%}")
        print(f"Opponent Equity : {opp_eq:.2%}")
        print("-" * 30)

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()