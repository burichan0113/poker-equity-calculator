import equity_calculator as ec


def main():
    print("=" * 40)
    print("Texas Hold'em Equity Calculator")
    print("=" * 40)

    hero_text = input("Hero (例: AhKh): ").strip()
    opponent_text = input("Opponent (例: QcQs): ").strip()
    board_text = input("Board (空欄、または Ad7c2s): ").strip()

    try:
        hero_cards = ec.parse_cards(hero_text, "Hero")
        opponent_cards = ec.parse_cards(opponent_text, "Opponent")
        board_cards = ec.parse_cards(board_text, "Board")

        ec.validate_hand(hero_cards, "Hero", 2)
        ec.validate_hand(opponent_cards, "Opponent", 2)
        ec.validate_board(board_cards)
        ec.validate_no_duplicates(
            hero_cards,
            opponent_cards,
            board_cards,
        )

        hero_equity, opponent_equity = ec.calculate_equity(
            hero_cards,
            opponent_cards,
            board_cards,
        )

        print()
        print("=" * 40)
        print(f"Hero Equity      : {hero_equity:.2%}")
        print(f"Opponent Equity  : {opponent_equity:.2%}")
        print("=" * 40)

    except ValueError as e:
        print()
        print("Error:", e)


if __name__ == "__main__":
    main()