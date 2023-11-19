"""
Dice class file

Copyright (C) 2023 _kodokami
"""
from random import randint


class Dice:
    """Dice class"""

    def __init__(self, sides_count: int):
        """sides_count : the number of sides of the dice"""
        if sides_count <= 1:
            raise ValueError('Dice needs more than one side to be a dice!')
        self.sides_count = sides_count

    def roll(self) -> int:
        """Method for rolling the dice"""
        return randint(1, self.sides_count)
