from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Iterable

import click

from ..core import (
    get_input_file,
    grid_input,
    inbounds,
    parse_coords,
    read_file,
    GridElement,
)

Point = complex


class Face(Enum):
    up = complex(1, 0)
    right = complex(0, 1)
    down = complex(-1, 0)
    left = complex(0, -1)
    standing = complex(0, 0)


TURN = 1j

WALL = "#"
AGENT_FACES = "^>v<"
SYM2ENUM = {
    "^": Face.up,
    ">": Face.right,
    "v": Face.down,
    "<": Face.left,
}


def get_walls(data):
    return parse_coords(data, WALL)


def get_agent(data):
    for ele in grid_input(data):
        if ele.sym in AGENT_FACES:
            return ele
    raise AttributeError("Can't find agent!")


def step(
    agent: GridElement,
    agent_history: set[GridElement],
    walls: Iterable[GridElement],
    dims=tuple[int, int],
) -> bool:
    face = SYM2ENUM[agent.sym]
    new_agent = GridElement(agent.pos + face.value, Face(face.value * TURN).name)
    if inbounds(new_agent, dims):
        if new_agent in agent_history:
            new_agent.sym = Face.standing.name
        agent_history.add(new_agent.pos)
    # TODO: Here
    return new_agent


def walk_agent(
    agent: Agent,
    walls: list[Wall],
    maxes=tuple[int, int],
) -> list[Agent]:
    agent_pos = [agent]
    stop = False
    steps = 0
    MAX_STEPS = 20_000
    while not stop:
        stop = step(agent_pos, walls, dims=maxes)
        # steps += 1
        if steps > MAX_STEPS:
            # hard to find infinite loop?
            break
    return agent_pos


def infill_agents(first: Agent, second: Agent):
    if first.x == second.x:
        axis = 1
        diff = second.y - first.y
        start = first.y
        stop = second.y
    else:
        axis = 0
        diff = second.x - first.x
        start = first.x
        stop = second.x
    direction = 2 * int(diff > 0) - 1
    for ele in range(start, stop, direction):
        if axis:
            yield Agent(Point(first.x, ele), second.face)
        else:
            yield Agent(Point(ele, first.y), second.face)


def infill_agent_list(agent_pos: list[Agent]):
    first_agent = agent_pos.pop(0)
    for next_agent in agent_pos:
        for agent in infill_agents(first_agent, next_agent):
            yield agent
        first_agent = next_agent


def calculate_steps(agent_pos: list[Agent]) -> int:
    no_repeat = set((agent.x, agent.y) for agent in infill_agent_list(agent_pos))
    return len(no_repeat)


def get_dims(data):
    return len(data), len(data[0])


def main_part1(data):
    """Solution to day 06 part 1"""
    agent = get_agent(data)
    walls = get_walls(data)
    maxes = get_dims(data)
    agent_pos = walk_agent(agent, walls, maxes=maxes)
    return calculate_steps(agent_pos)


def _add_nearby(agent: Agent, maxes: tuple[int, int]) -> list[Wall]:
    max_x, max_y = maxes
    left = agent.pos.x - 1, agent.pos.y
    right = agent.pos.x + 1, agent.pos.y
    up = agent.pos.x, agent.pos.y - 1
    down = agent.pos.x, agent.pos.y + 1
    nearby = []
    for x, y in (left, right, up, down):
        if x > max_x or y > max_y or x < 0 or y < 0:
            continue
        nearby.append(Wall(x, y))
    return nearby


def _get_naive_walls(agent_pos: list[Agent], maxes: tuple[int, int]) -> list[Wall]:
    naive_walls = []
    for agent in infill_agent_list(agent_pos):
        naive_walls.extend(_add_nearby(agent, maxes))
    no_doubles = []
    for wall in naive_walls:
        if wall in no_doubles:
            continue
        no_doubles.append(wall)
    return no_doubles


def get_wall_candidates(
    agent_pos: list[Agent], walls: list[Wall], maxes: tuple[int, int]
) -> list[Wall]:
    naive_cand = _get_naive_walls(agent_pos, maxes)
    return [cand for cand in naive_cand if cand not in walls]


def does_wall_make_loop(cand, walls, agent, maxes):
    tmp_walls = deepcopy(walls)
    tmp_walls.append(cand)
    agent_pos = walk_agent(agent, tmp_walls, maxes=maxes)
    return agent_pos[-1].face != Face.standing


def find_loops(
    agent: Agent,
    walls: list[Wall],
    candidates: list[Wall],
    maxes: tuple[int, int],
) -> list[Wall]:
    successful = [
        cand
        for cand in candidates
        if does_wall_make_loop(
            cand,
            walls,
            agent,
            maxes,
        )
    ]
    return successful


def main_part2(data):
    """Solution to day 06 part 2"""
    agent = get_agent(data)
    walls = get_walls(data)
    maxes = get_dims(data)
    agent_pos = walk_agent(agent, walls, maxes=maxes)
    candidates = get_wall_candidates(agent_pos, walls, maxes)
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
