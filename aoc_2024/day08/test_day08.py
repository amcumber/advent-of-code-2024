import pytest

from aoc_2024.day08 import soln


@pytest.fixture
def ex_toy_input_p1():
    input_ = [
        "..........",
        "...#......",
        "..........",
        "....a.....",
        "..........",
        ".....a....",
        "..........",
        "......#...",
        "..........",
        "..........",
    ]
    expected = 2
    return input_, expected


@pytest.fixture
def ex_raw_input_p1():
    input_ = [
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
    expected = 14  # true matches = 14
    return input_, expected


@pytest.fixture
def ex_raw_input_p2():
    input_ = []
    expected = 0
    return input_, expected


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
