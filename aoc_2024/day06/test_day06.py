import pytest

from aoc_2024.day06 import soln


@pytest.fixture
def input_():
    return [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#..^.....",
        "........#.",
        "#.........",
        "......#...",
    ]


@pytest.fixture
def ex_raw_input_p1(input_):
    expected = 41
    return input_, expected


@pytest.fixture
def ex_raw_input_p2(input_):
    expected = 6
    return input_, expected


@pytest.fixture
def expected_cands():
    return set(
        (
            6 + 3j,
            7 + 6j,
            8 + 1j,
            9 + 7j,
            7 + 7j,
            8 + 3j,
        )
    )


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_find_loops(input_, expected_cands):
    agent = soln.get_agent(input_)
    walls = soln.get_walls(input_)
    maxes = soln.get_coord_dims(input_)
    agent_history, _ = soln.walk_agent(agent, walls, dims=maxes)
    candidates = [agent.pos for agent in agent_history]
    result = soln.find_loops(agent, walls, candidates, maxes)
    assert result == expected_cands


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected
