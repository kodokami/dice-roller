"""
Roller tests

Copyright (C) 2023 _kodokami
"""
from unittest.mock import Mock, patch

from dice_roller import Roller, DiceRoll

SAMPLE_SINGLE_DICE_ROLL = '1k20'
SIMULATED_SINGLE_ROLL_VALUE = 3

SAMPLE_MULTIPLE_DICE_ROLLS = ['1k10', '3k6']
SIMULATED_MULTIPLE_ROLLS = [8, 3, 5, 4]


class TestRoller:
    @patch("dice_roller.dice.randint", Mock(return_value=SIMULATED_SINGLE_ROLL_VALUE))
    def test_single_dice_roll(self):
        """Testing single dice roll with Roller class"""
        result = Roller([SAMPLE_SINGLE_DICE_ROLL]).roll()

        assert len(result) == 1
        assert isinstance(result[0], DiceRoll)
        assert result[0].dice_roll == SAMPLE_SINGLE_DICE_ROLL
        assert result[0].result == SIMULATED_SINGLE_ROLL_VALUE
        assert result[0].subsequent_rolls == [SIMULATED_SINGLE_ROLL_VALUE]

    @patch("dice_roller.dice.randint", Mock(side_effect=SIMULATED_MULTIPLE_ROLLS))
    def test_rolling_multiple_dices(self):
        """Testing multiple dice rolls"""
        result = Roller(SAMPLE_MULTIPLE_DICE_ROLLS).roll()

        assert len(result) == len(SAMPLE_MULTIPLE_DICE_ROLLS)
        for roll in result:
            assert isinstance(roll, DiceRoll)

        assert result[0].dice_roll == SAMPLE_MULTIPLE_DICE_ROLLS[0]
        assert result[0].result == 8
        assert result[0].subsequent_rolls == SIMULATED_MULTIPLE_ROLLS[:1]

        assert result[1].dice_roll == SAMPLE_MULTIPLE_DICE_ROLLS[1]
        assert result[1].result == sum(SIMULATED_MULTIPLE_ROLLS[1:4])
        assert result[1].subsequent_rolls == SIMULATED_MULTIPLE_ROLLS[1:4]

    @patch(
        "dice_roller.roller.os.urandom", Mock(side_effect=NotImplementedError('Simulated error'))
    )
    @patch("dice_roller.roller.time", Mock(return_value=123))
    def test_class_initialization_with_broken_entropy(self, capsys):
        """Testing if Roller class will initialize without systems entropy"""
        warning_message = 'Warn: os.urandom() not available, using time based seed. ' \
                          'Original message: Simulated error\n'
        result = Roller([SAMPLE_SINGLE_DICE_ROLL]).roll()

        assert len(result) == 1
        assert isinstance(result[0], DiceRoll)
        # the result of random.randint(1, 20) with random.seed(123) is 2
        assert result[0].result == 2
        assert capsys.readouterr().out == warning_message
