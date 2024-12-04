from pathlib import Path

ROOT = Path(__file__).parent / ".."


def read_file(file: Path | str, as_str: bool = False):
    with open(file, "r") as fh:
        fun = fh.readlines
        if as_str:
            fun = fh.read
        payload = fun()
    return payload


def get_input_file(soln_file: str):
    day = Path(soln_file).parent.name
    return ROOT / "usr" / day / "input.txt"
