from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Iterable

import click

from ..core import (
    GridElement,
    get_coord_dims,
    get_input_file,
    grid_input,
    inbounds,
    parse_coords,
    read_file,
)

Point = complex


class Face(Enum):
    up = complex(-1, 0)
    right = complex(0, 1)
    down = complex(1, 0)
    left = complex(0, -1)
    standing = complex(0, 0)


TURN = -1j

WALL = "#"
AGENT_FACES = "^>v<"
SYM2ENUM = {
    "^": Face.up,
    ">": Face.right,
    "v": Face.down,
    "<": Face.left,
}

Agent = namedtuple("Agent", ["pos", "face"])


def get_walls(data):
    return [wall.pos for wall in parse_coords(data, WALL)]


def get_agent(data):
    for ele in grid_input(data):
        if ele.sym in AGENT_FACES:
            return Agent(ele.pos, SYM2ENUM[ele.sym])
    raise AttributeError("Can't find agent!")


def step(
    agent: Agent,
    agent_history: set[Agent],
    walls: Iterable[GridElement],
    dims=tuple[int, int],
) -> bool:
    new_agent = Agent(agent.pos + agent.face.value, agent.face)
    stop = False
    if new_agent.pos in walls:
        new_agent = Agent(agent.pos, Face(agent.face.value * TURN))
    if not inbounds(new_agent, dims):
        new_agent = Agent(new_agent.pos, Face.standing)
        stop = True
        return stop, new_agent

    if new_agent in agent_history:
        stop = True
    agent_history.add(new_agent)
    return stop, new_agent


def walk_agent(
    agent: Agent,
    walls: list[GridElement],
    dims=tuple[int, int],
) -> list[Agent]:
    agent_history = set()
    agent_history.add(agent)
    stop = False
    steps = 0
    MAX_STEPS = 10_000
    while not stop:
        stop, agent = step(agent, agent_history, walls, dims=dims)
        steps += 1
        if steps > MAX_STEPS:
            # hard to find infinite loop?
            break
    return agent_history, agent


def main_part1(data):
    """Solution to day 06 part 1"""
    agent = get_agent(data)
    walls = get_walls(data)
    dims = get_coord_dims(data)
    agent_history, _ = walk_agent(agent, walls, dims=dims)
    agent_pos = {agent.pos for agent in agent_history}
    return len(agent_pos)


def find_loops(
    agent: Agent,
    walls: list[complex],
    candidates: list[complex],
    dims: tuple[int, int],
) -> list[complex]:
    successful = set()
    for cand in candidates:
        tmp_walls = deepcopy(walls)
        tmp_walls.append(cand)
        _, last_agent = walk_agent(agent, tmp_walls, dims=dims)
        if last_agent.face != Face.standing:
            successful.add(cand)
    return successful


def main_part2(data):
    """Solution to day 06 part 2"""
    agent = get_agent(data)
    walls = get_walls(data)
    maxes = get_coord_dims(data)
    agent_history, _ = walk_agent(agent, walls, dims=maxes)
    candidates = [agent.pos for agent in agent_history]
    loops = find_loops(agent, walls, candidates, maxes)
    return len(loops)


@click.group
def cli():
    """Command Line Interface for day06"""


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part1(file):
    data = read_file(Path(file))
    print(main_part1(data))


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part2(file):
    data = read_file(Path(file))
    print(main_part2(data))
