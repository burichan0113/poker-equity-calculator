from deck import Deck


deck = Deck()

deck.shuffle()


print("Hero:")
print(deck.deal())
print(deck.deal())


print("Board:")
for i in range(5):
    print(deck.deal())