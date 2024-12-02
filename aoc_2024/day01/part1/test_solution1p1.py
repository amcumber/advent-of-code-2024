import pytest


@pytest.fixture
def ex_raw_input():
    return "\n".join(
        [
            "3   4",
            "4   3",
            "2   5",
            "1   3",
            "3   9",
            "3   3",
        ]
    )


@pytest.fixture
def ex_input():
    return (
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
