import pytest

from aoc_2024.day06 import soln


@pytest.fixture
def input_():
    return [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#..^.....",
        "........#.",
        "#.........",
        "......#...",
    ]


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 41
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 123
    return input_, expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected
