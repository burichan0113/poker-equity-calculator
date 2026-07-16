import tkinter as tk

import equity_calculator as ec

from widgets import (
    ActionButton,
    CardImage,
    CardWidget,
)


TABLE_COLOR = "#075E2A"
PANEL_COLOR = "#064D25"

RANKS = [
    "A", "K", "Q", "J", "T",
    "9", "8", "7", "6",
    "5", "4", "3", "2",
]

SUITS = [
    ("s", "♠"),
    ("h", "♥"),
    ("d", "♦"),
    ("c", "♣"),
]


class PokerUI:

    def __init__(self, root):
        self.root = root

        self.root.title(
            "Poker Equity Calculator"
        )

        self.root.geometry(
            "1180x950"
        )

        self.root.minsize(
            1050,
            850,
        )

        self.root.configure(
            bg=TABLE_COLOR
        )

        self.board_cards = []
        self.hero_cards = []
        self.opponent_cards = []

        self.palette_buttons = {}
        self.palette_images = {}

        self.active_widget = None

        self.build_ui()

        # Enterで計算
        self.root.bind(
            "<Return>",
            lambda event:
                self.calculate_equity(),
        )

        # Escで全消去
        self.root.bind(
            "<Escape>",
            lambda event:
                self.clear_cards(),
        )

    def build_ui(self):
        title = tk.Label(
            self.root,
            text=(
                "Texas Hold'em "
                "Equity Calculator"
            ),
            font=(
                "Arial",
                24,
                "bold",
            ),
            fg="white",
            bg=TABLE_COLOR,
        )

        title.pack(
            pady=(18, 5),
        )

        instruction = tk.Label(
            self.root,
            text=(
                "カード枠を選択してから"
                "下のパレットをクリック\n"
                "右クリックまたは"
                "ダブルクリックで1枚解除"
            ),
            font=(
                "Arial",
                11,
            ),
            fg="white",
            bg=TABLE_COLOR,
            justify="center",
        )

        instruction.pack(
            pady=(0, 12),
        )

        self.build_board_section()
        self.build_player_section()
        self.build_button_section()
        self.build_result_section()
        self.build_palette_section()

        self.set_active_widget(
            self.hero_cards[0]
        )

    def build_board_section(self):
        tk.Label(
            self.root,
            text="Board",
            font=(
                "Arial",
                17,
                "bold",
            ),
            fg="white",
            bg=TABLE_COLOR,
        ).pack()

        board_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )

        board_frame.pack(
            pady=(8, 16),
        )

        for _ in range(5):
            widget = CardWidget(
                board_frame,
                width=72,
                height=104,
                click_callback=(
                    self.set_active_widget
                ),
                clear_callback=(
                    self.clear_single_card
                ),
            )

            widget.pack(
                side="left",
                padx=5,
            )

            self.board_cards.append(
                widget
            )

    def build_player_section(self):
        players_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )

        players_frame.pack(
            pady=5,
        )

        # Hero
        hero_section = tk.Frame(
            players_frame,
            bg=TABLE_COLOR,
        )

        hero_section.grid(
            row=0,
            column=0,
            padx=70,
        )

        tk.Label(
            hero_section,
            text="Hero",
            font=(
                "Arial",
                17,
                "bold",
            ),
            fg="white",
            bg=TABLE_COLOR,
        ).pack()

        hero_cards_frame = tk.Frame(
            hero_section,
            bg=TABLE_COLOR,
        )

        hero_cards_frame.pack(
            pady=8,
        )

        for _ in range(2):
            widget = CardWidget(
                hero_cards_frame,
                width=82,
                height=118,
                click_callback=(
                    self.set_active_widget
                ),
                clear_callback=(
                    self.clear_single_card
                ),
            )

            widget.pack(
                side="left",
                padx=7,
            )

            self.hero_cards.append(
                widget
            )

        # Opponent
        opponent_section = tk.Frame(
            players_frame,
            bg=TABLE_COLOR,
        )

        opponent_section.grid(
            row=0,
            column=1,
            padx=70,
        )

        tk.Label(
            opponent_section,
            text="Opponent",
            font=(
                "Arial",
                17,
                "bold",
            ),
            fg="white",
            bg=TABLE_COLOR,
        ).pack()

        opponent_cards_frame = tk.Frame(
            opponent_section,
            bg=TABLE_COLOR,
        )

        opponent_cards_frame.pack(
            pady=8,
        )

        for _ in range(2):
            widget = CardWidget(
                opponent_cards_frame,
                width=82,
                height=118,
                click_callback=(
                    self.set_active_widget
                ),
                clear_callback=(
                    self.clear_single_card
                ),
            )

            widget.pack(
                side="left",
                padx=7,
            )

            self.opponent_cards.append(
                widget
            )

    def build_button_section(self):
        button_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )

        button_frame.pack(
            pady=12,
        )

        ActionButton(
            button_frame,
            "Calculate Equity",
            self.calculate_equity,
        ).pack(
            side="left",
            padx=8,
        )

        ActionButton(
            button_frame,
            "Clear",
            self.clear_cards,
        ).pack(
            side="left",
            padx=8,
        )

    def build_result_section(self):
        result_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )

        result_frame.pack(
            pady=(2, 12),
        )

        self.result_box = tk.Label(
            result_frame,
            text=(
                "Hero Equity: --    "
                "Opponent Equity: --"
            ),
            font=(
                "Arial",
                17,
                "bold",
            ),
            fg="yellow",
            bg=TABLE_COLOR,
        )

        self.result_box.pack(
            pady=(0, 8),
        )

        self.equity_bar = tk.Canvas(
            result_frame,
            width=700,
            height=34,
            bg="#222222",
            highlightthickness=0,
        )

        self.equity_bar.pack()

        self.draw_equity_bar(
            None,
            None,
        )

    def build_palette_section(self):
        palette_container = tk.Frame(
            self.root,
            bg=PANEL_COLOR,
            relief="ridge",
            borderwidth=3,
        )

        palette_container.pack(
            padx=20,
            pady=(5, 18),
            fill="x",
        )

        tk.Label(
            palette_container,
            text="Card Palette",
            font=(
                "Arial",
                14,
                "bold",
            ),
            fg="white",
            bg=PANEL_COLOR,
        ).pack(
            pady=(7, 4),
        )

        palette_frame = tk.Frame(
            palette_container,
            bg=PANEL_COLOR,
        )

        palette_frame.pack(
            pady=(0, 8),
        )

        for row, (
            suit_code,
            suit_symbol,
        ) in enumerate(SUITS):

            suit_color = (
                "#FF4D4D"
                if suit_code in {"h", "d"}
                else "white"
            )

            tk.Label(
                palette_frame,
                text=suit_symbol,
                font=(
                    "Arial",
                    20,
                    "bold",
                ),
                fg=suit_color,
                bg=PANEL_COLOR,
                width=2,
            ).grid(
                row=row,
                column=0,
                padx=(4, 8),
            )

            for column, rank in enumerate(
                RANKS,
                start=1,
            ):
                card = rank + suit_code

                try:
                    image = CardImage.load(
                        card,
                        42,
                        59,
                    )

                    self.palette_images[
                        card
                    ] = image

                    button = tk.Button(
                        palette_frame,
                        image=image,
                        width=45,
                        height=62,
                        relief="raised",
                        borderwidth=2,
                        cursor="hand2",
                        command=(
                            lambda selected=card:
                                self.select_palette_card(
                                    selected
                                )
                        ),
                    )

                except FileNotFoundError:
                    button = tk.Button(
                        palette_frame,
                        text=(
                            f"{rank}"
                            f"{suit_symbol}"
                        ),
                        width=4,
                        height=2,
                        font=(
                            "Arial",
                            10,
                            "bold",
                        ),
                        cursor="hand2",
                        command=(
                            lambda selected=card:
                                self.select_palette_card(
                                    selected
                                )
                        ),
                    )

                button.grid(
                    row=row,
                    column=column,
                    padx=2,
                    pady=2,
                )

                self.palette_buttons[
                    card
                ] = button

    def get_all_widgets(self):
        """
        自動移動順。

        Hero
        → Opponent
        → Board
        """
        return (
            self.hero_cards
            + self.opponent_cards
            + self.board_cards
        )

    def get_selected_cards(self):
        """選択済みカードを返す。"""
        return [
            widget.card
            for widget
            in self.get_all_widgets()
            if widget.card is not None
        ]

    def set_active_widget(
        self,
        widget,
    ):
        """入力対象の枠を変更する。"""
        if self.active_widget is not None:
            self.active_widget.set_active(
                False
            )

        self.active_widget = widget

        self.active_widget.set_active(
            True
        )

        self.update_palette_buttons()

    def select_palette_card(
        self,
        card,
    ):
        """カードを現在の枠へ設定する。"""
        if self.active_widget is None:
            return

        used_cards = (
            self.get_selected_cards()
        )

        if (
            self.active_widget.card
            in used_cards
        ):
            used_cards.remove(
                self.active_widget.card
            )

        if card in used_cards:
            return

        self.active_widget.set_card(
            card
        )

        self.reset_results()

        self.update_palette_buttons()
        self.move_to_next_empty_widget()

    def move_to_next_empty_widget(self):
        """次の空き枠へ自動移動する。"""
        all_widgets = (
            self.get_all_widgets()
        )

        if (
            self.active_widget
            not in all_widgets
        ):
            return

        current_index = (
            all_widgets.index(
                self.active_widget
            )
        )

        for index in range(
            current_index + 1,
            len(all_widgets),
        ):
            if (
                all_widgets[index].card
                is None
            ):
                self.set_active_widget(
                    all_widgets[index]
                )
                return

        for index in range(
            0,
            current_index,
        ):
            if (
                all_widgets[index].card
                is None
            ):
                self.set_active_widget(
                    all_widgets[index]
                )
                return

        self.active_widget.set_active(
            False
        )

        self.active_widget = None

    def clear_single_card(
        self,
        widget,
    ):
        """指定されたカード1枚だけを解除する。"""
        widget.clear()

        self.set_active_widget(
            widget
        )

        self.reset_results()
        self.update_palette_buttons()

    def update_palette_buttons(self):
        """使用済みカードを無効化する。"""
        used_cards = set(
            self.get_selected_cards()
        )

        current_card = (
            self.active_widget.card
            if self.active_widget
            else None
        )

        for card, button in (
            self.palette_buttons.items()
        ):
            if (
                card in used_cards
                and card != current_card
            ):
                button.config(
                    state="disabled",
                    relief="sunken",
                )

            else:
                button.config(
                    state="normal",
                    relief="raised",
                )

    def get_card_text(
        self,
        widgets,
    ):
        """AsKs形式へ変換する。"""
        return "".join(
            widget.card or ""
            for widget in widgets
        )

    def draw_equity_bar(
        self,
        hero_equity,
        opponent_equity,
    ):
        """エクイティバーを描画する。"""
        self.equity_bar.delete(
            "all"
        )

        width = 700
        height = 34

        if (
            hero_equity is None
            or opponent_equity is None
        ):
            self.equity_bar.create_rectangle(
                0,
                0,
                width,
                height,
                fill="#444444",
                outline="",
            )

            self.equity_bar.create_text(
                width / 2,
                height / 2,
                text="No calculation yet",
                fill="white",
                font=(
                    "Arial",
                    11,
                    "bold",
                ),
            )

            return

        hero_width = (
            width * hero_equity
        )

        self.equity_bar.create_rectangle(
            0,
            0,
            hero_width,
            height,
            fill="#2F80ED",
            outline="",
        )

        self.equity_bar.create_rectangle(
            hero_width,
            0,
            width,
            height,
            fill="#EB5757",
            outline="",
        )

        if hero_width > 100:
            self.equity_bar.create_text(
                hero_width / 2,
                height / 2,
                text=(
                    f"Hero "
                    f"{hero_equity:.1%}"
                ),
                fill="white",
                font=(
                    "Arial",
                    11,
                    "bold",
                ),
            )

        opponent_width = (
            width - hero_width
        )

        if opponent_width > 100:
            self.equity_bar.create_text(
                (
                    hero_width
                    + opponent_width / 2
                ),
                height / 2,
                text=(
                    f"Opponent "
                    f"{opponent_equity:.1%}"
                ),
                fill="white",
                font=(
                    "Arial",
                    11,
                    "bold",
                ),
            )

    def calculate_equity(self):
        """現在のカードで計算する。"""
        hero_text = self.get_card_text(
            self.hero_cards
        )

        opponent_text = (
            self.get_card_text(
                self.opponent_cards
            )
        )

        board_text = self.get_card_text(
            self.board_cards
        )

        self.result_box.config(
            text="Calculating...",
            fg="white",
        )

        self.root.update_idletasks()

        try:
            hero = ec.parse_cards(
                hero_text,
                "Hero",
            )

            opponent = ec.parse_cards(
                opponent_text,
                "Opponent",
            )

            board = ec.parse_cards(
                board_text,
                "Board",
            )

            ec.validate_hand(
                hero,
                "Hero",
                2,
            )

            ec.validate_hand(
                opponent,
                "Opponent",
                2,
            )

            ec.validate_board(
                board
            )

            ec.validate_no_duplicates(
                hero,
                opponent,
                board,
            )

            (
                hero_equity,
                opponent_equity,
            ) = ec.calculate_equity(
                hero,
                opponent,
                board,
            )

            board_display = (
                board_text
                if board_text
                else "Preflop"
            )

            self.result_box.config(
                text=(
                    f"Board: "
                    f"{board_display}    "
                    f"Hero Equity: "
                    f"{hero_equity:.2%}    "
                    f"Opponent Equity: "
                    f"{opponent_equity:.2%}"
                ),
                fg="yellow",
            )

            self.draw_equity_bar(
                hero_equity,
                opponent_equity,
            )

        except ValueError as error:
            self.result_box.config(
                text=f"Error: {error}",
                fg="#FF5555",
            )

            self.draw_equity_bar(
                None,
                None,
            )

        except Exception as error:
            self.result_box.config(
                text=(
                    f"Unexpected Error: "
                    f"{error}"
                ),
                fg="#FF5555",
            )

            self.draw_equity_bar(
                None,
                None,
            )

    def reset_results(self):
        """カード変更時に結果をリセットする。"""
        self.result_box.config(
            text=(
                "Hero Equity: --    "
                "Opponent Equity: --"
            ),
            fg="yellow",
        )

        self.draw_equity_bar(
            None,
            None,
        )

    def clear_cards(self):
        """全カードを解除する。"""
        for widget in (
            self.get_all_widgets()
        ):
            widget.clear()

        self.reset_results()

        self.set_active_widget(
            self.hero_cards[0]
        )

        self.update_palette_buttons()