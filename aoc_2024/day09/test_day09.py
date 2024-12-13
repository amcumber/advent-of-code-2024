import pytest

from aoc_2024 import core
from aoc_2024.day09 import soln


@pytest.fixture
def input_():
    return "2333133121414131402\n"


@pytest.fixture
def toy_input():
    input_ = "12345\n"
    expanded = "0..111....22222"
    defragged = "022111222......"
    checksum = 60
    return input_, expanded, defragged, checksum


@pytest.fixture
def ex_raw_input_expanded_p1(input_):
    expanded = "00...111...2...333.44.5555.6666.777.888899"
    defragged = "0099811188827773336446555566.............."
    checksum = 1928
    return input_, expanded, defragged, checksum


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 1928
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 10000
    return input_, expected


def test_expanded_toy(toy_input):
    input_, expected, *_ = toy_input
    result = soln.expand(input_)
    assert result == expected


def test_expanded_long(ex_raw_input_expanded_p1):
    input_, expected, *_ = ex_raw_input_expanded_p1
    result = soln.expand(input_)
    assert result == expected


def test_defrag_toy(toy_input):
    _, input_, expected, _ = toy_input
    result = soln.defrag(input_)
    assert result == expected


def test_defrag_long(ex_raw_input_expanded_p1):
    _, input_, expected, _ = ex_raw_input_expanded_p1
    result = soln.defrag(input_)
    assert result == expected


def test_checksum_toy(toy_input):
    *_, input_, expected = toy_input
    result = soln.checksum(input_)
    assert result == expected


def test_checksum_long(ex_raw_input_expanded_p1):
    *_, input_, expected = ex_raw_input_expanded_p1
    result = soln.checksum(input_)
    assert result == expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected
