"""
Roller class file

Copyright (C) 2023 _kodokami
"""
import os
import random
import re
import struct
from dataclasses import dataclass
from math import ceil as ceiling
from time import time
from typing import List

from . import Dice

ROLL_PATTERN = re.compile('^([1-9][0-9]*)[kd](4|6|8|10|12|20)([+-][1-9]+[0-9]*)?$')


@dataclass(frozen=True)
class DiceRollStats:
    """Class representing the dice roll statistics"""
    min: int
    max: int
    avg: int


@dataclass(frozen=True)
class DiceRoll:
    """Class representing a thrown dice roll"""
    dice_roll: str
    result: int
    subsequent_rolls: List[int]
    roll_stats: DiceRollStats

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
        for throw in dices:
            match = ROLL_PATTERN.match(throw)
            if match is None:
                raise ValueError(f'Invalid dice roll pattern "{throw}".')

            # dices to throw; group1 - dices count, group2 - dice type
            dices = [Dice(int(match.group(2))) for _ in range(int(match.group(1)))]

            if match.group(3) is not None:
                self.rolls_to_execute.append(
                    self.DiceRollToExecute(
                        dice_roll=throw,
                        dices=dices,
                        addition=int(match.group(3))
                    )
                )
            else:
                self.rolls_to_execute.append(
                    self.DiceRollToExecute(
                        dice_roll=throw,
                        dices=dices
                    )
                )

    def roll(self) -> List[DiceRoll]:
        """roll dices"""
        executed_rolls = []
        for roll in self.rolls_to_execute:
            subsequent_dices = [dice.roll() for dice in roll.dices]
            executed_rolls.append(
                DiceRoll(
                    dice_roll=roll.dice_roll,
                    result=sum(subsequent_dices) + roll.addition,
                    subsequent_rolls=subsequent_dices,
                    roll_stats=DiceRollStats(
                        min=len(roll.dices) + roll.addition,
                        max=len(roll.dices) * roll.dices[0].sides_count + roll.addition,
                        avg=ceiling(
                            # pylint: disable=C0301
                            # all allowed dice types have even sides count, that why we are adding 0.5 to
                            # the statistically average throw, eg. for k20 dice an average throw would be 10.5
                            len(roll.dices) * (roll.dices[0].sides_count / 2 + 0.5)
                        ) + roll.addition
                    )
                )
            )

        return executed_rolls

    @staticmethod
    def _init_randomness():
        """initialize random library with a true random seed"""
        data_format = 'I'
        try:
            random.seed(
                struct.unpack(
                    data_format,
                    os.urandom(struct.calcsize(data_format))
                )[0]
            )
        except NotImplementedError as err:
            # TODO - change this to warn log when logging will be added
            print(
                'Warn: os.urandom() not available, using time based seed. '
                f'Original message: {err}'
            )
            random.seed(time())

    @dataclass(frozen=True)
    class DiceRollToExecute:
        """Class representing a dice roll that awaits to be thrown"""
        dice_roll: str
        dices: List[Dice]
        addition: int = 0
