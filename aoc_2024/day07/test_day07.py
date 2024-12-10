import pytest

from aoc_2024.day07 import soln


@pytest.fixture
def ex_raw_input_p1():
    input_ = [
        "190: 10 19",
        "3267: 81 40 27",
        "83: 17 5",
        "156: 15 6",
        "7290: 6 8 6 15",
        "161011: 16 10 13",
        "192: 17 8 14",
        "21037: 9 7 18 13",
        "292: 11 6 16 20",
    ]
    expected = 3749
    return input_, expected


@pytest.fixture
def ex_raw_input_p2():
    input_ = [
        "156: 15 6",
        "7290: 6 8 6 15",
        "192: 17 8 14",
        "190: 10 19",
        "3267: 81 40 27",
        "292: 11 6 16 20",
    ]
    expected = 11387
    return input_, expected


@pytest.mark.parametrize(
    ["line", "expected"],
    [
        ("190: 10 19", 190),
        ("3267: 81 40 27", 3267),
        ("83: 17 5", 0),
        ("292: 11 6 16 20", 292),
    ],
)
def test_compute(line, expected):
    result = soln.compute(line)
    assert result == expected


@pytest.mark.parametrize(
    ["line", "expected"],
    [
        ("156: 15 6", 156),
        ("7290: 6 8 6 15", 7290),
        ("192: 17 8 14", 192),
        ("190: 10 19", 190),
        ("3267: 81 40 27", 3267),
        ("83: 17 5", 0),
        ("292: 11 6 16 20", 292),
    ],
)
def test_compute_p2(line, expected):
    result = soln.compute_p2(line)
    assert result == expected


@pytest.mark.parametrize(
    ["args", "expected"],
    [
        ((2, 3), 23),
        ((8, 10), 810),
    ],
)
def test_concat(args, expected):
    result = soln.concat(*args)
    assert result == expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected
