import pytest
from aoc_2024.day04 import soln


@pytest.fixture
def ex_transpose():
    input_ = [
        "123",
        "456",
        "789",
    ]
    expected = [
        "147",
        "258",
        "369",
    ]
    return input_, expected


@pytest.fixture
def ex_diag_sw_ne():
    input_ = [
        "123",
        "456",
        "789",
    ]
    expected = [
        "1",
        "24",
        "357",
        "68",
        "9",
    ]
    return input_, expected


@pytest.fixture
def ex_diag_sw_ne_unsquare():
    input_ = [
        "123",
        "456",
    ]
    expected = [
        "1",
        "24",
        "35",
        "6",
    ]
    return input_, expected


@pytest.fixture
def ex_diag_nw_se():
    input_ = [
        "123",
        "456",
        "789",
    ]
    expected = [
        "7",
        "48",
        "159",
        "26",
        "3",
    ]
    return input_, expected


@pytest.fixture
def ex_raw_input_p1():
    input_ = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX",
    ]
    expected = 18
    return input_, expected


@pytest.fixture
def ex_raw_input_p2():
    input_ = [
        ".M.S......",
        "..A..MSMS.",
        ".M.S.MAA..",
        "..A.ASMSM.",
        ".M.S.M....",
        "..........",
        "S.S.S.S.S.",
        ".A.A.A.A..",
        "M.M.M.M.M.",
        "..........",
    ]
    expected = 9
    return input_, expected


def test_transpose(ex_transpose):
    input_, expected = ex_transpose
    result = soln.transpose(input_)
    assert result == expected


def test_diag_sw_ne_unsquare(ex_diag_sw_ne_unsquare):
    input_, expected = ex_diag_sw_ne_unsquare
    result = soln.diagnolize_sw_ne(input_)
    assert result == expected


def test_diag_sw_ne(ex_diag_sw_ne):
    input_, expected = ex_diag_sw_ne
    result = soln.diagnolize_sw_ne(input_)
    assert result == expected


def test_diag_nw_sw(ex_diag_nw_se):
    input_, expected = ex_diag_nw_se
    result = soln.diagnolize_nw_se(input_)
    assert result == expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected
