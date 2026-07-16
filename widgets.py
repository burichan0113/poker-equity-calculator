import os
import tkinter as tk

from PIL import Image, ImageTk


class CardImage:
    """カード画像を読み込み、サイズ別にキャッシュする。"""

    cache = {}

    @staticmethod
    def load(
        card: str,
        width: int,
        height: int,
    ):
        key = f"{card}_{width}_{height}"

        if key in CardImage.cache:
            return CardImage.cache[key]

        path = os.path.join(
            os.path.dirname(__file__),
            "cards",
            f"{card}.png",
        )

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"カード画像が見つかりません: {path}"
            )

        image = Image.open(path).convert("RGBA")

        image = image.resize(
            (width, height),
            Image.Resampling.LANCZOS,
        )

        photo = ImageTk.PhotoImage(image)

        CardImage.cache[key] = photo

        return photo


class CardWidget(tk.Frame):
    """
    Hero・Opponent・Boardで使うカード枠。

    左クリック:
        選択対象にする

    右クリックまたはダブルクリック:
        カードを解除する
    """

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
        clear_callback=None,
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg="white",
            relief="solid",
            borderwidth=2,
            cursor="hand2",
            highlightthickness=3,
            highlightbackground="#222222",
            highlightcolor="#222222",
        )

        self.pack_propagate(False)
        self.grid_propagate(False)

        self.card_width = width
        self.card_height = height

        self.click_callback = click_callback
        self.clear_callback = clear_callback

        self.card = None
        self.image = None

        self.label = tk.Label(
            self,
            bg="white",
            fg="gray",
            font=("Arial", 24, "bold"),
            cursor="hand2",
        )

        self.label.pack(
            expand=True,
            fill="both",
        )

        # 左クリック
        self.bind(
            "<Button-1>",
            self._on_click,
        )

        self.label.bind(
            "<Button-1>",
            self._on_click,
        )

        # 右クリック
        self.bind(
            "<Button-3>",
            self._on_clear,
        )

        self.label.bind(
            "<Button-3>",
            self._on_clear,
        )

        # ダブルクリック
        self.bind(
            "<Double-Button-1>",
            self._on_clear,
        )

        self.label.bind(
            "<Double-Button-1>",
            self._on_clear,
        )

        self.show_back()

    def _on_click(self, event=None):
        """このカード枠を選択対象にする。"""
        if self.click_callback:
            self.click_callback(self)

    def _on_clear(self, event=None):
        """このカード枠だけを解除する。"""
        if self.clear_callback:
            self.clear_callback(self)

        return "break"

    def set_active(self, active: bool):
        """選択中の枠を黄色で表示する。"""
        color = (
            "#FFD43B"
            if active
            else "#222222"
        )

        self.config(
            highlightbackground=color,
            highlightcolor=color,
        )

    def set_card(self, card: str):
        """指定されたカードを表示する。"""
        self.card = card

        try:
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

        except FileNotFoundError:
            rank = card[0]
            suit = card[1]

            symbol = self.SUIT_SYMBOLS[suit]

            color = (
                "red"
                if suit in {"h", "d"}
                else "black"
            )

            self.image = None

            self.label.config(
                image="",
                text=f"{rank}{symbol}",
                fg=color,
                bg="white",
            )

    def show_back(self):
        """カード未選択状態へ戻す。"""
        self.card = None

        try:
            self.image = CardImage.load(
                "back",
                self.card_width,
                self.card_height,
            )

            self.label.config(
                image=self.image,
                text="",
                bg="white",
            )

        except FileNotFoundError:
            self.image = None

            self.label.config(
                image="",
                text="?",
                fg="gray",
                bg="white",
            )

    def clear(self):
        """カードを解除する。"""
        self.show_back()
        self.set_active(False)


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
            font=("Arial", 13, "bold"),
            bg="#111111",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="raised",
            borderwidth=3,
            cursor="hand2",
        )