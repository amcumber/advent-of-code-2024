from collections import defaultdict, namedtuple
from pathlib import Path
from typing import NamedTuple

import click

from ..core import get_coord_dims, get_input_file, parse_coords_except, read_file

# AntennaType = tuple[int, int, str]
AntennaType = tuple[complex, str]
MatchType = tuple[AntennaType, AntennaType, AntennaType]
MatchListType = list[MatchType]
# CoordType = tuple[int, int]
Antenna = namedtuple("Antenna", ["pos", "sym"])

AntennaListType = list[Antenna]
SYMBOLS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
MT = "."


# def _get_count(match_: MatchType, symb: str, cnt: int):
#     symbs = [ele[ISYMB] for ele in match_]
#     return len(symbs) >= cnt


def inbounds(coord, maxes):
    return 0 <= coord.real < maxes[0] and 0 <= coord.imag < maxes[1]


def find(coord: complex, ant_list: AntennaListType, maxes: tuple[int, int]):
    if not inbounds(coord, maxes):
        return None
    for ant in ant_list:
        if ant.pos == coord:
            return ant
    return None


def flatten_ant_lib(ant_lib):
    ants = []
    for coords in ant_lib.values():
        ants.extend(coords)
    return ants


def is_match_in(ant_match: MatchType, matches: MatchListType):
    ant_pos = [ant.pos for ant in ant_match]
    for prev_match in matches:
        match_pos = [ant.pos for ant in prev_match]
        if all(pos in match_pos for pos in ant_pos):
            return True
    return False


def make_lib(ant_list: AntennaListType):
    ant_lib = defaultdict(list)
    for pos, sym in ant_list:
        if sym not in SYMBOLS:
            continue
        ant_lib[sym].append(Antenna(pos, sym))
    return ant_lib


def main_part1(data):
    """Solution to day 08 part 1"""
    ant_list = [Antenna(*ant) for ant in parse_coords_except(data, MT)]
    ant_lib = make_lib(ant_list)
    dims = get_coord_dims(data)

    matches = set()
    for sym, ants in ant_lib.items():
        # breakpoint()
        for i in range(len(ants)):
            for j in range(i):
                first = ants[i]
                second = ants[j]
                diff = second.pos - first.pos
                minus = first.pos - diff
                plus = second.pos + diff
                # if third := find(minus, ant_list, dims):
                #     new_match = (third, first, second)
                #     if not is_match_in(new_match, matches):
                #         matches.append(new_match)
                if inbounds(minus, dims):
                    matches.add(minus)
                if inbounds(plus, dims):
                    matches.add(plus)

    return len(matches)


def main_part2(data):
    """Solution to day 08 part 2"""


@click.group
def cli():
    """Command Line Interface for day08"""


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part1(file):
    breakpoint()
    data = read_file(Path(file))
    print(main_part1(data))


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part2(file):
    data = read_file(Path(file))
    print(main_part2(data))
