from pathlib import Path

import click

from ..core import get_input_file, read_file


def main_part1(data):
    """Solution to day 13 part 1"""


def main_part2(data):
    """Solution to day 13 part 2"""


@click.group
def cli():
    """Command Line Interface for day13"""


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part1(file):
    data = read_file(Path(file), as_str=True)
    print(main_part1(data))


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part2(file):
    data = read_file(Path(file), as_str=True)
    print(main_part2(data))
