import typing as T
import sys
from collections import namedtuple

DiagramT = T.List[T.List[str]]
Point = namedtuple("Point", "x y")

StartSym = "S"

def load(path: str) -> DiagramT:
    with open(path) as f:
        lines = f.readlines()

    return [[*line.strip()] for line in lines]

def find_start_pos(diagram: DiagramT) -> Point:
    for x, line in enumerate(diagram):
        for y, sym in enumerate(line):
            if sym == StartSym:
                return Point(x,y)
            
def calc_cycle_midpoint_distance(diagram: DiagramT, origin_pt: Point, start_pt: Point = None) -> int:
    # this is a hack, in both the example and input you can just go one to the right to start
    p_pt = origin_pt
    c_pt = Point(origin_pt.x, origin_pt.y+1) if start_pt is None else start_pt
    current_sym = None
    ctr = 1
    while True:
        current_sym = diagram[c_pt.x][c_pt.y]
        if current_sym == StartSym:
            break
        print(current_sym, p_pt, c_pt, ctr)
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
    
    print(ctr)
    return ctr // 2

if __name__ == "__main__":
    diagram = load(sys.argv[1])
    start_pt = find_start_pos(diagram)
    midpoint_distance = calc_cycle_midpoint_distance(diagram, start_pt)
    print(f"midpoint_distance: {midpoint_distance}")