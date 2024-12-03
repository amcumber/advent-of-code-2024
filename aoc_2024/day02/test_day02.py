import pytest

from aoc_2024.day02 import day02


@pytest.fixture
def input_():
    return [
        "7 6 4 2 1",
        "1 2 7 8 9",
        "9 7 6 2 1",
        "1 3 2 4 5",
        "8 6 4 4 1",
        "1 3 6 7 9",
    ]


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 2
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 4
    return input_, expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = day02.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = day02.main_part2(input_)
    assert result == expected
