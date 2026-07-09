import random


SUITS = ["s", "h", "d", "c"]
RANKS = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A"
]


class Deck:

    def __init__(self):

        self.cards = []

        self.create()


    def create(self):

        self.cards = [
            rank + suit
            for rank in RANKS
            for suit in SUITS
        ]


    def shuffle(self):

        random.shuffle(
            self.cards
        )


    def deal(self):

        return self.cards.pop()