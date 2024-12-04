import pytest

from aoc_2024.day03 import day03


@pytest.fixture
def ex_raw_input_p1():
    input_ = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    expected = 161
    return input_, expected


@pytest.fixture
def ex_raw_input_p2():
    input_ = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    expected = 48
    return input_, expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = day03.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = day03.main_part2(input_)
    assert result == expected
