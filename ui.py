import tkinter as tk

import equity_calculator as ec

from widgets import (
    ActionButton,
    CardImage,
    CardWidget,
)


TABLE_COLOR = "#075E2A"
PANEL_COLOR = "#064D25"
SECTION_COLOR = "#0A6B34"

RANKS = [
    "A",
    "K",
    "Q",
    "J",
    "T",
    "9",
    "8",
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
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

        self.root.title("Poker Equity Calculator")
        self.root.geometry("1500x850")
        self.root.minsize(1400, 780)
        self.root.configure(bg=TABLE_COLOR)

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
            lambda event: self.calculate_equity(),
        )

        # Escで全消去
        self.root.bind(
            "<Escape>",
            lambda event: self.clear_cards(),
        )

    def build_ui(self):
        main_container = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )

        main_container.pack(
            expand=True,
            fill="both",
            padx=18,
            pady=14,
        )

        # 左側：ゲーム画面
        self.left_panel = tk.Frame(
            main_container,
            bg=TABLE_COLOR,
        )

        self.left_panel.pack(
            side="left",
            expand=True,
            fill="both",
            padx=(0, 14),
        )

        # 右側：カードパレット
        self.right_panel = tk.Frame(
            main_container,
            bg=PANEL_COLOR,
            relief="ridge",
            borderwidth=3,
            width=690,
        )

        self.right_panel.pack(
            side="right",
            fill="y",
        )

        self.right_panel.pack_propagate(False)

        self.build_left_panel()
        self.build_palette_section()

        # 最初はHeroの1枚目を選択
        self.set_active_widget(
            self.hero_cards[0]
        )

    def build_left_panel(self):
        tk.Label(
            self.left_panel,
            text="Texas Hold'em Equity Calculator",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        ).pack(
            pady=(12, 5),
        )

        tk.Label(
            self.left_panel,
            text=(
                "Click a card slot, then choose a card.\n"
                "Right-click or double-click to clear."
            ),
            font=("Arial", 11),
            fg="white",
            bg=TABLE_COLOR,
            justify="center",
        ).pack(
            pady=(0, 14),
        )

        self.build_board_section()
        self.build_player_section()
        self.build_button_section()
        self.build_result_section()

    def build_board_section(self):
        board_container = tk.Frame(
            self.left_panel,
            bg=SECTION_COLOR,
            relief="ridge",
            borderwidth=3,
        )

        board_container.pack(
            padx=20,
            pady=(4, 16),
        )

        tk.Label(
            board_container,
            text="Board",
            font=("Arial", 18, "bold"),
            fg="white",
            bg=SECTION_COLOR,
        ).pack(
            pady=(8, 4),
        )

        streets_frame = tk.Frame(
            board_container,
            bg=SECTION_COLOR,
        )

        streets_frame.pack(
            padx=14,
            pady=(0, 12),
        )

        # Flop
        flop_section = tk.Frame(
            streets_frame,
            bg=SECTION_COLOR,
        )

        flop_section.grid(
            row=0,
            column=0,
            padx=(0, 14),
        )

        tk.Label(
            flop_section,
            text="Flop",
            font=("Arial", 13, "bold"),
            fg="white",
            bg=SECTION_COLOR,
        ).pack(
            pady=(0, 5),
        )

        flop_cards_frame = tk.Frame(
            flop_section,
            bg=SECTION_COLOR,
        )

        flop_cards_frame.pack()

        for _ in range(3):
            widget = CardWidget(
                flop_cards_frame,
                width=72,
                height=104,
                click_callback=self.set_active_widget,
                clear_callback=self.clear_single_card,
            )

            widget.pack(
                side="left",
                padx=5,
            )

            self.board_cards.append(widget)

        # Flop / Turn separator
        tk.Frame(
            streets_frame,
            width=2,
            height=130,
            bg="#D9D9D9",
        ).grid(
            row=0,
            column=1,
            padx=5,
            sticky="ns",
        )

        # Turn
        turn_section = tk.Frame(
            streets_frame,
            bg=SECTION_COLOR,
        )

        turn_section.grid(
            row=0,
            column=2,
            padx=14,
        )

        tk.Label(
            turn_section,
            text="Turn",
            font=("Arial", 13, "bold"),
            fg="white",
            bg=SECTION_COLOR,
        ).pack(
            pady=(0, 5),
        )

        turn_widget = CardWidget(
            turn_section,
            width=72,
            height=104,
            click_callback=self.set_active_widget,
            clear_callback=self.clear_single_card,
        )

        turn_widget.pack(
            padx=5,
        )

        self.board_cards.append(turn_widget)

        # Turn / River separator
        tk.Frame(
            streets_frame,
            width=2,
            height=130,
            bg="#D9D9D9",
        ).grid(
            row=0,
            column=3,
            padx=5,
            sticky="ns",
        )

        # River
        river_section = tk.Frame(
            streets_frame,
            bg=SECTION_COLOR,
        )

        river_section.grid(
            row=0,
            column=4,
            padx=(14, 0),
        )

        tk.Label(
            river_section,
            text="River",
            font=("Arial", 13, "bold"),
            fg="white",
            bg=SECTION_COLOR,
        ).pack(
            pady=(0, 5),
        )

        river_widget = CardWidget(
            river_section,
            width=72,
            height=104,
            click_callback=self.set_active_widget,
            clear_callback=self.clear_single_card,
        )

        river_widget.pack(
            padx=5,
        )

        self.board_cards.append(river_widget)

    def build_player_section(self):
        players_frame = tk.Frame(
            self.left_panel,
            bg=TABLE_COLOR,
        )

        players_frame.pack(
            pady=8,
        )

        # Hero
        hero_section = tk.Frame(
            players_frame,
            bg=TABLE_COLOR,
        )

        hero_section.grid(
            row=0,
            column=0,
            padx=42,
        )

        tk.Label(
            hero_section,
            text="Hero",
            font=("Arial", 17, "bold"),
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
                click_callback=self.set_active_widget,
                clear_callback=self.clear_single_card,
            )

            widget.pack(
                side="left",
                padx=7,
            )

            self.hero_cards.append(widget)

        # Opponent
        opponent_section = tk.Frame(
            players_frame,
            bg=TABLE_COLOR,
        )

        opponent_section.grid(
            row=0,
            column=1,
            padx=42,
        )

        tk.Label(
            opponent_section,
            text="Opponent",
            font=("Arial", 17, "bold"),
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
                click_callback=self.set_active_widget,
                clear_callback=self.clear_single_card,
            )

            widget.pack(
                side="left",
                padx=7,
            )

            self.opponent_cards.append(widget)

    def build_button_section(self):
        button_frame = tk.Frame(
            self.left_panel,
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
            self.left_panel,
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
            font=("Arial", 16, "bold"),
            fg="yellow",
            bg=TABLE_COLOR,
        )

        self.result_box.pack(
            pady=(0, 8),
        )

        self.equity_bar = tk.Canvas(
            result_frame,
            width=620,
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
        tk.Label(
            self.right_panel,
            text="Card Palette",
            font=("Arial", 18, "bold"),
            fg="white",
            bg=PANEL_COLOR,
        ).pack(
            pady=(10, 6),
        )

        tk.Label(
            self.right_panel,
            text="Select a card for the highlighted slot",
            font=("Arial", 10),
            fg="white",
            bg=PANEL_COLOR,
        ).pack(
            pady=(0, 10),
        )

        palette_frame = tk.Frame(
            self.right_panel,
            bg=PANEL_COLOR,
        )

        palette_frame.pack(
            pady=4,
        )

        # 13行 × 4列
        # A♠ A♥ A♦ A♣
        # K♠ K♥ K♦ K♣
        # ...
        for row, rank in enumerate(RANKS):
            for column, (
                suit_code,
                suit_symbol,
            ) in enumerate(SUITS):

                card = rank + suit_code

                try:
                    image = CardImage.load(
                        card,
                        32,
                        45,
                    )

                    self.palette_images[card] = image

                    button = tk.Button(
                        palette_frame,
                        image=image,
                        width=36,
                        height=49,
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
                    text_color = (
                        "#FF4D4D"
                        if suit_code in {"h", "d"}
                        else "black"
                    )

                    button = tk.Button(
                        palette_frame,
                        text=f"{rank}{suit_symbol}",
                        width=4,
                        height=2,
                        font=("Arial", 9, "bold"),
                        fg=text_color,
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
                    pady=1,
                )

                self.palette_buttons[card] = button

    def get_all_widgets(self):
        return (
            self.hero_cards
            + self.opponent_cards
            + self.board_cards
        )

    def get_selected_cards(self):
        return [
            widget.card
            for widget in self.get_all_widgets()
            if widget.card is not None
        ]

    def set_active_widget(self, widget):
        if self.active_widget is not None:
            self.active_widget.set_active(False)

        self.active_widget = widget
        self.active_widget.set_active(True)

        self.update_palette_buttons()

    def select_palette_card(self, card):
        if self.active_widget is None:
            return

        used_cards = self.get_selected_cards()

        # 現在の枠に入っているカードは変更可能
        if self.active_widget.card in used_cards:
            used_cards.remove(
                self.active_widget.card
            )

        if card in used_cards:
            return

        self.active_widget.set_card(card)

        self.reset_results()
        self.update_palette_buttons()
        self.move_to_next_empty_widget()

    def move_to_next_empty_widget(self):
        all_widgets = self.get_all_widgets()

        if self.active_widget not in all_widgets:
            return

        current_index = all_widgets.index(
            self.active_widget
        )

        # 現在より後ろの空き枠を探す
        for index in range(
            current_index + 1,
            len(all_widgets),
        ):
            if all_widgets[index].card is None:
                self.set_active_widget(
                    all_widgets[index]
                )
                return

        # 後ろになければ前方を探す
        for index in range(
            0,
            current_index,
        ):
            if all_widgets[index].card is None:
                self.set_active_widget(
                    all_widgets[index]
                )
                return

        # 全部埋まった場合
        self.active_widget.set_active(False)
        self.active_widget = None

    def clear_single_card(self, widget):
        widget.clear()

        self.set_active_widget(widget)

        self.reset_results()
        self.update_palette_buttons()

    def update_palette_buttons(self):
        used_cards = set(
            self.get_selected_cards()
        )

        current_card = (
            self.active_widget.card
            if self.active_widget
            else None
        )

        for card, button in self.palette_buttons.items():
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

    def get_card_text(self, widgets):
        return "".join(
            widget.card or ""
            for widget in widgets
        )

    def validate_board_order(self):
        seen_empty = False

        for widget in self.board_cards:
            if widget.card is None:
                seen_empty = True

            elif seen_empty:
                raise ValueError(
                    "Board cards must be selected from left to right."
                )

    def draw_equity_bar(
        self,
        hero_equity,
        opponent_equity,
    ):
        self.equity_bar.delete("all")

        width = 620
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
                font=("Arial", 11, "bold"),
            )

            return

        hero_width = width * hero_equity

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

        if hero_width > 90:
            self.equity_bar.create_text(
                hero_width / 2,
                height / 2,
                text=f"Hero {hero_equity:.1%}",
                fill="white",
                font=("Arial", 11, "bold"),
            )

        opponent_width = width - hero_width

        if opponent_width > 90:
            self.equity_bar.create_text(
                hero_width + opponent_width / 2,
                height / 2,
                text=(
                    f"Opponent "
                    f"{opponent_equity:.1%}"
                ),
                fill="white",
                font=("Arial", 11, "bold"),
            )

    def calculate_equity(self):
        hero_text = self.get_card_text(
            self.hero_cards
        )

        opponent_text = self.get_card_text(
            self.opponent_cards
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
            self.validate_board_order()

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

            ec.validate_board(board)

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
                    f"Board: {board_display}    "
                    f"Hero: {hero_equity:.2%}    "
                    f"Opponent: {opponent_equity:.2%}"
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
        for widget in self.get_all_widgets():
            widget.clear()

        self.reset_results()

        self.set_active_widget(
            self.hero_cards[0]
        )

        self.update_palette_buttons()