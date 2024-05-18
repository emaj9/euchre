import typing as t
from dataclasses import dataclass

@dataclass
class Card:
    suit: str
    rank: int
