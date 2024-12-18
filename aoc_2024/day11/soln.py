from collections import Counter
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


def blink_stones_p2(stone: int):
    if stone == 0:
        yield 1
    elif (n := len(str(stone))) % 2 == 0:
        new_stones = str(stone)[: n // 2], str(stone)[n // 2 :]
        for new_stone in new_stones:
            yield int(new_stone)
    else:
        yield stone * 2024


def main_part2(data, generations=75):
    """Solution to day 11 part 2"""
    stones = Counter([int(ele) for ele in data.strip().split()])
    for _ in range(generations):
        new_stones = Counter()
        for stone in stones:
            next_stones = Counter(list(blink_stones_p2(stone)))
            for next_ in next_stones:
                next_stones[next_] *= stones[stone]
            new_stones.update(next_stones)
        stones = new_stones
    return stones.total()


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
@click.option("-g", "--generations", default=75)
def part2(file, generations):
    data = read_file(Path(file), as_str=True)
    print(main_part2(data, generations))
