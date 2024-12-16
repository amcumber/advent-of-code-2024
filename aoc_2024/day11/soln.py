from functools import cache
from pathlib import Path

import click

from ..core import get_input_file, read_file


def to_list(data):
    return [int(ele) for ele in data.strip().split()]


@cache
def apply_rules(stone: int) -> list[int]:
    YEAR = 2024
    if stone == 0:
        return [1]
    if (n := len(s_stone := str(stone))) % 2 == 0:
        n2 = n // 2
        # added backwards
        return [int(s_stone[n2:]), int(s_stone[:n2])]
    return [stone * YEAR]


def blink(stones):
    for istone in reversed(range(len(stones))):
        stone = stones[istone]
        new_stones = apply_rules(stone)
        stones[istone] = new_stones[0]
        if len(new_stones) > 1:
            for i_new_stone in range(1, len(new_stones)):
                stones.insert(istone, new_stones[i_new_stone])
    return stones


def main_part1(data, generations=25):
    """Solution to day 11 part 1"""
    stones = to_list(data)
    for _ in range(generations):
        stones = blink(stones)
    return len(stones)


@cache
def gen0(gen, stagger=0):
    # 0 -> 1 -> 2024 -> 20, 24 -> 2, 0, 2, 4
    #
    # t-0 n = 1
    # t-5 n = 4
    # t-10 n = 7 + 2*gen2(gen-5)+ gen4(gen-5)
    # t-13 = n@t10 + 1
    CYCLE = 5
    rem = (gen + stagger) % CYCLE
    n = (gen + stagger) // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = gen0(m) + 2 * gen2(m) + gen4(m)
    last = 0
    if rem == CYCLE - 2:
        last = 1
    if rem == CYCLE - 1:
        last = 3
    return addl + last


@cache
def gen1(gen):
    if gen == 0:
        return 1
    return gen0(gen - 1, 1)


@cache
def gen2(gen):
    # 2 -> 4048 -> 40, 48 -> 4, 0, 4, 8
    #
    # t-0 n = 1
    # t-4 n = 4
    # t-8 n = 4 + 2*gen4(gen-4)+ gen8(gen-4)
    # t-13 = n@t10 + 1
    CYCLE = 4
    rem = gen % CYCLE
    n = gen // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = gen0(m) + 2 * gen4(m) + gen8(m)
    last = 0
    if rem == CYCLE - 2:
        last = 1
    if rem == CYCLE - 1:
        last = 3
    return addl + last


@cache
def gen3(gen):
    # 6 ->6072 -> 60, 72 -> 6, 0, 7, 2 ->
    CYCLE = 4
    rem = gen % CYCLE
    n = gen // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = gen0(m) + gen2(m) + gen6(m) + gen7(m)
    last = 0
    if rem == CYCLE - 2:
        last = 1
    if rem == CYCLE - 1:
        last = 3
    return addl + last


@cache
def gen4(gen):
    # 4 -> 8096 -> 80, 96 -> 8,0,9,6
    CYCLE = 4
    rem = gen % CYCLE
    n = gen // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = gen0(m) + gen8(m) + gen9(m) + gen6(m)
    last = 0
    if rem == CYCLE - 2:
        last = 1
    if rem == CYCLE - 1:
        last = 3
    return addl + last


@cache
def gen5(gen):
    # 5 -> 10120 -> 20482880 -> 2048, 2880 -> 20, 48, 28, 80 ->
    # 2, 0, 4, 8, 2, 8, 8, 0 ->
    CYCLE = 6
    rem = gen % CYCLE
    n = gen // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = 2 * gen0(m) + 2 * gen2(m) + gen4(m) + 3 * gen8(m)
    last = 0
    if rem == CYCLE - 2:
        last = 3
    elif rem == CYCLE - 3:
        last = 1
    if rem == CYCLE - 1:
        last = 7
    return addl + last


@cache
def gen6(gen):
    # 6 -> 12144 -> 24579456 -> 2457, 9456
    # 24, 57, 94, 56 -> 2, 4, 5,7, 9, 4, 5, 6
    CYCLE = 6
    rem = gen % CYCLE
    n = gen // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = gen2(m) + 2 * gen4(m) + 2 * gen5(m) + gen6(m) + gen7(m) + gen9(m)
    last = 0
    if rem == CYCLE - 2:
        last = 3
    elif rem == CYCLE - 3:
        last = 1
    elif rem == CYCLE - 1:
        last = 7
    return addl + last


@cache
def gen7(gen):
    # 7 ->14168 -> 28676032-> 2867, 6032
    # 28,67, 60, 32 -> 2, 8, 6, 7, 6, 0, 3, 2
    CYCLE = 6
    rem = gen % CYCLE
    n = gen // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = gen0(m) + 2 * gen2(m) + gen3(m) + 2 * gen6(m) + gen7(m) + gen8(m)
    last = 0
    if rem == CYCLE - 2:
        last = 3
    elif rem == CYCLE - 3:
        last = 1
    elif rem == CYCLE - 1:
        last = 7
    return addl + last


@cache
def gen8(gen, stagger=0):
    # 8 -> 16192 -> 32772608 -> 3277, 2608 -> 32, 77, 26, 8 ->
    # 3, 2, 7, 7, 2, 6, 16192 ->
    CYCLE = 6
    rem = (gen + stagger) % CYCLE
    n = (gen + stagger) // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = gen3(m) + 2 * gen2(m) + gen6(m) + 2 * gen7(m) + gen8(m, stagger=1)
    last = 0
    if rem == CYCLE - 2:
        last = 3
    elif rem == CYCLE - 3:
        last = 1
    elif rem == CYCLE - 1:
        last = 7
    return addl + last


@cache
def gen9(gen):
    # 9 -> 18216 -> 36869184 -> 3686, 9184 -> 36, 86, 91, 84 ->
    # 3, 6, 8, 6, 9, 1, 8, 4 ->
    CYCLE = 6
    rem = gen % CYCLE
    n = gen // CYCLE
    addl = 1
    if n >= 1:
        m = gen - CYCLE + 1
        addl = gen1(m) + gen3(m) + gen4(m) + 2 * gen6(m) + 2 * gen8(m) + gen9(m)
    last = 0
    if rem == CYCLE - 2:
        last = 3
    elif rem == CYCLE - 3:
        last = 1
    elif rem == CYCLE - 1:
        last = 7
    return addl + last


def pop_stones(stones):
    out_stones = []
    for n in range(10):
        try:
            while True:
                idx = stones.index(n)
                val = stones.pop(idx)
                out_stones.append(val)
        except ValueError:
            ...
    return out_stones


def count_stones(out_stones, gen):
    N2GEN = {
        0: gen0,
        1: gen1,
        2: gen2,
        3: gen3,
        4: gen4,
        5: gen5,
        6: gen6,
        7: gen7,
        8: gen8,
        9: gen9,
    }
    n = 0
    for stone in out_stones:
        fun = N2GEN[stone]
        n += fun(gen)
    return n


def main_part2(data, generations=75):
    """Solution to day 11 part 2"""
    stones = to_list(data)
    n_stones = 0
    gen = generations
    while True:
        out_stones = pop_stones(stones)
        n_stones += count_stones(out_stones, gen)
        if len(stones) == 0:
            break
        gen -= 1
        stones = blink(stones)
        if gen <= 0:
            break
    return n_stones + len(stones)


@click.group
def cli():
    """Command Line Interface for day11"""


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part1(file):
    data = read_file(Path(file), as_str=True)
    print(main_part1(data))


@cli.command()
@click.option("--file", default=get_input_file(__file__))
def part2(file):
    data = read_file(Path(file), as_str=True)
    print(main_part2(data))
