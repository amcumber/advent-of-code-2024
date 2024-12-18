from collections import defaultdict
from itertools import product
from pathlib import Path

import click

from ..core import (
    GridElement,
    get_coord_dims,
    get_input_file,
    inbounds,
    parse_coords_all,
    parse_coords_except,
    read_file,
)

UP = 1 + 0j
TURN = -1j


def get_grid(data):
    grid = defaultdict(list)
    for ele in parse_coords_all(data):
        grid[int(ele.sym)] += [ele.pos]
    return grid


def adjacent(last, next_):
    return next_ in [last + UP * TURN**idx for idx in range(4)]


def find_next(pos, next_nums):
    return [nn for nn in next_nums if adjacent(pos, nn)]


def find_trails(zero, grid):
    last_nums = [zero]

    for nns in range(1, 10):
        adj_nums = []
        for l_num in last_nums:
            adj_nums.append(find_next(l_num, nns))
        if not adj_nums:
            return 0
        adj_numsj = set(adj_nums)
    return len(adj_nums)


def main_part1(data):
    """Solution to day 10 part 1"""
    grid = get_grid(data)
    zeros = grid[0]
    n_trails = 0
    for zero in zeros:
        n_trails += find_trails(zero)
    return n_trails


def main_part2(data):
    """Solution to day 10 part 2"""


@click.group
def cli():
    """Command Line Interface for day10"""


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
