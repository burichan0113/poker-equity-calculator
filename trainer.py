import random
import tkinter as tk

from deck import Deck
from widgets import ActionButton, CardWidget


TABLE_COLOR = "#075E2A"


class PokerTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Action Trainer")
        self.root.geometry("900x700")
        self.root.configure(bg=TABLE_COLOR)

        self.deck = Deck()

        self.hero_cards = []
        self.board_cards = []

        self.build_ui()
        self.deal_new_spot()

    def build_ui(self):
        tk.Label(
            self.root,
            text="Poker Action Trainer",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Board",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        ).pack()

        board_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )
        board_frame.pack(pady=10)

        for _ in range(5):
            widget = CardWidget(
                board_frame,
                width=80,
                height=115,
            )
            widget.pack(
                side="left",
                padx=6,
            )
            self.board_cards.append(widget)

        tk.Label(
            self.root,
            text="Hero",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        ).pack(pady=(20, 0))

        hero_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )
        hero_frame.pack(pady=10)

        for _ in range(2):
            widget = CardWidget(
                hero_frame,
                width=90,
                height=130,
            )
            widget.pack(
                side="left",
                padx=8,
            )
            self.hero_cards.append(widget)

        self.spot_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 16, "bold"),
            fg="yellow",
            bg=TABLE_COLOR,
        )
        self.spot_label.pack(pady=20)

        action_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )
        action_frame.pack(pady=10)

        ActionButton(
            action_frame,
            "Fold",
            lambda: self.choose_action("Fold"),
        ).pack(side="left", padx=8)

        ActionButton(
            action_frame,
            "Call",
            lambda: self.choose_action("Call"),
        ).pack(side="left", padx=8)

        ActionButton(
            action_frame,
            "Raise",
            lambda: self.choose_action("Raise"),
        ).pack(side="left", padx=8)

        ActionButton(
            self.root,
            "Next Hand",
            self.deal_new_spot,
        ).pack(pady=20)

        self.result_label = tk.Label(
            self.root,
            text="Choose an action",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        )
        self.result_label.pack()

    def deal_new_spot(self):
        self.deck = Deck()
        self.deck.shuffle()

        hero = [
            self.deck.deal(),
            self.deck.deal(),
        ]

        board = [
            self.deck.deal(),
            self.deck.deal(),
            self.deck.deal(),
        ]

        for widget, card in zip(
            self.hero_cards,
            hero,
        ):
            widget.set_card(card)

        for index, widget in enumerate(
            self.board_cards
        ):
            if index < 3:
                widget.set_card(board[index])
            else:
                widget.clear()

        pot = round(
            random.uniform(4.0, 12.0),
            1,
        )

        bet = round(
            random.uniform(1.5, pot * 0.75),
            1,
        )

        self.current_pot = pot
        self.current_bet = bet
        self.current_hero = hero
        self.current_board = board

        self.spot_label.config(
            text=(
                f"Pot: {pot}bb    "
                f"Opponent bets: {bet}bb"
            )
        )

        self.result_label.config(
            text="Choose an action",
            fg="white",
        )

    def choose_action(self, action):
        self.result_label.config(
            text=f"You chose: {action}",
            fg="yellow",
        )


if __name__ == "__main__":
    root = tk.Tk()
    PokerTrainer(root)
    root.mainloop()