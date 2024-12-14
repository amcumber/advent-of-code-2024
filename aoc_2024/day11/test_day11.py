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


def to_list(stringy):
    listy = []
    for ele in stringy:
        if ele != ".":
            listy.append(int(ele))
        else:
            listy.append(soln.BLANK)

    return listy


@pytest.fixture
def toy_input():
    b = soln.BLANK
    input_ = "12345\n"
    expanded = to_list("0..111....22222")
    defragged = to_list("022111222......")
    checksum = 60
    file_expanded = [
        soln.FileBlock(*x)
        for x in (
            (0, 1),
            (b, 2),
            (1, 3),
            (b, 4),
            (2, 5),
        )
    ]
    return input_, expanded, defragged, checksum, file_expanded


@pytest.fixture
def ex_input(input_):
    b = soln.BLANK
    expanded = to_list("00...111...2...333.44.5555.6666.777.888899")
    defragged_p1 = to_list("0099811188827773336446555566..............")
    checksum = 1928
    file_expanded = [
        soln.FileBlock(*x)
        for x in (
            (0, 2),
            (b, 3),
            (1, 3),
            (b, 3),
            (2, 1),
            (b, 3),
            (3, 3),
            (b, 1),
            (4, 2),
            (b, 1),
            (5, 4),
            (b, 1),
            (6, 4),
            (b, 1),
            (7, 3),
            (b, 1),
            (8, 4),
            (9, 2),
        )
    ]
    return input_, expanded, defragged_p1, checksum, file_expanded


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 1928
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 2858
    return input_, expected


def test_expanded_toy(toy_input):
    input_, expected, *_ = toy_input
    result = soln.expand(input_)
    assert result == expected


def test_expanded_long(ex_input):
    input_, expected, *_ = ex_input
    result = soln.expand(input_)
    assert result == expected


def test_defrag_toy(toy_input):
    _, input_, expected, *_ = toy_input
    result = soln.defrag(input_)
    assert result == expected


def test_defrag_long(ex_input):
    _, input_, expected, *_ = ex_input
    result = soln.defrag(input_)
    assert result == expected


def test_checksum_toy(toy_input):
    *_, input_, expected, _ = toy_input
    result = soln.checksum(input_)
    assert result == expected


def test_checksum_long(ex_input):
    *_, input_, expected, _ = ex_input
    result = soln.checksum(input_)
    assert result == expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_convert_expanded_toy(toy_input):
    _, expanded, *_, file_expanded = toy_input
    results = soln.convert_expanded(expanded)
    assert results == file_expanded


def test_convert_expanded_long(ex_input):
    _, expanded, *_, file_expanded = ex_input
    results = soln.convert_expanded(expanded)
    assert results == file_expanded


@pytest.fixture
def part2_toy():
    return to_list("00...111...2...333.44.5555.6666.777.888899")


@pytest.fixture
def part2_files():
    b = soln.BLANK
    return [
        soln.FileBlock(*x)
        for x in [
            (0, 2),
            (b, 3),
            (1, 3),
            (b, 3),
            (2, 1),
            (b, 3),
            (3, 3),
            (b, 1),
            (4, 2),
            (b, 1),
            (5, 4),
            (b, 1),
            (6, 4),
            (b, 1),
            (7, 3),
            (b, 1),
            (8, 4),
            (9, 2),
        ]
    ]


@pytest.fixture
def part2_defragged():
    return to_list("00992111777.44.333....5555.6666.....8888..")


@pytest.fixture
def part2_defrag_files():
    b = soln.BLANK
    return [
        soln.FileBlock(*x)
        for x in [
            (0, 2),
            (9, 2),
            (2, 1),
            (1, 3),
            (7, 3),
            (b, 1),
            (4, 2),
            (b, 1),
            (3, 3),
            (b, 4),
            (5, 4),
            (b, 1),
            (6, 4),
            (b, 5),
            (8, 4),
            (b, 2),
        ]
    ]


@pytest.fixture
def ex_files(part2_toy, part2_files, part2_defragged, part2_defrag_files):
    return part2_toy, part2_files, part2_defragged, part2_defrag_files


def test_convert_files(ex_files):
    expected, files, defragged, def_files = ex_files
    result = soln.convert_files(files)
    assert result == expected

    expected = defragged
    result = soln.convert_files(def_files)
    assert result == expected


def test_main_part2_convert(ex_files, ex_raw_input_p2):
    _, checksum = ex_raw_input_p2
    expanded, files, defragged, def_files = ex_files
    r_files = soln.convert_expanded(expanded)
    assert files == r_files


def test_main_part2_convert_defrag(ex_files, ex_raw_input_p2):
    _, checksum = ex_raw_input_p2
    expanded, files, defragged, def_files = ex_files
    first_soln = soln.convert_files(def_files)
    assert first_soln == defragged

    r_files = soln.convert_expanded(expanded)

    r_def_files = soln.defrag_p2(r_files)

    r_defragged = soln.convert_files(r_def_files)
    assert r_defragged == defragged


def test_main_part2_pipeline(ex_files, ex_raw_input_p2):
    _, checksum = ex_raw_input_p2
    expanded, files, defragged, def_files = ex_files
    r_files = soln.convert_expanded(expanded)

    r_def_files = soln.defrag_p2(r_files)

    r_defragged = soln.convert_files(r_def_files)

    r_check = soln.checksum(r_defragged, False)
    assert r_check == checksum


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected
