from pokerkit import Deck, StandardHighHand, calculate_equities, parse_range

equities = calculate_equities(
    (
        parse_range("AhKh"),
        parse_range("QcQs"),
    ),
    (),  # ボードなし = プリフロップ
    2,   # ホールカード2枚
    5,   # ボード5枚
    Deck.STANDARD,
    (StandardHighHand,),
    sample_count=10000,
)

print(f"AhKh: {equities[0]:.1%}")
print(f"QcQs: {equities[1]:.1%}")
