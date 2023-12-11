"""
dice-roller

Copyright (C) 2023 _kodokami
"""
import sys
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
from typing import List

from . import (
    __version__ as VERSION,
    COMMAND_NAME,
    DESCRIPTION,
    COPYRIGHT,
    Roller,
    DiceRoll
)
from .roller import ROLL_PATTERN

COMMON_ERROR_CODE = 1
SIGINT_ERROR_CODE = 130


def _roll(value: str) -> str:
    match = ROLL_PATTERN.match(value)
    if match is None:
        raise ArgumentTypeError('Invalid dice roll pattern')
    return value


def _commandmaker():
    """Console command arguments parser"""
    command = ArgumentParser(
        prog=COMMAND_NAME,
        description=DESCRIPTION,
        epilog=COPYRIGHT,
        add_help=False,
        formatter_class=RawTextHelpFormatter
    )

    roll = command.add_argument_group('rolling options')
    roll.add_argument(
        'rolls', action='store', nargs='+', type=_roll,
        help='dice roll to be made, accepted patterns are:'
             '\n\t- NdM+|-X - where N represents the number of rolls, M the number of dice sides ' \
             'and X is the natural number to add | subtract from the throw result, eg. 1d20+5'
             '\n\t- NkM+|-X - N, M and X like above, eg. 1k12-2',
        metavar='ROLL'
    )
    roll.add_argument(
        '-s', '--show-rolls', action='store_true', help='shows subsequence rolls'
    )
    roll.add_argument(
        '-S', '--show-statistics', action='store_true',
        help='shows roll statistics like minimal, maximum and average possible throw results'
    )

    other = command.add_argument_group('other')
    other.add_argument(
        '-h', '--help', action='help', help='print this help message and exit'
    )
    other.add_argument(
        '-V', '--version', action='version', version=f'{COMMAND_NAME} v{VERSION}',
        help='print program version and exit'
    )

    return command.parse_args()


def _print_results(executed_rolls: List[DiceRoll], show_rolls: bool, show_stats: bool):
    for index, roll in enumerate(executed_rolls):
        print(f'{roll.dice_roll} - {roll.result}', end=" " if show_rolls else "\n")
        if show_rolls:
            rolls = str(roll.subsequent_rolls).strip('[]')
            print(f'| Rolls: {rolls}')
        if show_stats:
            stats_msg = (
                f'[MIN: {roll.roll_stats.min}, '
                f'MAX: {roll.roll_stats.max}, '
                f'AVG: {roll.roll_stats.avg}]'
            )
            if index == len(executed_rolls) - 1 \
                or roll.dice_roll != executed_rolls[index + 1].dice_roll:
                print(stats_msg)


def execute():
    """Main execution function"""
    try:
        args = _commandmaker()
        _print_results(
            executed_rolls=Roller(args.rolls).roll(),
            show_rolls=args.show_rolls,
            show_stats=args.show_statistics
        )

    except KeyboardInterrupt:
        sys.exit(SIGINT_ERROR_CODE)

    except (OSError, SystemError):
        sys.exit(COMMON_ERROR_CODE)


if __name__ == '__main__':
    execute()
