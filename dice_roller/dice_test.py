"""
Dice tests

Copyright (C) 2023 _kodokami
"""
import pytest

from dice_roller import Dice


class TestDice:
    @pytest.mark.parametrize(
        'dice_sides',
        (4, 6, 8, 10, 12, 20),
        ids=[
            'dice_sides=4', 'dice_sides=6', 'dice_sides=8',
            'dice_sides=10', 'dice_sides=12', 'dice_sides=20'
        ]
    )
    def test_dice_roll(self, dice_sides: int):
        """Simple dice rolling test"""
        dice = Dice(dice_sides)
        roll = dice.roll()

        assert roll >= 1
        assert roll <= dice_sides

    @pytest.mark.parametrize(
        'dice_sides',
        [0, 1],
        ids=['dice_sides=0', 'dice_sides=1']
    )
    def test_invalid_sides_count(self, dice_sides: int):
        """Checking dice validation"""
        with pytest.raises(ValueError):
            Dice(dice_sides)
