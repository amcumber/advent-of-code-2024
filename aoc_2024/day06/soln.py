from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

import click

from ..core import get_input_file, read_file


class Face(Enum):
    up = auto()
    right = auto()
    down = auto()
    left = auto()
    standing = auto()


WALL = "#"
AGENT_FACES = ["^", ">", "v", "<"]
AGENT2ENUM = {
    "^": Face.up,
    ">": Face.right,
    "v": Face.down,
    "<": Face.left,
}
TURN = {
    Face.up: Face.right,
    Face.right: Face.down,
    Face.down: Face.left,
    Face.left: Face.up,
    Face.standing: Face.standing,
}


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
    for agent_face in AGENT_FACES:
        face = AGENT2ENUM[agent_face]
        if agent_pos := _get_targets(data, agent_face):
            return Agent(Point(*agent_pos.pop()), face)


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Must be same type")
        return (self.x, self.y) == (other.x, other.y)


@dataclass
class Wall(Point):
    """wall"""


@dataclass
class Agent:
    """agent position and facing direction"""

    pos: Point
    face: Face

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Must be same type")
        if self.pos != other.pos:
            return False
        return self.face == other.face


def get_walls_row(agent: Agent, walls: list[Wall]):
    return [wall for wall in walls if wall.x == agent.x]


def get_walls_col(agent: Agent, walls: list[Wall]):
    return [wall for wall in walls if wall.y == agent.y]


def walk_up(agent, walls) -> Agent:
    collided_wall = None
    for wall in get_walls_col(agent, walls):
        is_wall_fits = wall.x < agent.x
        is_wall_close = True
        if collided_wall is not None:
            is_wall_close = wall.x > collided_wall.x
        if is_wall_fits and is_wall_close:
            collided_wall = wall
    if collided_wall is None:
        return Agent(Point(0, agent.y), Face.standing)
    return Agent(Point(collided_wall.x + 1, agent.y), TURN[agent.face])


def walk_right(agent, walls, max_y=999):
    collided_wall = None
    for wall in get_walls_row(agent, walls):
        is_wall_fits = wall.y > agent.y
        is_wall_close = True
        if collided_wall is not None:
            is_wall_close = wall.y < collided_wall.y
        if is_wall_fits and is_wall_close:
            collided_wall = wall
    if collided_wall is None:
        return Agent(Point(agent.x, max_y), Face.standing)
    return Agent(Point(agent.x, collided_wall.y - 1), TURN[agent.face])


def walk_down(agent, walls, max_x=999):
    collided_wall = None
    for wall in get_walls_col(agent, walls):
        is_wall_fits = wall.x > agent.x
        is_wall_close = True
        if collided_wall is not None:
            is_wall_close = wall.x < collided_wall.x
        if is_wall_fits and is_wall_close:
            collided_wall = wall
    if collided_wall is None:
        return Agent(Point(max_x, agent.y), Face.standing)
    return Agent(Point(collided_wall.x - 1, agent.y), TURN[agent.face])


def walk_left(agent, walls):
    collided_wall = None
    for wall in get_walls_row(agent, walls):
        is_wall_fits = wall.y < agent.y
        is_wall_close = True
        if collided_wall is not None:
            is_wall_close = wall.y > collided_wall.y
        if is_wall_fits and is_wall_close:
            collided_wall = wall
    if collided_wall is None:
        return Agent(Point(agent.x, 0), Face.standing)
    return Agent(Point(agent.x, collided_wall.y + 1), TURN[agent.face])


def step(agent_pos: list[Agent], walls: list[Wall], maxes=tuple[int, int]) -> bool:
    agent = agent_pos[-1]
    max_x, max_y = maxes
    match agent.face:
        case Face.up:
            new_agent = walk_up(agent, walls)
        case Face.right:
            new_agent = walk_right(agent, walls, max_y=max_y)
        case Face.down:
            new_agent = walk_down(agent, walls, max_x=max_x)
        case Face.left:
            new_agent = walk_left(agent, walls)
        case Face.standing:
            return True
    if new_agent in agent_pos:
        return True
    if new_agent.pos == agent_pos[-1].pos:
        agent_pos[-1] = new_agent
    agent_pos.append(new_agent)
    return False


def walk_agent(agent: Agent, walls: list[Wall], maxes=tuple[int, int]) -> list[Agent]:
    agent_pos = [agent]
    stop = False
    while not stop:
        stop = step(agent_pos, walls, maxes=maxes)
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
    """Solution to day 05 part 1"""
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
    tmp_walls = walls.copy()
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
    # for cand in candidates:
    #     if await does_wall_make_loop(cand, walls, maxes):
    #         successful.append(cand)
    final_set = set((wall.x, wall.y) for wall in successful)
    return final_set


def main_part2(data):
    """Solution to day 05 part 2"""
    agent = get_agent(data)
    walls = get_walls(data)
    maxes = get_dims(data)
    agent_pos = walk_agent(agent, walls, maxes=maxes)
    candidates = get_wall_candidates(agent_pos, walls, maxes)
    loops = find_loops(agent, walls, candidates, maxes)
    return len(loops)


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
