import tkinter as tk

from widgets import CardWidget, ActionButton
from deck import Deck


class PokerUI:

    def __init__(self, root):

        self.root = root
        self.deck = Deck()

        self.root.title("GTO Poker Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#075E2A")


        self.table = tk.Frame(
            root,
            bg="#075E2A"
        )

        self.table.pack(
            expand=True,
            fill="both"
        )


        tk.Label(
            self.table,
            text="GTO Poker Trainer",
            font=("Arial",24,"bold"),
            fg="white",
            bg="#075E2A"
        ).pack(pady=20)



        # Board

        self.board_frame = tk.Frame(
            self.table,
            bg="#075E2A"
        )

        self.board_frame.pack(pady=30)


        self.board_cards = []

        for i in range(5):

            card = CardWidget(
                self.board_frame,
                80,
                120
            )

            card.grid(
                row=0,
                column=i,
                padx=10
            )

            self.board_cards.append(card)



        # Hero

        tk.Label(
            self.table,
            text="Your Hand",
            font=("Arial",16),
            fg="white",
            bg="#075E2A"
        ).pack()


        self.hand_frame = tk.Frame(
            self.table,
            bg="#075E2A"
        )

        self.hand_frame.pack(pady=15)


        self.hand_cards = []

        for i in range(2):

            card = CardWidget(
                self.hand_frame,
                90,
                130
            )

            card.grid(
                row=0,
                column=i,
                padx=15
            )

            self.hand_cards.append(card)



        # Buttons

        self.action_frame = tk.Frame(
            self.table,
            bg="#075E2A"
        )

        self.action_frame.pack(pady=30)


        ActionButton(
            self.action_frame,
            "Fold"
        ).grid(row=0,column=0,padx=10)


        ActionButton(
            self.action_frame,
            "Call"
        ).grid(row=0,column=1,padx=10)


        ActionButton(
            self.action_frame,
            "Raise"
        ).grid(row=0,column=2,padx=10)


        ActionButton(
            self.action_frame,
            "Deal",
            self.deal_hand
        ).grid(row=0,column=3,padx=10)



        self.result_box = tk.Label(
            self.table,
            text="Waiting...",
            font=("Arial",18),
            fg="yellow",
            bg="#075E2A"
        )

        self.result_box.pack()



    def deal_hand(self):

        self.deck = Deck()
        self.deck.shuffle()


        hero = [
            self.deck.deal(),
            self.deck.deal()
        ]


        board = [
            self.deck.deal(),
            self.deck.deal(),
            self.deck.deal(),
            self.deck.deal(),
            self.deck.deal()
        ]


        self.update_hand(hero)
        self.update_board(board)


        self.result_box.config(
            text=f"Hero: {hero[0]} {hero[1]}"
        )



    def update_hand(self, cards):

        for widget, card in zip(
            self.hand_cards,
            cards
        ):
            widget.show_card(card)



    def update_board(self, cards):

        for widget, card in zip(
            self.board_cards,
            cards
        ):
            widget.show_card(card)