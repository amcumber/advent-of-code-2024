from functools import cache
from pathlib import Path

import click

from ..core import get_input_file, read_file


def to_list(data):
    return [int(ele) for ele in data.strip().split()]


@cache
def apply_rules(stone: int) -> list[int]:
    YEAR = 2024
    if stone == 0:
        return [1]
    if (n := len(s_stone := str(stone))) % 2 == 0:
        n2 = n // 2
        # added backwards
        return [int(s_stone[n2:]), int(s_stone[:n2])]
    return [stone * YEAR]


def blink(stones):
    for istone in reversed(range(len(stones))):
        stone = stones[istone]
        new_stones = apply_rules(stone)
        stones[istone] = new_stones[0]
        if len(new_stones) > 1:
            for i_new_stone in range(1, len(new_stones)):
                stones.insert(istone, new_stones[i_new_stone])
    return stones


def main_part1(data, generations=25):
    """Solution to day 11 part 1"""
    stones = to_list(data)
    for _ in range(generations):
        stones = blink(stones)
    return len(stones)


def main_part2(data, generations=75):
    """Solution to day 11 part 2"""
    stones = to_list(data)
    n_stones = 0
    gen = generations
    while True:
        out_stones = pop_stones(stones)
        n_stones += count_stones(out_stones, gen)
        if len(stones) == 0:
            break
        gen -= 1
        stones = blink(stones)
        if gen <= 0:
            break
    return n_stones + len(stones)


@click.group
def cli():
    """Command Line Interface for day11"""


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
