from collections import defaultdict, namedtuple
from itertools import product
from pathlib import Path

import click

from ..core import (
    get_coord_dims,
    get_input_file,
    parse_coords_except,
    read_file,
    GridElement,
)

SYMBOLS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
MT = "."


def inbounds(coord, maxes):
    return 0 <= coord.real < maxes[0] and 0 <= coord.imag < maxes[1]


def make_lib(ant_list: list[GridElement]):
    ant_lib = defaultdict(list)
    for ele in ant_list:
        if ele.sym not in SYMBOLS:
            continue
        ant_lib[ele.sym].append(ele)
    return ant_lib


def get_antinodes(data):
    ant_list = list(parse_coords_except(data, MT))
    ant_lib = make_lib(ant_list)
    dims = get_coord_dims(data)

    antinodes = set()
    for sym, ants in ant_lib.items():
        for first, second in product(ants, repeat=2):
            diff = second.pos - first.pos
            third = first.pos - diff
            if inbounds(third, dims):
                antinodes.add(third)
    return antinodes


def main_part1(data):
    """Solution to day 08 part 1"""
    antinodes = get_antinodes(data)
    return len(antinodes)


def main_part2(data):
    """Solution to day 08 part 2"""


@click.group
def cli():
    """Command Line Interface for day08"""


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
