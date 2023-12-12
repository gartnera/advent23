import typing as T
from methodtools import lru_cache
import sys
import rustworkx as rx
import matplotlib.pyplot as plt
from print_color import print
from copy import copy
from itertools import combinations
from tqdm import tqdm


def point_to_name(x: int, y: int) -> str:
    return f"x{x}y{y}"


class Point(T.NamedTuple):
    x: int
    y: int

    def name(self):
        return point_to_name(self.x, self.y)

    @classmethod
    def from_name(cls, name: str):
        x, y = name.split("x")[-1].split("y")
        return cls(x, y)


IdPointMapT = T.Dict[int, Point]
NodeNameToNodeIdT = T.Dict[int, int]


class Lines(list):
    def __init__(self, *args):
        super().__init__(args)

    @lru_cache(maxsize=100)
    def row_has_galaxy(self, x: int) -> bool:
        return max(self[x]) > 0

    @lru_cache(maxsize=100)
    def col_has_galaxy(self, y: int) -> bool:
        for line in self:
            if line[y] > 0:
                return True
        return False

    def point_has_galaxy(self, point: Point) -> bool:
        return self.row_has_galaxy(point.x) or self.col_has_galaxy(point.y)

    def print(self):
        for line in self:
            print(line)


class Universe(T.NamedTuple):
    galaxy_id_to_point: IdPointMapT
    node_name_to_node_id: NodeNameToNodeIdT
    graph: rx.PyDiGraph
    lines: Lines
    max_galaxy_id: int

    def distance_between_points(self, a: Point, b: Point) -> int:
        a_node = self.node_name_to_node_id[a.name()]
        b_node = self.node_name_to_node_id[b.name()]
        pathmap = rx.dijkstra_shortest_paths(self.graph, a_node, b_node, weight_fn=float)
        nodes = pathmap[b_node]
        weights = [self.graph.get_edge_data(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
        return sum(weights)

    def distance_between_all_points(self) -> int:
        res = 0
        for lhand, rhand in tqdm(list(combinations(range(1, self.max_galaxy_id), 2))):
            lhand_pt = self.galaxy_id_to_point[lhand]
            rhand_pt = self.galaxy_id_to_point[rhand]
            res += self.distance_between_points(lhand_pt, rhand_pt)
        return res


HVNeighborsOffsets = [
    [-1, 0],
    [0, 1],
    [1, 0],
    [0, -1],
]


def expand_lines(lines: Lines) -> Lines:
    expanded_lines = Lines(*copy(lines))
    # reverse iteration to perserve insert indexing
    for i, row in reversed(tuple(enumerate(lines))):
        if lines.row_has_galaxy(i):
            continue
        new_row = [0 for _ in range(len(row))]
        expanded_lines.insert(i, new_row)

    for j in range(len(lines[0]) - 1, -1, -1):
        if lines.col_has_galaxy(j):
            continue

        for line in expanded_lines:
            line.insert(j, 0)
    return expanded_lines


def load(path: str, expansion_weight=2) -> Universe:
    with open(path) as f:
        raw_lines = f.readlines()

    # convert to numeric
    max_galaxy_id = 1
    lines: Lines = Lines()
    for _, raw_line in enumerate(raw_lines):
        line = []
        for _, sym in enumerate(raw_line.strip()):
            if sym == "#":
                line.append(max_galaxy_id)
                max_galaxy_id += 1
            else:
                line.append(0)
        lines.append(line)

    # lines = expand_lines(lines)

    g = rx.PyDiGraph()

    node_name_to_node_id: NodeNameToNodeIdT = {}

    galaxy_id_to_point: IdPointMapT = {}
    for x, line in enumerate(lines):
        for y, sym in enumerate(line):
            p = Point(x, y)
            p_name = p.name()
            node_name_to_node_id[p_name] = g.add_node(p_name)
            if sym == 0:
                continue
            galaxy_id_to_point[sym] = Point(x, y)

    for i, line in enumerate(lines):
        for j, sym in enumerate(line):
            current = Point(i, j)
            for ii, jj in HVNeighborsOffsets:
                x = i + ii
                y = j + jj
                target = Point(x, y)
                if x < 0 or x > len(lines) - 1 or y < 0 or y > len(line) - 1:
                    continue
                if current == target:
                    continue
                weight = 1
                if not lines.row_has_galaxy(target.x) or not lines.col_has_galaxy(target.y):
                    weight = expansion_weight
                current_node = node_name_to_node_id[current.name()]
                target_node = node_name_to_node_id[target.name()]
                g.add_edge(current_node, target_node, weight)

    return Universe(galaxy_id_to_point, node_name_to_node_id, g, lines, max_galaxy_id)


if __name__ == "__main__":
    universe = load(sys.argv[1], expansion_weight=1000000)
    res = universe.distance_between_all_points()
    print(res)
