from pathlib import Path

ROOT = Path(__file__).parent / ".."


def read_file(file: Path | str):
    with open(file, "r") as fh:
        payload = fh.readlines()
    return payload


def get_input_file(soln_file: str):
    day = Path(soln_file).parent.name
    return ROOT / "usr" / day / "input.txt"
