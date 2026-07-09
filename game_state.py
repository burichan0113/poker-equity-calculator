class GameState:

    def __init__(self):

        self.hero = [None, None]

        self.opponent = [None, None]

        self.board = [None, None, None, None, None]

    def all_cards(self):

        cards = []

        cards.extend(c for c in self.hero if c)

        cards.extend(c for c in self.opponent if c)

        cards.extend(c for c in self.board if c)

        return cards