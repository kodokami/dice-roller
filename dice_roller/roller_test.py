"""
Roller tests

Copyright (C) 2023 _kodokami
"""
from unittest.mock import Mock, patch

import pytest

from dice_roller import Roller, DiceRoll

SAMPLE_SINGLE_DICE_ROLL = '1k20'
SIMULATED_SINGLE_ROLL_VALUE = 3

SAMPLE_MULTIPLE_DICE_ROLLS = ['1k10', '3k6']
SAMPLE_MULTIPLE_DICE_ROLLS_WITH_ADDITION = ['2k20+16', '5k6+2', '3k4-2']
SIMULATED_MULTIPLE_ROLLS = [8, 3, 5, 4, 3, 1, 6, 1, 1, 2]


class TestRoller:
    """Dice roller test class"""

    @pytest.mark.parametrize(
        'throw_pattern',
        [
            # simple throws
            '1k4', '1k6', '1k8', '1k10', '1k12', '1k20',
            '1d4', '1d6', '1d8', '1d10', '1d12', '1d20',
            # multiple throws
            '4k4', '34k6', '5k8', '53k10', '11k12', '8k20',
            '4d4', '34d6', '5d8', '53d10', '11d12', '8d20',
            # multiple throws width addition
            '12k4+2', '12k6+7', '13k8+8', '12k10+8', '81k12+6', '14k20+9',
            '12d4+2', '12d6+7', '13d8+8', '12d10+8', '81d12+6', '14d20+9',
            # multiple throws width subtraction
            '15k4-6', '14k6-6', '17k8-4', '15k10-3', '16k12-5', '12k20-7',
            '15d4-6', '14d6-6', '17d8-4', '15d10-3', '16d12-5', '12d20-7',
            # multiple throws with multiple digit addition or subtraction
            '15k4-45', '7k6+234', '1k8+46', '35k10-45', '1k12-56', '2k20+64',
            '15d4-45', '7d6+234', '1d8+46', '35d10-45', '1d12-56', '2d20+64',
        ]
    )
    @patch('dice_roller.roller.random.seed', Mock())
    def test_allowed_throw_patterns(self, throw_pattern: str):
        """Testing acceptance of a multiple throw patterns"""
        try:
            Roller([throw_pattern])
        except ValueError:
            pytest.fail(f'{throw_pattern} pattern was not accepted!')

    @pytest.mark.parametrize(
        'throw_pattern',
        [
            'k10', 'd10', 'k3', 'd5', '1k3', '1d5', '1b12', '1x20', '1kk12', '1dd20',
            '1k20++1', '1d20++1', '1k20++', '1d20--', '1k20+10+12', '1d12-1-2',
            '1k20k6', '1d12d4'
        ]
    )
    @patch('dice_roller.roller.random.seed', Mock())
    def test_illegal_throw_patterns(self, throw_pattern: str):
        """Testing denial of a multiple throw patterns"""
        with pytest.raises(ValueError) as err:
            Roller([throw_pattern])
        assert err.value.args[0] == f'Invalid dice roll pattern "{throw_pattern}".'

    @patch('dice_roller.dice.randint', Mock(return_value=SIMULATED_SINGLE_ROLL_VALUE))
    def test_single_dice_roll(self):
        """Testing single dice roll with Roller class"""
        result = Roller([SAMPLE_SINGLE_DICE_ROLL]).roll()

        # 1k20
        assert len(result) == 1
        assert isinstance(result[0], DiceRoll)
        assert result[0].dice_roll == SAMPLE_SINGLE_DICE_ROLL
        assert result[0].result == SIMULATED_SINGLE_ROLL_VALUE
        assert result[0].subsequent_rolls == [SIMULATED_SINGLE_ROLL_VALUE]
        assert result[0].roll_stats.min == 1
        assert result[0].roll_stats.max == 20
        assert result[0].roll_stats.avg == 11

    @patch('dice_roller.dice.randint', Mock(side_effect=SIMULATED_MULTIPLE_ROLLS))
    def test_rolling_multiple_dices(self):
        """Testing multiple dice rolls"""
        result = Roller(SAMPLE_MULTIPLE_DICE_ROLLS).roll()

        assert len(result) == len(SAMPLE_MULTIPLE_DICE_ROLLS)
        for roll in result:
            assert isinstance(roll, DiceRoll)

        # 1k10
        assert result[0].dice_roll == SAMPLE_MULTIPLE_DICE_ROLLS[0]
        assert result[0].result == SIMULATED_MULTIPLE_ROLLS[0]
        assert result[0].subsequent_rolls == SIMULATED_MULTIPLE_ROLLS[:1]
        assert result[0].roll_stats.min == 1
        assert result[0].roll_stats.max == 10
        assert result[0].roll_stats.avg == 6

        # 3k6
        assert result[1].dice_roll == SAMPLE_MULTIPLE_DICE_ROLLS[1]
        assert result[1].result == sum(SIMULATED_MULTIPLE_ROLLS[1:4])
        assert result[1].subsequent_rolls == SIMULATED_MULTIPLE_ROLLS[1:4]
        assert result[1].roll_stats.min == 3
        assert result[1].roll_stats.max == 18
        assert result[1].roll_stats.avg == 11

    @patch('dice_roller.dice.randint', Mock(side_effect=SIMULATED_MULTIPLE_ROLLS))
    def test_rolling_multiple_dices_with_addition(self):
        """Testing multiple dice rolls with addition and subtraction"""
        result = Roller(SAMPLE_MULTIPLE_DICE_ROLLS_WITH_ADDITION).roll()

        assert len(result) == len(SAMPLE_MULTIPLE_DICE_ROLLS_WITH_ADDITION)
        for roll in result:
            assert isinstance(roll, DiceRoll)

        # 2k20+16
        assert result[0].dice_roll == SAMPLE_MULTIPLE_DICE_ROLLS_WITH_ADDITION[0]
        assert result[0].result == sum(SIMULATED_MULTIPLE_ROLLS[:2]) + 16
        assert result[0].subsequent_rolls == SIMULATED_MULTIPLE_ROLLS[:2]
        assert result[0].roll_stats.min == 18
        assert result[0].roll_stats.max == 56
        assert result[0].roll_stats.avg == 37

        # 5k6+2
        assert result[1].dice_roll == SAMPLE_MULTIPLE_DICE_ROLLS_WITH_ADDITION[1]
        assert result[1].result == sum(SIMULATED_MULTIPLE_ROLLS[2:7]) + 2
        assert result[1].subsequent_rolls == SIMULATED_MULTIPLE_ROLLS[2:7]
        assert result[1].roll_stats.min == 7
        assert result[1].roll_stats.max == 32
        assert result[1].roll_stats.avg == 20

        # 3k4-2
        assert result[2].dice_roll == SAMPLE_MULTIPLE_DICE_ROLLS_WITH_ADDITION[2]
        assert result[2].result == sum(SIMULATED_MULTIPLE_ROLLS[7:10]) - 2
        assert result[2].subsequent_rolls == SIMULATED_MULTIPLE_ROLLS[7:10]
        assert result[2].roll_stats.min == 1
        assert result[2].roll_stats.max == 10
        assert result[2].roll_stats.avg == 6

    @patch(
        'dice_roller.roller.os.urandom', Mock(side_effect=NotImplementedError('Simulated error'))
    )
    @patch('dice_roller.roller.time', Mock(return_value=123))
    def test_class_initialization_with_broken_entropy(self, capsys):
        """Testing if Roller class will initialize without systems entropy"""
        warning_message = 'warning: os.urandom() not available, using time based seed. ' \
                          'Original message: Simulated error\n'
        result = Roller([SAMPLE_SINGLE_DICE_ROLL]).roll()

        assert len(result) == 1
        assert isinstance(result[0], DiceRoll)
        # the result of random.randint(1, 20) with random.seed(123) is 2
        assert result[0].result == 2
        assert capsys.readouterr().out == warning_message
