from pathlib import Path

ROOT = Path(__file__).parent / ".."


def read_file(file: Path | str, as_str: bool = False) -> list[str] | str:
    """read a aoc file using either as newline separated str or as a list of
    strings
    """
    with open(file, "r") as fh:
        fun = fh.readlines
        if as_str:
            fun = fh.read
        payload = fun()
    return payload


def get_input_file(soln_file: str) -> Path:
    """fetch the default location of the input data file
    <root>/usr/<day>/input.txt
    """
    day = Path(soln_file).parent.name
    return ROOT / "usr" / day / "input.txt"


def parse_coords(data: list[str], symbol: str):
    """parse coordinates of a given symbol - used for grid problems
    e.g. result yields (ROW, COL, symbol)
    """
    for irow, line in enumerate(data):
        for icol, ele in enumerate(line.strip()):
            if ele == symbol:
                yield complex(irow, icol), ele


def parse_coords_except(data: list[str], symbol: str):
    """parse coordinates of a given symbol - used for grid problems
    e.g. result yields (ROW, COL, symbol)
    """
    for irow, line in enumerate(data):
        for icol, ele in enumerate(line.strip()):
            if ele != symbol:
                yield complex(irow, icol), ele


def get_coord_dims(data: list[str]) -> tuple[int, int]:
    """get coordinate dimensions assuming square grid"""
    return len(data), len(data[0])
