import tkinter as tk

RANKS = [
    "A", "K", "Q", "J", "T",
    "9", "8", "7", "6",
    "5", "4", "3", "2",
]

SUITS = {
    "s": "♠",
    "h": "♥",
    "d": "♦",
    "c": "♣",
}


class CardSelector(tk.Toplevel):

    def __init__(self, parent, callback):

        super().__init__(parent)

        self.callback = callback

        self.title("Select Card")

        self.resizable(False, False)

        for row, rank in enumerate(RANKS):

            for col, (suit, symbol) in enumerate(SUITS.items()):

                card = rank + suit

                tk.Button(
                    self,
                    text=rank + symbol,
                    width=6,
                    command=lambda c=card: self.select(c),
                ).grid(row=row, column=col, padx=3, pady=3)

    def select(self, card):

        self.callback(card)

        self.destroy()