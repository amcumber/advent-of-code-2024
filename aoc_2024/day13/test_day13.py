import pytest

from aoc_2024 import core
from aoc_2024.day13 import soln


@pytest.fixture
def ex_raw_input_p1():
    return


@pytest.fixture
def ex_raw_input_p2():
    return


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected
