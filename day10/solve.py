import typing as T
import sys
import copy
from print_color import print

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


def print_color_fixed_width(num: int):
    color = "blue" if (num // 10 % 2 == 0) else "green"
    print(num % 10, color=color, end="")


def print_diagram(
    diagram: DiagramT, red_pts: T.Set[Point] = None, green_pts: T.Set[Point] = None, number=True
):
    if number:
        print(" ", end="")
    for y in range(len(diagram[0])):
        if number:
            print_color_fixed_width(y)
    if number:
        print()
    for x, line in enumerate(diagram):
        if number:
            print_color_fixed_width(x)
        for y, sym in enumerate(line):
            point = Point(x, y)
            color = "red" if red_pts and point in red_pts else ""
            color = "green" if green_pts and point in green_pts else color
            print(sym, end="", color=color)
        print()


def clean_diagram(diagram: DiagramT, good_pts: T.Set[Point]) -> DiagramT:
    """
    remove irrelevent symbols from the diagram
    """
    diagram = copy.copy(diagram)
    for x, line in enumerate(diagram):
        for y, _ in enumerate(line):
            p = Point(x, y)
            if p in good_pts:
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


def calc_inner_point(prev: Point, current: Point) -> Point:
    return Point(current.x + (current.y - prev.y), current.y + (prev.x - current.x))


def dilate_inner_points(inner_pts: T.Set[Point], loop_pts: T.Set[Point]):
    did_dialate = False
    for inner_pt in inner_pts.copy():
        for i in range(3):
            for j in range(3):
                dc_point = Point(inner_pt.x + i - 1, inner_pt.y + j - 1)
                if dc_point == inner_pt or dc_point in inner_pts or dc_point in loop_pts:
                    continue
                inner_pts.add(dc_point)
                did_dialate = True
    if did_dialate:
        dilate_inner_points(inner_pts, loop_pts)


def calc_loop(diagram: DiagramT, origin_pt: Point, start_pt: Point = None) -> T.Tuple[int, int]:
    # this is a hack, in both the example and input you can just go one to the right to start
    p_pt = origin_pt
    c_pt = Point(origin_pt.x, origin_pt.y + 1) if start_pt is None else start_pt
    current_sym = None
    ctr = 1
    loop_pts = {origin_pt}
    raw_inner_pts = set()
    while True:
        loop_pts.add(c_pt)
        current_sym = diagram[c_pt.x][c_pt.y]
        if current_sym == StartSym:
            break
        # print(current_sym, p_pt, c_pt, ctr)
        inner_pt = calc_inner_point(p_pt, c_pt)
        # print(f"inner_pt: {inner_pt}")
        if diagram[inner_pt.x][inner_pt.y]:
            raw_inner_pts.add(inner_pt)
        # print_diagram(diagram, red_pts={inner_pt}, green_pts={c_pt})
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

    cdiagram = diagram
    # cdiagram = prune_obvious_outside(diagram)
    inner_pts = raw_inner_pts - loop_pts
    print_diagram(cdiagram, red_pts=inner_pts)
    dilate_inner_points(inner_pts, loop_pts)
    cdiagram = clean_diagram(diagram, loop_pts.union(inner_pts))
    print_diagram(cdiagram, red_pts=inner_pts)

    return loop_midpoint_distance, len(inner_pts)


if __name__ == "__main__":
    diagram = load(sys.argv[1])
    start_pt = find_start_pos(diagram)
    midpoint_distance, inner_ctr = calc_loop(diagram, start_pt)
    print(f"midpoint_distance: {midpoint_distance} inner_ctr: {inner_ctr}")
