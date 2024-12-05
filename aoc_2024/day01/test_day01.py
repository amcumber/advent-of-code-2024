import aoc_2024.day01.day01 as day01
import pytest


@pytest.fixture
def input_():
    return [
        "3   4",
        "4   3",
        "2   5",
        "1   3",
        "3   9",
        "3   3",
    ]


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 11
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 31
    return input_, expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = day01.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = day01.main_part2(input_)
    assert result == expected
