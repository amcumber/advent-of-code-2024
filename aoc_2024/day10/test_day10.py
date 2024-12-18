import pytest

from aoc_2024 import core
from aoc_2024.day08 import soln


@pytest.fixture
def toy_input():
    return [
        "0123\n",
        "1234\n",
        "8765\n",
        "9876\n",
    ]


@pytest.fixture
def ex_toy_input_p1(toy_input):
    expected = 1
    return toy_input, expected


@pytest.fixture
def input_():
    return [
        "89010123\n",
        "78121874\n",
        "87430965\n",
        "96549874\n",
        "45678903\n",
        "32019012\n",
        "01329801\n",
        "10456732\n",
    ]


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 36
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 34
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
