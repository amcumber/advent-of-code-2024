import pytest

from aoc_2024 import core
from aoc_2024.day09 import soln


@pytest.fixture
def input_():
    return "2333133121414131402\n"


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 1928
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 10000
    return input_, expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected
