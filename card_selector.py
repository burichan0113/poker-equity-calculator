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

    def __init__(
        self,
        parent,
        callback,
        used_cards=None,
    ):
        super().__init__(parent)

        self.callback = callback
        self.used_cards = set(used_cards or [])
        self.buttons = {}

        self.title("Select Card")
        self.resizable(False, False)
        self.transient(parent)

        # クリック中でも親画面を操作できるように
        # grab_set() は使わない

        for row, rank in enumerate(RANKS):
            for column, (suit, symbol) in enumerate(SUITS.items()):
                card = rank + suit

                button = tk.Button(
                    self,
                    text=rank + symbol,
                    width=6,
                    font=("Arial", 12, "bold"),
                    command=lambda selected_card=card: self.select(
                        selected_card
                    ),
                )

                button.grid(
                    row=row,
                    column=column,
                    padx=4,
                    pady=4,
                )

                self.buttons[card] = button

        self.update_used_cards(self.used_cards)

    def select(self, card):
        if card in self.used_cards:
            return

        self.callback(card)

    def update_used_cards(self, used_cards):
        self.used_cards = set(used_cards)

        for card, button in self.buttons.items():
            if card in self.used_cards:
                button.config(
                    state="disabled",
                    bg="#dddddd",
                )
            else:
                button.config(
                    state="normal",
                    bg="SystemButtonFace",
                )