from pathlib import Path
import re

import click
from ..core import read_file, get_input_file


def main_part1(data):
    """Solution to day 03 part 1"""
    pat = re.compile(r"mul[(](\d{1,3}),(\d{1,3})[)]")
    result = [int(m.group(1)) * int(m.group(2)) for m in pat.finditer(data)]
    return sum(result)


def main_part2(data):
    """Solution to day 03 part 2"""
    data = data.replace("\n", " ")
    gates = re.compile(r"(?=do\(\)|^).*?(?=don\'t\(\)|$)")
    pat = re.compile(r"mul[(](\d{1,3}),(\d{1,3})[)]")
    matches = [m.group() for m in gates.finditer(data)]
    result = []
    for sub in matches:
        r = [int(m.group(1)) * int(m.group(2)) for m in pat.finditer(sub)]
        result.extend(r)
    return sum(result)


@click.group
def cli():
    """Command Line Interface for day3"""


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
