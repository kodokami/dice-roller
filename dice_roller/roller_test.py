"""
Roller tests

Copyright (C) 2023 _kodokami
"""
from unittest.mock import Mock, patch

from dice_roller import Roller, DiceRoll


@patch("dice_roller.dice.randint")
class TestRoller:
    def test_single_dice_roll(self, mocked_randint: Mock):
        """Testing single dice roll with Roller class"""
        sample_dice_roll = '1k20'
        simulated_roll_value = 3
        mocked_randint.return_value = simulated_roll_value

        result = Roller([sample_dice_roll]).roll()

        assert len(result) == 1
        assert isinstance(result[0], DiceRoll)
        assert result[0].dice_roll == sample_dice_roll
        assert result[0].result == simulated_roll_value
        assert result[0].subsequent_rolls == [simulated_roll_value]

    def test_rolling_multiple_dices(self, mocked_randint: Mock):
        """Testing multiple dice rolls"""
        sample_dice_rolls = ['1k10', '3k6']
        simulated_rolls = [8, 3, 5, 4]
        mocked_randint.side_effect = simulated_rolls

        result = Roller(sample_dice_rolls).roll()

        assert len(result) == len(sample_dice_rolls)
        for roll in result:
            assert isinstance(roll, DiceRoll)

        assert result[0].dice_roll == sample_dice_rolls[0]
        assert result[0].result == 8
        assert result[0].subsequent_rolls == simulated_rolls[:1]

        assert result[1].dice_roll == sample_dice_rolls[1]
        assert result[1].result == sum(simulated_rolls[1:4])
        assert result[1].subsequent_rolls == simulated_rolls[1:4]
