import tkinter as tk

from widgets import CardImage


RANKS = [
    "A", "K", "Q", "J", "T",
    "9", "8", "7", "6",
    "5", "4", "3", "2",
]

SUITS = ["s", "h", "d", "c"]


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
        self.images = {}

        self.title("Select Card")
        self.resizable(False, False)
        self.transient(parent)

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close,
        )

        for row, rank in enumerate(RANKS):
            for column, suit in enumerate(SUITS):
                card = rank + suit

                image = CardImage.load(
                    card,
                    48,
                    68,
                )

                self.images[card] = image

                button = tk.Button(
                    self,
                    image=image,
                    width=52,
                    height=68,
                    relief="raised",
                    borderwidth=2,
                    cursor="hand2",
                    command=lambda selected_card=card: self.select(
                        selected_card
                    ),
                )

                button.grid(
                    row=row,
                    column=column,
                    padx=3,
                    pady=3,
                )

                self.buttons[card] = button

        self.update_used_cards(
            self.used_cards
        )

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
                    relief="sunken",
                )
            else:
                button.config(
                    state="normal",
                    relief="raised",
                )

    def close(self):
        self.destroy()