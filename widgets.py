import os
import tkinter as tk
from PIL import Image, ImageTk

class CardWidget(tk.Frame):
    """固定サイズで、クリックしてカードを選択できるカード枠。"""

    SUIT_SYMBOLS = {
        "s": "♠",
        "h": "♥",
        "d": "♦",
        "c": "♣",
    }

    def __init__(
        self,
        parent,
        width=90,
        height=130,
        click_callback=None,
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg="white",
            relief="solid",
            borderwidth=2,
            cursor="hand2",
        )

        # Frameを中身に合わせて縮ませず、指定サイズを維持する
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.card_width = width
        self.card_height = height
        self.click_callback = click_callback

        self.card = None
        self.image = None

        self.label = tk.Label(
            self,
            text="?",
            bg="white",
            fg="gray",
            font=("Arial", 24, "bold"),
            cursor="hand2",
        )

        self.label.pack(
            expand=True,
            fill="both",
        )

        # Frameと中のLabel、どちらを押しても反応させる
        self.bind("<Button-1>", self._on_click)
        self.label.bind("<Button-1>", self._on_click)

    def _on_click(self, event=None):
        if self.click_callback:
            self.click_callback(self)

    def set_card(self, card: str):
        """画像があれば画像、なければA♠のような文字で表示する。"""
        self.card = card

        image_path = os.path.join(
            os.path.dirname(__file__),
            "cards",
            f"{card}.png",
        )

        if os.path.exists(image_path):
            self.image = CardImage.load(
                card,
                self.card_width,
                self.card_height,
            )

            self.label.config(
                image=self.image,
                text="",
                bg="white",
            )

        else:
            rank = card[0]
            suit = card[1]
            symbol = self.SUIT_SYMBOLS[suit]

            text_color = (
                "red"
                if suit in {"h", "d"}
                else "black"
            )

            self.image = None

            self.label.config(
                image="",
                text=f"{rank}{symbol}",
                fg=text_color,
                bg="white",
            )

    def show_back(self):
        """カード未選択状態に戻す。"""
        self.card = None
        self.image = None

        self.label.config(
            image="",
            text="?",
            fg="gray",
            bg="white",
        )

    def clear(self):
        self.show_back()

class ActionButton(tk.Button):
    """共通デザインの操作ボタン。"""

    def __init__(
        self,
        parent,
        text,
        command=None,
    ):
        super().__init__(
            parent,
            text=text,
            command=command,
            width=18,
            height=2,
            font=("Arial", 14, "bold"),
            bg="#111111",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="raised",
            borderwidth=3,
            cursor="hand2",
        )