from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from itertools import product

import click

from ..core import get_input_file, read_file


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def can_compute(line: str) -> int:
    OPERATORS = [add, mul]
    resultant, argument = line.split(":")
    resultant = int(resultant)
    args = [int(arg) for arg in argument.split()]
    for ops in product(OPERATORS, repeat=len(args) - 1):
        first = args[0]
        for idx, op in enumerate(ops):
            second = args[idx + 1]
            first = op(first, second)
        return resultant if first == resultant else 0


def main_part1(data):
    """Solution to day 06 part 1"""
    vals = [can_compute(line) for line in data]
    return sum(vals)


def main_part2(data):
    """Solution to day 06 part 2"""


@click.group
def cli():
    """Command Line Interface for day05"""


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part1(file):
    data = read_file(Path(file))
    print(main_part1(data))


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part2(file):
    data = read_file(Path(file))
    print(main_part2(data))
