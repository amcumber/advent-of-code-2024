import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import click

from ..core import get_input_file, read_file

WALL = "#"
AGENTS = ["^", ">", "v", "<"]
WALK = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
    "": None,
}
TURN = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
    "": None,
}
_gbl_max_x = None
_gbl_max_y = None


def _get_targets(data: list[str], target: str) -> list[tuple[int, int]]:
    targets = []
    for x, row in enumerate(data):
        if target in row:
            for y, ele in enumerate(row):
                if ele == target:
                    targets.append((x, y))
    return targets


def get_walls(data):
    return [Wall(*ele) for ele in _get_targets(data, WALL)]


def get_agent(data):
    for agent_face in AGENTS:
        if agent_list := _get_targets(data, agent_face):
            return Agent(Point(*agent_list.pop()), agent_face)


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Wall(Point):
    """wall"""


@dataclass
class Agent:
    """agent position and facing direction"""

    pos: Point
    face: str

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y


def get_walls_row(agent_row: int, walls: list[Wall]):
    return [wall for wall in walls if wall.y == agent_row]


def get_walls_col(agent_col: int, walls: list[Wall]):
    return [wall for wall in walls if wall.x == agent_col]


def walk_up(agent, walls) -> Agent:
    collided_wall = None
    for wall in get_walls_col(agent.y, walls):
        is_wall_fits = wall.x < agent.x
        is_wall_close = collided_wall is not None and wall.x > collided_wall.x
        if is_wall_fits and is_wall_close:
            collided_wall = wall
    if collided_wall is None:
        return Agent(Point(_gbl_max_x, agent.y), "")
    return Agent(Point(collided_wall.x + 1, agent.y), TURN[agent.face])


def walk_right(agent, walls):
    collided_wall = None
    for wall in get_walls_row(agent.x, walls):
        is_wall_fits = wall.y > agent.y
        is_wall_close = collided_wall is not None and wall.y < collided_wall.y
        if is_wall_fits and is_wall_close:
            collided_wall = wall
    if collided_wall is None:
        return Agent(Point(agent.x, _gbl_max_y), "")
    return Agent(Point(agent.x, collided_wall.y - 1), TURN[agent.face])


def walk_down(agent, walls):
    collided_wall = None
    for wall in get_walls_col(agent.y, walls):
        is_wall_fits = wall.x > agent.x
        is_wall_close = collided_wall is not None and wall.x < collided_wall.x
        if is_wall_fits and is_wall_close:
            collided_wall = wall
    if collided_wall is None:
        return Agent(Point(_gbl_max_x, agent.y), "")
    return Agent(Point(collided_wall.x - 1, agent.y), TURN[agent.face])


def walk_left(agent, walls):
    collided_wall = None
    for wall in get_walls_row(agent.x, walls):
        is_wall_fits = wall.y < agent.y
        is_wall_close = collided_wall is not None and wall.y > collided_wall.y
        if is_wall_fits and is_wall_close:
            collided_wall = wall
    if collided_wall is None:
        return Agent(Point(agent.x, _gbl_max_y), "")
    return Agent(Point(agent.x, collided_wall.y + 1), TURN[agent.face])


def step(agent_pos: list[Agent], walls: list[Wall]) -> bool:
    agent = agent_pos[-1]
    match agent.face:
        case "^":
            new_agent = walk_up(agent, walls)
        case ">":
            new_agent = walk_right(agent, walls)
        case "v":
            new_agent = walk_down(agent, walls)
        case "<":
            new_agent = walk_left(agent, walls)
        case "":
            return True
    agent_pos.append(new_agent)
    return False


def walk_agent(agent: tuple[int, int], walls: list[tuple[int, int]]):
    agent_pos = [agent]
    stop = False
    while not stop:
        stop = step(agent_pos, walls)
    return agent_pos


def infill_agents(first, second):
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
    direction = int(diff > 0)
    for ele in range(start, stop, direction):
        if axis:
            yield Agent(Point(first.x, ele), second.face)
        else:
            yield Agent(Point(ele, first.y), second.face)


def calculate_steps(agent_pos):
    first_agent = agent_pos.pop(0)
    infilled = []
    for next_agent in agent_pos:
        infilled.extend(list(infill_agents(first_agent, next_agent)))
    return len(set((agent.x, agent.y) for agent in infilled))


def set_glb(data):
    global _gbl_max_x
    global _gbl_max_y
    _gbl_max_x = len(data)
    _gbl_max_y = len(data[0])


def main_part1(data):
    """Solution to day 05 part 1"""
    agent = get_agent(data)
    walls = get_walls(data)
    set_glb(data)
    agent_pos = walk_agent(agent, walls)
    return calculate_steps(agent_pos)


def main_part2(data):
    """Solution to day 05 part 2"""


@click.group
def cli():
    """Command Line Interface for day05"""


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
