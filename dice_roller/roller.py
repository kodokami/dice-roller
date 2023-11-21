"""
Roller class file

Copyright (C) 2023 _kodokami
"""
import os
import random
import re
import struct
from dataclasses import dataclass
from typing import List

from . import Dice

ROLL_PATTERN = re.compile('^([1-9][0-9]*)[kd](4|6|8|10|12|20)$')


@dataclass(frozen=True)
class DiceRoll:
    """Class representing a dice roll"""
    dice_roll: str
    result: int
    subsequent_rolls: List[int]

    def __post_init__(self):
        """Data validation"""
        if ROLL_PATTERN.match(self.dice_roll) is None:
            raise ValueError('Unknown dice roll pattern')


class Roller:
    """Roller class"""

    def __init__(self, dices: List[str]):
        """dices : list of dices to roll in NdM or NkM pattern"""
        self._init_randomness()
        self.rolls_to_execute = []
        for dice in dices:
            match = ROLL_PATTERN.match(dice)
            dice_count, dice_sides = int(match.group(1)), int(match.group(2))
            self.rolls_to_execute.append(
                self.DiceRollToExecute(dice, [Dice(dice_sides) for _ in range(dice_count)])
            )

    def roll(self) -> List[DiceRoll]:
        """roll dices"""
        executed_rolls = []
        for roll in self.rolls_to_execute:
            subsequent_dices = [dice.roll() for dice in roll.dices]
            executed_rolls.append(
                DiceRoll(
                    dice_roll=roll.dice_roll,
                    result=sum(subsequent_dices),
                    subsequent_rolls=subsequent_dices
                )
            )

        return executed_rolls

    def _init_randomness(self):
        """initialize random library with a true random seed"""
        data_format = 'I'
        random.seed(
            struct.unpack(
                data_format,
                os.urandom(struct.calcsize(data_format))
            )[0]
        )

    @dataclass(frozen=True)
    class DiceRollToExecute:
        dice_roll: str
        dices: List[Dice]
