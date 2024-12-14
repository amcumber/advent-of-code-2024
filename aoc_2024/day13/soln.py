from pathlib import Path

import click
import numpy as np

from ..core import get_input_file, read_file


def parse_blocks(data):
    block = []
    blocks = []
    for line in data:
        if line.startswith("Button"):
            block.append(line)
        if line.startswith("Prize"):
            block.append(line)
            blocks.append(block)
            block = []
    return blocks


def parse_equation_block(block):
    def parse_ab(line: str):
        assert line.startswith("Button")
        x, y = line.strip().split(":")[-1].split(",")
        x_val = int(x.strip().strip("X"))
        y_val = int(y.strip().strip("Y"))
        return [x_val, y_val]

    def parse_prize(line):
        assert line.startswith("Prize:")
        x, y = line.split(":")[-1].strip().split(",")
        x_val = int(x.split("=")[-1])
        y_val = int(y.split("=")[-1])
        return [x_val, y_val]

    assert len(block) == 3
    line_a, line_b, line_p = block
    aa = np.array([parse_ab(line_a), parse_ab(line_b)]).T
    bb = np.array(parse_prize(line_p))
    return aa, bb


def solve_eqn(eqn: tuple[np.ndarray, np.ndarray], accuracy: int = 2) -> int:
    result = np.linalg.solve(*eqn)
    if not all((rounded := result.round(accuracy)) % 1 == 0):
        return 0
    return np.sum(rounded * [3, 1]).tolist()


def main_part1(data):
    """Solution to day 13 part 1"""
    blocks = parse_blocks(data)
    eqns = [parse_equation_block(block) for block in blocks]
    solns = [solve_eqn(eqn) for eqn in eqns]
    return sum(solns)


def main_part2(data):
    """Solution to day 13 part 2"""
    ERR = 10_000_000_000_000
    err_arr = np.array([ERR, ERR])
    blocks = parse_blocks(data)
    eqns = [parse_equation_block(block) for block in blocks]
    eqns = [(a, b + err_arr) for a, b in eqns]
    solns = [solve_eqn(eqn) for eqn in eqns]
    return sum(solns)


@click.group
def cli():
    """Command Line Interface for day13"""


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
