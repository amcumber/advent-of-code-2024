import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import click

from ..core import get_input_file, read_file

FORWARD = "XMAS"


def find_hits_p1(data):

    hits = []
    for fun in (find_horiz, find_vert, find_sw_ne, find_nw_se):
        hits.extend([len(line) for line in fun(data)])
    return hits


def find_horiz(data, pat=FORWARD):
    backward = pat[::-1]
    hits = []
    for line in data:
        hits.append(list(re.finditer(pat, line)))
        hits.append(list(re.finditer(backward, line)))
    return hits


def find_sw_ne(data, pat=FORWARD):
    diag = diagnolize_sw_ne(data)
    return find_horiz(diag, pat=pat)


def find_nw_se(data, pat=FORWARD):
    diag = diagnolize_nw_se(data)
    return find_horiz(diag, pat=pat)


def find_vert(data):
    transposed = transpose(data)
    return find_horiz(transposed)


def transpose(data) -> list[str]:
    new_data = []
    first_line = data[0]
    for iCol in range(len(first_line)):
        col = []
        for line in data:
            col.append(line[iCol])
        new_data.append(col)
    return ["".join(line) for line in new_data]


def diagnolize_sw_ne(data) -> list[str]:
    """
    From
    ```
    00 01 02
    10 11 12
    20 21 22
    ```

    To
    ```
    0 00
    1 01 10
    2 02 11 20
    3 12 21
    4 22
    ```

    From
    ```
    00 01 02
    10 11 12
    ```

    To
    ```
    0 00
    1 01 10
    2 02 11
    3 12
    ```
    """

    new_data = []
    first_line = data[0]
    n_daigs = (n_row := len(data)) + (n_col := len(first_line)) - 1
    for idx in range(n_daigs):
        new_col = []
        if idx < n_row:
            for jdx in range(idx + 1):
                y = idx - jdx
                new_col.append(data[jdx][y])
        else:
            row_start = (idx + 1) % n_col
            # row_end = idx - row_start + 1
            for jdx in range(row_start, n_row):
                y = idx - jdx
                new_col.append(data[jdx][y])
        new_data.append(new_col)
    return ["".join(line) for line in new_data]


def flip_ud(data):
    new_data = []
    for line in reversed(data):
        new_data.append(line)
    return new_data


def flip_lr(data):
    new_data = []
    for line in data:
        new_data.append("".join(reversed(line)))
    return new_data


def diagnolize_nw_se(data) -> list[str]:
    new_data = flip_ud(data)
    new_data = diagnolize_sw_ne(new_data)
    return flip_lr(new_data)


def get_similarity(sw_hits, nw_hits):
    hits = []
    for sw_line, nw_line in zip(sw_hits, nw_hits):
        for sw_hit in sw_line:
            sw_span = sw_hit.span()
            sw_match = sw_hit.group()
            for nw_hit in nw_line:
                if sw_hit.span() != nw_hit.span():
                    continue
                hits.append((sw_hit, nw_hit))
    return hits


def find_x_mas(data, pattern):
    n_row = len(data)
    hits = 0
    for iRow, line in enumerate(data):
        n_col = len(line)
        for iCol, tl in enumerate(line):
            if tl != pattern["tl"]:
                continue
            if (iR := iCol + 2) >= n_col:
                continue
            if line[iR] != pattern["tr"]:
                continue
            if (iB := iRow + 2) >= n_row:
                continue
            if data[iRow + 1][iCol + 1] != pattern["m"]:
                continue
            if data[iB][iCol] != pattern["bl"]:
                continue
            if data[iB][iR] != pattern["br"]:
                continue
            hits += 1
    return hits


def find_mmass(data):

    pattern = {
        "tl": "M",
        "tr": "M",
        "m": "A",
        "bl": "S",
        "br": "S",
    }
    return find_x_mas(data, pattern)


def find_msams(data):

    pattern = {
        "tl": "M",
        "tr": "S",
        "m": "A",
        "bl": "M",
        "br": "S",
    }
    return find_x_mas(data, pattern)


def find_ssamm(data):

    pattern = {
        "tl": "S",
        "tr": "S",
        "m": "A",
        "bl": "M",
        "br": "M",
    }
    return find_x_mas(data, pattern)


def find_smasm(data):

    pattern = {
        "tl": "S",
        "tr": "M",
        "m": "A",
        "bl": "S",
        "br": "M",
    }
    return find_x_mas(data, pattern)


def find_hits_p2(data):
    hits = 0
    hits += find_mmass(data)
    hits += find_msams(data)
    hits += find_ssamm(data)
    hits += find_smasm(data)
    return hits


def main_part1(data):
    """Solution to day 04 part 1"""
    hits = find_hits_p1(data)
    return sum(hits)


def main_part2(data):
    """Solution to day 04 part 2"""
    return find_hits_p2(data)


@click.group
def cli():
    """Command Line Interface for day04"""


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
