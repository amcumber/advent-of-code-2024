from collections import defaultdict, namedtuple
from itertools import product, zip_longest
from pathlib import Path

import click

from ..core import get_input_file, read_file

BLANK = "."


def expand(data) -> str:
    file_sizes = [int(ele) for ele in data.strip()[::2]]
    open_sizes = [int(ele) for ele in data.strip()[1::2]]
    expanded = []
    for file_id, (n_file, n_blank) in enumerate(zip_longest(file_sizes, open_sizes)):
        if n_file is not None:
            expanded.extend([str(file_id)] * n_file)
        if n_blank is not None:
            expanded.extend([BLANK] * n_blank)
    return "".join(expanded)


def defrag(expanded):
    defragged = list(expanded)
    max_n = len(defragged)
    for rev_id, ele in enumerate(reversed(expanded)):
        max_id = max_n - rev_id
        if ele == BLANK:
            continue
        if (idx := defragged.index(BLANK)) >= max_id:
            break
        defragged[idx] = ele
        defragged[max_id - 1] = BLANK
    return "".join(defragged)


def checksum(defraged):
    check = 0
    for idx, file_num in enumerate(defraged):
        if file_num == BLANK:
            break
        check += idx * int(file_num)
    return check


def main_part1(data):
    """Solution to day 09 part 1"""
    expanded = expand(data)
    defraged = defrag(expanded)
    return checksum(defraged)


def main_part2(data):
    """Solution to day 09 part 2"""


@click.group
def cli():
    """Command Line Interface for day09"""


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
