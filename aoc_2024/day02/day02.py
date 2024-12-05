from pathlib import Path

import click

from ..core import get_input_file, read_file


def is_ascending(seq: list[int]):
    last_ele = None
    for ele in seq:
        if last_ele is None:
            last_ele = ele
            continue
        if ele < last_ele:
            return False
        last_ele = ele
    return True


def is_descending(seq: list[int]):
    last_ele = None
    for ele in seq:
        if last_ele is None:
            last_ele = ele
            continue
        if ele > last_ele:
            return False
        last_ele = ele
    return True


def is_close(seq: list[int], min_val=1, max_val=3):
    last_ele = None
    for ele in seq:
        if last_ele is None:
            last_ele = ele
            continue
        diff = abs(ele - last_ele)
        if diff > max_val or diff < min_val:
            return False
        last_ele = ele
    return True


def is_safe(seq: list[int]):
    return (is_ascending(seq) or is_descending(seq)) and is_close(seq)


def parse_data(data):
    return [[int(ele) for ele in line.split()] for line in data]


def main_part1(data):
    """Solution to day 02 part 1"""
    lines = parse_data(data)
    safe_lines = [line for line in lines if is_safe(line)]
    return len(safe_lines)


def is_tolerant(seq: list[int]) -> bool:
    for idx in range(len(seq)):
        new_line = seq.copy()
        new_line.pop(idx)
        if is_safe(new_line):
            return True
    return False


def main_part2(data):
    """Solution to day 02 part 2"""
    is_safe = lambda x: (is_ascending(x) or is_descending(x)) and is_close(x)
    lines = parse_data(data)
    safe_lines = [line for line in lines if is_safe(line)]
    unsafe_lines = [line for line in lines if not is_safe(line)]
    new_safe_lines = [line for line in unsafe_lines if is_tolerant(line)]

    return len(safe_lines) + len(new_safe_lines)


@click.group
def cli():
    """Command Line Interface for day2"""


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
