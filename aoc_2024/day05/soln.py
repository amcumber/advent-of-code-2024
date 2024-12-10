from collections import defaultdict
from pathlib import Path

import click

from ..core import get_input_file, read_file

DIV = "|"
DELIM = ","


def create_rule_set(data):
    raw = [line for line in data if DIV in line]
    reverse = defaultdict(list)
    forward = defaultdict(list)
    for line in raw:
        before, after = map(int, line.split(DIV))
        reverse[after].append(before)
        forward[before].append(after)
    return forward, reverse


def create_instructions(data):
    raw = [line for line in data if line.strip() and DIV not in line]
    return [[int(ele) for ele in line.split(DELIM)] for line in raw]


def is_validate(instruction, no_left, no_right):
    right = instruction.copy()
    left = []
    for page in instruction:
        right.pop(0)
        left.append(page)
        if any(ele in right for ele in no_right[page]):
            return False
        if any(ele in no_left[page] for ele in left):
            return False
    return True


def get_middle(instruction):
    idx = len(instruction) // 2
    return instruction[idx]


def main_part1(data):
    """Solution to day 05 part 1"""
    rule_set = create_rule_set(data)
    instructions = create_instructions(data)
    valid_ = [inst for inst in instructions if is_validate(inst, *rule_set)]
    mids = [get_middle(inst) for inst in valid_]
    return sum(mids)


def is_next(page, instruction, no_right):
    not_page_inst = instruction.copy()
    not_page_inst.remove(page)
    for not_page in not_page_inst:
        if not_page in no_right[page]:
            return False
    return True


def validate(instruction, no_right):
    new_list = []
    while instruction:
        frozen_inst = instruction.copy()
        for page in frozen_inst:
            if is_next(page, instruction, no_right):
                new_list.append(page)
                instruction.remove(page)
                continue
    return new_list


def main_part2(data):
    """Solution to day 05 part 2"""
    rule_set = create_rule_set(data)
    _, no_right = rule_set
    instructions = create_instructions(data)
    invalid = [inst for inst in instructions if not is_validate(inst, *rule_set)]
    valid = [validate(inst, no_right) for inst in invalid]
    mids = [get_middle(inst) for inst in valid]
    return sum(mids)


@click.group
def cli():
    """Command Line Interface for day05"""


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
