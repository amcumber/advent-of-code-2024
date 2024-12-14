from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product, zip_longest
from pathlib import Path

import click

from ..core import get_input_file, read_file

BLANK = -1


def expand(data: str) -> list[int]:
    file_sizes = [int(ele) for ele in data.strip()[::2]]
    open_sizes = [int(ele) for ele in data.strip()[1::2]]
    expanded = []
    for file_id, (n_file, n_blank) in enumerate(zip_longest(file_sizes, open_sizes)):
        if n_file is not None:
            expanded.extend([file_id] * n_file)
        if n_blank is not None:
            expanded.extend([BLANK] * n_blank)
    return expanded


def defrag(expanded: list[int]) -> list[int]:
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
    return defragged


def checksum(defraged, stop_on_blank=True):
    check = 0
    for idx, file_num in enumerate(defraged):
        val = idx * int(file_num)
        if file_num == BLANK:
            if stop_on_blank:
                break
            val = 0
        check += val
    return check


def main_part1(data):
    """Solution to day 09 part 1"""
    expanded = expand(data)
    defragged = defrag(expanded)
    return checksum(defragged)


@dataclass
class FileBlock:
    file_id: int
    n: int


# FileBlock = namedtuple("FileBlock", ["file_id", "n", "idx"])


def convert_expanded(expanded) -> list[FileBlock]:
    files = []
    prev_id = expanded[0]
    n = 0
    for idx, file_id in enumerate(expanded):
        if file_id == prev_id:
            n += 1
            continue
        files.append(FileBlock(prev_id, n))
        prev_id = file_id
        n = 1
    files.append(FileBlock(file_id, n))
    return files


def defrag_p2(files: list[FileBlock]) -> list[int]:
    def _compress_mt(defragged, loc, n):
        prev_ = defragged[loc - 1]
        next_ = defragged[loc + 1]
        new_mt = defragged[loc]
        if next_.file_id == new_mt.file_id:
            new_mt.n += next_.n
            defragged.pop(loc + 1)
        if prev_.file_id == new_mt.file_id:
            new_mt.n += prev_.n
            defragged.pop(loc - 1)

    def _search(file, defragged):
        i_file = defragged.index(file)
        mts = [
            (idx, file)
            for idx, file in enumerate(defragged)
            if file.file_id == BLANK and idx < i_file
        ]
        for i_mt, mt in mts:
            if i_mt >= i_file:
                return
            if mt.n < file.n:
                continue
            if mt.n == file.n:
                defragged[i_file] = mt
                defragged[i_mt] = file
                _compress_mt(defragged, i_file, file.n)
                return
            remaining = FileBlock(BLANK, mt.n - file.n)
            displaced = FileBlock(BLANK, file.n)
            # update file and origin MT
            defragged[i_file] = displaced
            defragged[i_mt] = remaining
            # insert file
            defragged.insert(i_mt, file)
            _compress_mt(defragged, i_file, file.n)
            return

    defragged = list(files)
    for file in reversed(files):
        if file.file_id == BLANK:
            continue
        _search(file, defragged)
    return defragged


def convert_files(files: list[FileBlock]) -> list[int]:
    expanded = []
    for file in files:
        expanded += [file.file_id] * file.n
    return expanded


def main_part2(data):
    """Solution to day 09 part 2"""
    expanded = expand(data)
    files = convert_expanded(expanded)
    defragged = defrag_p2(files)
    defragged_list = convert_files(defragged)
    return checksum(defragged_list, False)


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
