import random
import typing as t
from dataclasses import dataclass

SUITS = ['clubs', 'diamonds', 'spades', 'hearts']
RANKS = [9,10,11,12,13,14]

@dataclass
class Card:
    suit: str
    rank: int

    def score(self, trump, lead):
        """Returns a score, relative to a given trump, to compare cards during
        a game."""
        return self.rank + \
            (100 if self.suit == trump else 0) + \
            (50 if self.suit == lead else 0)

@dataclass
class Pile:
    @staticmethod
    def make_deck(cls):
        return Pile(Card(suit, rank) for suit in SUITS for rank in RANKS)

    def shuffle(self):
        random.shuffle(self.cards)

    def __init__(self, cards=None):
        self.cards = cards or []

    def maximum(self, trump, lead):
        return max(self.cards, key=lambda c: c.score(trump, lead))

    def find_index(self, card):
        return self.cards.index(card)

    def add(self, card):
        self.cards.append(card)

    def pick(self, index):
        return self.cards.pop(index)

    def sort(self, trump, lead):
        self.cards.sort(key=lambda c: c.score(trump, lead))

@dataclass
class Player:
    hand: Pile
    team: t.Literal[0, 1]
    trick_count: int

    @staticmethod
    def make_empty(cls):
        return Player(hand=Pile(), team=0, trick_count=0)
