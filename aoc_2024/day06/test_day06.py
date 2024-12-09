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


@pytest.mark.parametrize(
    ["agent", "walls", "expected"],
    [
        ((0, 0), [(0, 5), (0, 1), (1, 5)], [(0, 5), (0, 1)]),
        ((1, 0), [(0, 5), (0, 1), (1, 5)], [(1, 5)]),
    ],
)
def test_get_walls_row(agent, walls, expected):
    agent = soln.Agent(soln.Point(*agent), ">")
    walls = [soln.Point(*wall) for wall in walls]
    expected = [soln.Point(*wall) for wall in expected]
    results = soln.get_walls_row(agent, walls)
    assert len(results) == len(expected)
    for r, e in zip(results, expected):
        assert (r.x, r.y) == (e.x, e.y)


@pytest.mark.parametrize(
    ["agent", "walls", "expected"],
    [
        ((0, 0), [(5, 0), (1, 0), (5, 1)], [(5, 0), (1, 0)]),
        ((0, 1), [(5, 0), (1, 0), (5, 1)], [(5, 1)]),
    ],
)
def test_get_walls_col(agent, walls, expected):
    agent = soln.Agent(soln.Point(*agent), soln.Face.right)
    walls = [soln.Point(*wall) for wall in walls]
    expected = [soln.Point(*wall) for wall in expected]
    results = soln.get_walls_col(agent, walls)
    assert len(results) == len(expected)
    for r, e in zip(results, expected):
        assert (r.x, r.y) == (e.x, e.y)


@pytest.mark.parametrize(
    ["agent", "walls", "expected"],
    [
        ((0, 0), [(0, 5)], (0, 4)),
        ((0, 2), [(0, 1)], (0, 10)),
        ((0, 2), [(0, 8), (0, 5)], (0, 4)),
    ],
)
def test_walk_right(agent, walls, expected):
    agent = soln.Agent(soln.Point(*agent), soln.Face.right)
    walls = [soln.Point(*wall) for wall in walls]
    results = soln.walk_right(agent, walls, max_y=10)
    assert (results.x, results.y) == expected


@pytest.mark.parametrize(
    ["agent", "walls", "expected"],
    [
        ((0, 5), [(0, 0)], (0, 1)),
        ((0, 5), [(0, 6)], (0, 0)),
        ((0, 7), [(0, 2), (0, 5)], (0, 6)),
    ],
)
def test_walk_left(agent, walls, expected):
    agent = soln.Agent(soln.Point(*agent), soln.Face.left)
    walls = [soln.Point(*wall) for wall in walls]
    results = soln.walk_left(agent, walls)
    assert (results.x, results.y) == expected


@pytest.mark.parametrize(
    ["agent", "walls", "expected"],
    [
        ((5, 0), [(0, 0)], (1, 0)),
        ((5, 0), [(6, 0)], (0, 0)),
        ((7, 0), [(2, 0), (5, 0)], (6, 0)),
    ],
)
def test_walk_up(agent, walls, expected):
    agent = soln.Agent(soln.Point(*agent), soln.Face.up)
    walls = [soln.Point(*wall) for wall in walls]
    results = soln.walk_up(agent, walls)
    assert (results.x, results.y) == expected


@pytest.mark.parametrize(
    ["agent", "walls", "expected"],
    [
        ((0, 0), [(5, 0)], (4, 0)),
        ((2, 0), [(1, 0)], (10, 0)),
        ((2, 0), [(8, 0), (5, 0)], (4, 0)),
    ],
)
def test_walk_down(agent, walls, expected):
    agent = soln.Agent(soln.Point(*agent), soln.Face.down)
    walls = [soln.Point(*wall) for wall in walls]
    results = soln.walk_down(agent, walls, max_x=10)
    assert (results.x, results.y) == expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == expected


def test_main_part2(ex_raw_input_p2):
    input_, expected = ex_raw_input_p2
    result = soln.main_part2(input_)
    assert result == expected


@pytest.fixture
def expected_cands():
    return (
        soln.Wall(x, y)
        for x, y in [
            (6, 3),
            (7, 6),
            (8, 1),
            (9, 7),
            (7, 7),
            (8, 3),
        ]
    )


def test_get_naive_walls(input_, expected_cands):
    agent = soln.get_agent(input_)
    walls = soln.get_walls(input_)
    maxes = soln.get_dims(input_)
    agent_pos = soln.walk_agent(agent, walls, maxes=maxes)
    results = soln._get_naive_walls(agent_pos, maxes)
    for e in expected_cands:
        assert e in results


def test_get_wall_candidates(input_, expected_cands):
    agent = soln.get_agent(input_)
    walls = soln.get_walls(input_)
    maxes = soln.get_dims(input_)
    agent_pos = soln.walk_agent(agent, walls, maxes=maxes)
    results = soln.get_wall_candidates(agent_pos, walls, maxes)
    for e in expected_cands:
        assert e in results


@pytest.mark.parametrize(
    ["agent", "expected"],
    [
        ((5, 5), [(4, 5), (6, 5), (5, 6), (5, 4)]),
        ((0, 5), [(1, 5), (0, 6), (0, 4)]),
        ((0, 0), [(1, 0), (0, 1)]),
        ((10, 10), [(9, 10), (10, 9)]),
    ],
)
def test_get_nearby(agent, expected):
    max_ = 10
    expected = [soln.Wall(*ex) for ex in expected]
    agent = soln.Agent(soln.Point(*agent), soln.Face.up)
    result = soln._add_nearby(agent, (max_, max_))
    assert len(result) == len(expected)
    for ex in expected:
        assert ex in result
