from collections import namedtuple
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).parent / ".."

GridElement = namedtuple("GridElement", ["pos", "sym"])


def read_file(file: Path | str, as_str: bool = False):
    """read a aoc file using either as newline separated str or as a list of
    strings
    """
    with open(file, "r") as fh:
        fun = fh.readlines
        if as_str:
            fun = fh.read
        payload = fun()
    if isinstance(payload, list):
        return [line.strip() for line in payload]
    return payload


def get_input_file(soln_file: str) -> Path:
    """fetch the default location of the input data file
    <root>/usr/<day>/input.txt
    """
    day = Path(soln_file).parent.name
    return ROOT / "usr" / day / "input.txt"


def grid_input(data: Iterable[str]):
    """Generate a complete grid of the given input"""
    for row, line in enumerate(data):
        for col, ele in enumerate(line.strip()):
            yield GridElement(row + 1j * col, ele)


def parse_coords(data: list[str], symbol: str):
    """parse coordinates of a given symbol - used for grid problems
    e.g. result yields (ROW, COL, symbol)
    """
    return (pnt for pnt in grid_input(data) if pnt.sym == symbol)


def parse_coords_except(data: list[str], symbol: str):
    """parse coordinates of a given symbol - used for grid problems
    e.g. result yields (ROW, COL, symbol)
    """
    return (pnt for pnt in grid_input(data) if pnt.sym != symbol)


def get_coord_dims(data: list[str]) -> tuple[int, int]:
    """get coordinate dimensions assuming square grid"""
    return len(data), len(data[0])


def inbounds(element: GridElement, dims: tuple[int, int]) -> bool:
    """return true if object is in bounds of grid dimensions"""
    return 0 <= element.pos.real < dims[0] and 0 <= element.pos.imag < dims[1]
