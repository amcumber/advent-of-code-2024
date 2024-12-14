import numpy as np
import pytest

from aoc_2024 import core
from aoc_2024.day13 import soln


@pytest.fixture
def raw_input():
    return [
        "Button A: X+94, Y+34\n",
        "Button B: X+22, Y+67\n",
        "Prize: X=8400, Y=5400\n",
        "\n",
        "Button A: X+26, Y+66\n",
        "Button B: X+67, Y+21\n",
        "Prize: X=12748, Y=12176\n",
        "\n",
        "Button A: X+17, Y+86\n",
        "Button B: X+84, Y+37\n",
        "Prize: X=7870, Y=6450\n",
        "\n",
        "Button A: X+69, Y+23\n",
        "Button B: X+27, Y+71\n",
        "Prize: X=18641, Y=10279\n",
    ]


@pytest.fixture
def ex_eqn1():
    input_ = [
        "Button A: X+94, Y+34\n",
        "Button B: X+22, Y+67\n",
        "Prize: X=8400, Y=5400\n",
    ]
    eqn = (
        np.array(
            [
                [94, 22],
                [34, 67],
            ]
        ),
        np.array([8400, 5400]),
    )
    soln = 280
    return input_, eqn, soln


@pytest.fixture
def ex_eqn2():
    input_ = [
        "Button A: X+26, Y+66\n",
        "Button B: X+67, Y+21\n",
        "Prize: X=12748, Y=12176\n",
    ]
    eqn = (
        np.array(
            [
                [26, 67],
                [66, 21],
            ]
        ),
        np.array([12748, 12176]),
    )
    soln = 0
    return input_, eqn, soln


@pytest.fixture
def ex_eqn3():
    input_ = [
        "Button A: X+17, Y+86\n",
        "Button B: X+84, Y+37\n",
        "Prize: X=7870, Y=6450\n",
    ]
    eqn = (
        np.array(
            [
                [17, 84],
                [86, 37],
            ]
        ),
        np.array([7870, 6450]),
    )
    soln = 0
    return input_, eqn, soln


@pytest.fixture
def ex_eqn4():
    input_ = [
        "Button A: X+69, Y+23\n",
        "Button B: X+27, Y+71\n",
        "Prize: X=18641, Y=10279\n",
    ]
    eqn = (
        np.array(
            [
                [69, 27],
                [23, 71],
            ]
        ),
        np.array([18641, 10279]),
    )
    soln = 200
    return input_, eqn, soln


@pytest.fixture
def ex_raw_input_p1(raw_input):
    expected = [200, 0, 0, 280]
    return raw_input, expected


def test_main_part1(ex_raw_input_p1):
    input_, expected = ex_raw_input_p1
    result = soln.main_part1(input_)
    assert result == sum(expected)
