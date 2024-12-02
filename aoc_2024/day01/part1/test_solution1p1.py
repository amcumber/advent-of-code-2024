import pytest

import solution1p1


@pytest.fixture
def ex_raw_input():
    input_ = "\n".join(
        [
            "3   4",
            "4   3",
            "2   5",
            "1   3",
            "3   9",
            "3   3",
        ]
    )
    expected = 11
    return input_, expected


@pytest.fixture
def ex_input():
    input_ = (
        [
            3,
            4,
            2,
            1,
            3,
            3,
        ],
        [
            4,
            3,
            5,
            3,
            9,
            3,
        ],
    )
    expected = 11
    return input_, expected


def test_main(ex_raw_input):
    input_, expected = ex_raw_input
    result = solution1p1.main(input_)
    assert result == expected
