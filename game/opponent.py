from typing import Any

class Opponent():
    def __init__(self, difficulty: int, name: str, health: int, rew: dict[str, Any], deck: list[dict[str, Any]], tok_rew: int):
        self.difficulty = difficulty
        self.name = name
        self.health = health
        self.rew = rew
        self.deck = deck
        self.tok_rew = tok_rew