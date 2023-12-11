import typing as T
import sys
import copy
from functools import reduce
import os
import subprocess
import time

DiagramT = T.List[T.List[str]]


class Point(T.NamedTuple):
    x: int
    y: int


StartSym = "S"


def load(path: str) -> DiagramT:
    with open(path) as f:
        lines = f.readlines()

    return [[*line.strip()] for line in lines]


def find_start_pos(diagram: DiagramT) -> Point:
    for x, line in enumerate(diagram):
        for y, sym in enumerate(line):
            if sym == StartSym:
                return Point(x, y)


def print_diagram(diagram: DiagramT):
    for line in diagram:
        print("".join(line))


def clean_diagram(diagram: DiagramT, loop_pts: T.Set[Point]) -> DiagramT:
    """
    remove irrelevent symbols from the diagram
    """
    diagram = copy.copy(diagram)
    for x, line in enumerate(diagram):
        for y, sym in enumerate(line):
            if sym == ".":
                continue
            p = Point(x, y)
            if p in loop_pts:
                continue
            line[y] = " "
    return diagram


def line_has_sym(line: T.List[str], start_idx: int, step: int) -> bool:
    idx = start_idx
    while idx < len(line) and idx > 0:
        sym = line[idx]
        if sym != " " and sym != ".":
            return True
        idx += step
    return False


def col_has_sym(diagram: DiagramT, origin: Point, step: int) -> bool:
    idx = origin.x
    while idx < len(diagram) and idx > 0:
        sym = diagram[idx][origin.y]
        if sym != " " and sym != ".":
            return True
        idx += step
    return False


def prune_obvious_outside(diagram: DiagramT) -> DiagramT:
    diagram = copy.copy(diagram)
    for x, line in enumerate(diagram):
        for y, sym in enumerate(line):
            if sym != ".":
                continue
            left = line_has_sym(line, y, -1)
            right = line_has_sym(line, y, 1)
            up = col_has_sym(diagram, Point(x, y), -1)
            down = col_has_sym(diagram, Point(x, y), 1)
            if left and right and up and down:
                continue
            line[y] = " "

    return diagram


def calc_loop(diagram: DiagramT, origin_pt: Point, start_pt: Point = None) -> T.Tuple[int, int]:
    # this is a hack, in both the example and input you can just go one to the right to start
    p_pt = origin_pt
    c_pt = Point(origin_pt.x, origin_pt.y + 1) if start_pt is None else start_pt
    current_sym = None
    ctr = 1
    loop_pts = {origin_pt}
    while True:
        loop_pts.add(c_pt)
        current_sym = diagram[c_pt.x][c_pt.y]
        if current_sym == StartSym:
            break
        # print(current_sym, p_pt, c_pt, ctr)
        next_p_pt = c_pt
        match current_sym:
            case "J":
                c_pt = Point(c_pt.x - 1, c_pt.y) if p_pt.x == c_pt.x else Point(c_pt.x, c_pt.y - 1)
            case "F":
                c_pt = Point(c_pt.x + 1, c_pt.y) if p_pt.x == c_pt.x else Point(c_pt.x, c_pt.y + 1)
            case "7":
                c_pt = Point(c_pt.x + 1, c_pt.y) if p_pt.x == c_pt.x else Point(c_pt.x, c_pt.y - 1)
            case "|":
                c_pt = Point(c_pt.x + 1, c_pt.y) if p_pt.x < c_pt.x else Point(c_pt.x - 1, c_pt.y)
            case "L":
                c_pt = Point(c_pt.x - 1, c_pt.y) if p_pt.x == c_pt.x else Point(c_pt.x, c_pt.y + 1)
            case "-":
                c_pt = Point(c_pt.x, c_pt.y - 1) if p_pt.y > c_pt.y else Point(c_pt.x, c_pt.y + 1)
            case _:
                raise Exception(f"unhandled sym: {current_sym}")

        p_pt = next_p_pt
        ctr += 1

    loop_midpoint_distance = ctr // 2

    cdiagram = clean_diagram(diagram, loop_pts)
    print_diagram(cdiagram)
    pcdiagram = prune_obvious_outside(diagram)
    print_diagram(pcdiagram)

    raw_period_ctr = sum(row.count(".") for row in pcdiagram)

    return loop_midpoint_distance, raw_period_ctr


if __name__ == "__main__":
    diagram = load(sys.argv[1])
    start_pt = find_start_pos(diagram)
    midpoint_distance, raw_period_ctr = calc_loop(diagram, start_pt)
    print(f"midpoint_distance: {midpoint_distance} raw_period_ctr: {raw_period_ctr}")
