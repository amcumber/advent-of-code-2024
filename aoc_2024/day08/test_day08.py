import pytest

from aoc_2024 import core
from aoc_2024.day08 import soln


@pytest.fixture
def toy_input():
    return [
        "..........",
        "..........",
        "..........",
        "....a.....",
        "..........",
        ".....a....",
        "..........",
        "..........",
        "..........",
        "..........",
    ]


@pytest.fixture
def tee_input():
    return [
        "T.........",
        "...T......",
        ".T........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
    ]


@pytest.fixture
def ex_toy_input_p1(toy_input):
    expected = 2
    return toy_input, expected


@pytest.fixture
def input_():
    return [
        "............",
        "........0...",
        ".....0......",
        ".......0....",
        "....0.......",
        "......A.....",
        "............",
        "............",
        "........A...",
        ".........A..",
        "............",
        "............",
    ]


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 14  # true matches = 14
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 34
    return input_, expected


def test_get_antinodes(toy_input):
    expected = set([1 + 3j, 7 + 6j])
    result = soln.get_antinodes(toy_input)
    assert result == expected


def test_main_part1_toy(ex_toy_input_p1):
    input_, expected = ex_toy_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected


def test_get_antinodes_p2(tee_input):
    grid = [
        "#....#....",
        "...#......",
        ".#....#...",
        ".........#",
        "..#.......",
        "..........",
        "...#......",
        "..........",
        "....#.....",
        "..........",
    ]
    expected = set(coord.pos for coord in core.parse_coords(grid, "#"))
    result = soln.get_antinodes(tee_input, rng=range(0, 15))
    assert result == expected


def test_get_antinodes_large_p2(input_):
    grid = [
        "##....#....#",
        ".#.#....#...",
        "..#.##....#.",
        "..##...#....",
        "....#....#..",
        ".#...##....#",
        "...#..#.....",
        "#....#.#....",
        "..#.....#...",
        "....#....#..",
        ".#........#.",
        "...#......##",
    ]
    expected = set(coord.pos for coord in core.parse_coords(grid, "#"))
    result = soln.get_antinodes(input_, rng=range(0, 15))
    assert result == expected
