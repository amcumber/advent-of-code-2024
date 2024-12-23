import pytest

from aoc_2024 import core
from aoc_2024.day11 import soln


@pytest.fixture
def ex_input_p1():
    return [
        "125 17\n",
        "253000 1 7\n",
        "253 0 2024 14168\n",
        "512072 1 20 24 28676032\n",
        "512 72 2024 2 0 2 4 2867 6032\n",
        "1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32\n",
        "2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2\n",
    ]


def test_main_part1(ex_input_p1):
    input_, *_, expected = ex_input_p1
    expected = soln.to_list(expected)
    result = soln.main_part1(input_, generations=6)
    assert result == len(expected)


def test_main_part2(ex_input_p1):
    input_, *_, exp = ex_input_p1
    expected = len(exp.strip().split())
    result = soln.main_part2(input_, generations=6)
    assert result == expected
