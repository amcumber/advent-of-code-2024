import argparse
from itertools import zip_longest
from pathlib import Path

import click
from ..core import read_file, get_input_file


def get_lists(data):
    left = [int(line.split()[0]) for line in data]
    right = [int(line.split()[1]) for line in data]
    return left, right


def main_part1(data):
    """Solution to day 01 part 1"""
    left, right = get_lists(data)
    left.sort()
    right.sort()
    sum = 0
    for l, r in zip_longest(left, right):
        sum += abs(l - r)
    return sum


def main_part2(data):
    """Solution to day 01 part 2"""
    left, right = get_lists(data)
    prod = 0
    for ele in left:
        prod += ele * right.count(ele)
    return prod


@click.group
def cli():
    """Command Line Interface for day1"""


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
