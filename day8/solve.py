import sys
import typing as T
from print_color import print
from collections import OrderedDict
import re
from math import lcm

START = "AAA"
END = "ZZZ"

node_re = re.compile(r"^([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)")

MappingsT = T.Dict[str, T.Tuple[str]]

def load(filepath: str) -> T.Tuple[str, MappingsT]:
    with open(filepath) as f:
        lines = f.readlines()

    directions = lines[0].strip()
    mappings: T.Dict[str, T.Tuple[str]] = OrderedDict()
    for line in lines[2:]:
        line_match = node_re.match(line)
        assert line_match
        line_groups = line_match.groups()
        assert len(line_groups) == 3
        mappings[line_groups[0]] = tuple(line_groups[1:])

    return directions, mappings

def solve(directions: str, mappings: MappingsT, start_el = START, end_conn: T.Callable[[str], bool] = None) -> int:
    el = start_el
    ctr = 0
    if not end_conn:
        end_conn = lambda x: x == END
    while not end_conn(el):
        for direction in directions:
            if end_conn(el):
                break
            node = mappings[el]
            if direction == "L":
                el = node[0]
            else:
                el = node[1]
            ctr += 1

    return ctr

def iter_mappings(directions: str, mappings: MappingsT, node = START):
    el = node
    while True:
        for direction in directions:
            node = mappings[el]
            if direction == "L":
                el = node[0]
            else:
                el = node[1]
            yield el

def ends_with_z(val: str) -> bool:
    return val.endswith("Z")

def solve2brute(directions: str, mappings: MappingsT) -> int:
    starting_nodes = [key for key in mappings.keys() if key.endswith("A")]
    print(starting_nodes)
    iterator_iterators = enumerate(zip(*[iter_mappings(directions, mappings, node=node) for node in starting_nodes]))
    min_true_count = 0
    for i, vals in iterator_iterators:
        is_z = tuple(map(ends_with_z, vals))
        true_count = is_z.count(True)
        if true_count > min_true_count:
            print(f"got new max true_count: {true_count} i: {i} vals: {vals}")
            min_true_count = true_count
        if all(is_z):
            return i + 1
        
def cycle_size(node: str, directions: str, mappings: MappingsT, max_depth=9999, cycle_iterations=1) -> T.Optional[int]:
    seen_els = {}
    cycle_iteration_ctr = 0
    cycle_size = 0
    for i, el in enumerate(iter_mappings(directions, mappings, node=node)):
        if i > max_depth:
            return None
        if el in seen_els:
            inner_cycle_size = i - seen_els[el]
            if cycle_iteration_ctr == cycle_iterations:
                assert inner_cycle_size == cycle_size, f"unstable cycles {cycle_size} -> {inner_cycle_size}"
                return inner_cycle_size
            cycle_size = inner_cycle_size
            seen_els = {}
            cycle_iteration_ctr += 1
        seen_els[el] = i
            
def solve2(directions: str, mappings: MappingsT) -> int:
    starting_nodes = [key for key in mappings.keys() if key.endswith("A")]
    print(f"starting nodes: {starting_nodes}")
    cycles = [cycle_size(node, directions, mappings, cycle_iterations=2) for node in starting_nodes]
    print(f"cycles: {cycles}")
    solutions = [solve(directions, mappings, start_el=node, end_conn=ends_with_z) for node in starting_nodes]
    print(f"solutions: {solutions}")
    return lcm(*solutions)

if __name__ == "__main__":
    directions, mappings = load(sys.argv[1])
    steps = solve2(directions, mappings)
    print(f"steps: {steps}")