import argparse
from itertools import zip_longest
from pathlib import Path


def main(data):
    """Solution to day 01 part 1"""
    parsed = [(float(x) for x in line.split()) for line in data]
    left, right = zip(*parsed)
    left = list(left)
    right = list(right)
    left.sort()
    right.sort()
    sum = 0
    for l, r in zip_longest(left, right):
        sum += abs(l - r)
    return sum


def read_file(file: Path):
    with file.open("r") as fh:
        return fh.readlines()


def api():
    root = ...
    default_file = root / "usr/day01/input.txt"
    parser = argparse.ArgumentParser("Day 01 Part 1")
    parser.add_argument("-f", "--file", default=default_file, help="input file")
    args = parser.parse_args()
    data = read_file(Path(args.file))
    print(main(data))


if "__main__" == __name__:
    api()
