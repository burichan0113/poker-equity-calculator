import tkinter as tk

import equity_calculator as ec

from card_selector import CardSelector
from widgets import CardWidget, ActionButton


TABLE_COLOR = "#075E2A"


class PokerUI:

    def __init__(self, root):
        self.root = root

        self.root.title("Poker Equity Calculator")
        self.root.geometry("1000x820")
        self.root.configure(bg=TABLE_COLOR)
        self.root.resizable(True, True)

        self.board_cards = []
        self.hero_cards = []
        self.opponent_cards = []

        self.card_selector = None
        self.active_widget_index = None

        self.build_ui()

        # Enterで計算、Escapeでクリア
        self.root.bind("<Return>", lambda event: self.calculate_equity())
        self.root.bind("<Escape>", lambda event: self.clear_cards())

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Texas Hold'em Equity Calculator",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        )
        title.pack(pady=20)

        instruction = tk.Label(
            self.root,
            text=(
                "カードをクリックして選択してください\n"
                "Boardは空欄、または3・4・5枚に対応"
            ),
            font=("Arial", 12),
            fg="white",
            bg=TABLE_COLOR,
            justify="center",
        )
        instruction.pack(pady=(0, 15))

        # Board
        board_label = tk.Label(
            self.root,
            text="Board",
            font=("Arial", 17, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        )
        board_label.pack()

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
                click_callback=self.open_card_selector,
            )

            widget.pack(
                side="left",
                padx=7,
            )

            self.board_cards.append(widget)

        # Player area
        players_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )
        players_frame.pack(pady=25)

        # Hero
        hero_section = tk.Frame(
            players_frame,
            bg=TABLE_COLOR,
        )
        hero_section.grid(
            row=0,
            column=0,
            padx=60,
        )

        hero_label = tk.Label(
            hero_section,
            text="Hero",
            font=("Arial", 17, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        )
        hero_label.pack()

        hero_cards_frame = tk.Frame(
            hero_section,
            bg=TABLE_COLOR,
        )
        hero_cards_frame.pack(pady=10)

        for _ in range(2):
            widget = CardWidget(
                hero_cards_frame,
                width=90,
                height=130,
                click_callback=self.open_card_selector,
            )

            widget.pack(
                side="left",
                padx=10,
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
            padx=60,
        )

        opponent_label = tk.Label(
            opponent_section,
            text="Opponent",
            font=("Arial", 17, "bold"),
            fg="white",
            bg=TABLE_COLOR,
        )
        opponent_label.pack()

        opponent_cards_frame = tk.Frame(
            opponent_section,
            bg=TABLE_COLOR,
        )
        opponent_cards_frame.pack(pady=10)

        for _ in range(2):
            widget = CardWidget(
                opponent_cards_frame,
                width=90,
                height=130,
                click_callback=self.open_card_selector,
            )

            widget.pack(
                side="left",
                padx=10,
            )

            self.opponent_cards.append(widget)

        # Buttons
        button_frame = tk.Frame(
            self.root,
            bg=TABLE_COLOR,
        )
        button_frame.pack(pady=20)

        ActionButton(
            button_frame,
            "Calculate Equity",
            self.calculate_equity,
        ).pack(
            side="left",
            padx=10,
        )

        ActionButton(
            button_frame,
            "Clear",
            self.clear_cards,
        ).pack(
            side="left",
            padx=10,
        )

        # Results
        self.result_box = tk.Label(
            self.root,
            text=(
                "Hero Equity: --\n"
                "Opponent Equity: --"
            ),
            font=("Arial", 18, "bold"),
            fg="yellow",
            bg=TABLE_COLOR,
            justify="left",
        )

        self.result_box.pack(pady=10)

    def get_all_widgets(self):
        """
        カード選択の移動順。
        Hero → Opponent → Board
        """
        return (
            self.hero_cards
            + self.opponent_cards
            + self.board_cards
        )

    def get_all_selected_cards(self):
        """現在選択されているカードコードを返す。"""
        return [
            widget.card
            for widget in self.get_all_widgets()
            if widget.card is not None
        ]

    def open_card_selector(self, target_widget):
        """対象のカード枠を選択状態にして選択画面を開く。"""
        all_widgets = self.get_all_widgets()

        self.active_widget_index = all_widgets.index(
            target_widget
        )

        used_cards = self.get_all_selected_cards()

        # 現在の枠に入っているカードは変更可能にする
        if target_widget.card in used_cards:
            used_cards.remove(target_widget.card)

        if (
            self.card_selector is None
            or not self.card_selector.winfo_exists()
        ):
            self.card_selector = CardSelector(
                self.root,
                callback=self.handle_card_selected,
                used_cards=used_cards,
            )
        else:
            self.card_selector.update_used_cards(
                used_cards
            )
            self.card_selector.lift()
            self.card_selector.focus_force()

    def handle_card_selected(self, card):
        """
        選択したカードを現在の枠に設定し、
        次の未選択枠へ自動で移動する。
        """
        all_widgets = self.get_all_widgets()

        if self.active_widget_index is None:
            return

        current_widget = all_widgets[
            self.active_widget_index
        ]

        current_widget.set_card(card)

        used_cards = self.get_all_selected_cards()

        if (
            self.card_selector
            and self.card_selector.winfo_exists()
        ):
            self.card_selector.update_used_cards(
                used_cards
            )

        next_index = self.find_next_empty_widget(
            self.active_widget_index + 1
        )

        if next_index is None:
            self.close_card_selector()
            return

        self.active_widget_index = next_index

    def find_next_empty_widget(self, start_index):
        """次の空いているカード枠を探す。"""
        all_widgets = self.get_all_widgets()

        for index in range(
            start_index,
            len(all_widgets),
        ):
            if all_widgets[index].card is None:
                return index

        for index in range(
            0,
            start_index,
        ):
            if all_widgets[index].card is None:
                return index

        return None

    def get_card_text(self, widgets):
        """CardWidgetの内容をPokerKit用文字列にする。"""
        return "".join(
            widget.card or ""
            for widget in widgets
        )

    def calculate_equity(self):
        """Hero・Opponent・Boardからエクイティを計算する。"""
        hero_text = self.get_card_text(
            self.hero_cards
        )

        opponent_text = self.get_card_text(
            self.opponent_cards
        )

        board_text = self.get_card_text(
            self.board_cards
        )

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

            hero_equity, opponent_equity = ec.calculate_equity(
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
                    f"Board: {board_display}\n"
                    f"Hero Equity: {hero_equity:.2%}\n"
                    f"Opponent Equity: {opponent_equity:.2%}"
                ),
                fg="yellow",
            )

        except ValueError as error:
            self.result_box.config(
                text=f"Error: {error}",
                fg="red",
            )

        except Exception as error:
            self.result_box.config(
                text=f"Unexpected Error: {error}",
                fg="red",
            )

    def close_card_selector(self):
        """カード選択画面を安全に閉じる。"""
        if (
            self.card_selector
            and self.card_selector.winfo_exists()
        ):
            self.card_selector.destroy()

        self.card_selector = None
        self.active_widget_index = None

    def clear_cards(self):
        """すべてのカードと結果を初期化する。"""
        for widget in self.get_all_widgets():
            widget.clear()

        self.close_card_selector()

        self.result_box.config(
            text=(
                "Hero Equity: --\n"
                "Opponent Equity: --"
            ),
            fg="yellow",
        )