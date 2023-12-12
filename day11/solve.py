import networkx
import typing as T
from methodtools import lru_cache
import sys
import networkx as nx
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
    graph: nx.Graph
    lines: Lines
    max_galaxy_id: int

    def distance_between_points(self, a: Point, b: Point) -> int:
        path = nx.shortest_path(self.graph, a.name(), b.name())
        return len(path) - 1

    def distance_between_all_points(self) -> int:
        res = 0
        for lhand, rhand in tqdm(list(combinations(range(1, self.max_galaxy_id), 2))):
            lhand_pt = self.galaxy_id_to_point[lhand]
            rhand_pt = self.galaxy_id_to_point[rhand]
            res += self.distance_between_points(lhand_pt, rhand_pt)
        return res


def show_graph(graph: nx.Graph):
    elarge = [(u, v) for (u, v, d) in graph.edges(data=True)]

    esmall = [(u, v) for (u, v, d) in graph.edges(data=True)]

    pos = nx.spectral_layout(graph)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(graph, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(graph, pos, edgelist=elarge, width=2)
    nx.draw_networkx_edges(
        graph, pos, edgelist=esmall, width=2, alpha=0.5, edge_color="b", style="dashed"
    )
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, "weight"))
    nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")

    plt.axis("off")
    plt.tight_layout(pad=0, h_pad=0, w_pad=0)
    plt.show()


HVNeighborsOffsets = [
    [-1, 0],
    [0, 1],
    [1, 0],
    [0, -1],
]


def load(path: str) -> Universe:
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

    galaxy_id_to_point: IdPointMapT = {}
    for x, line in enumerate(expanded_lines):
        for y, sym in enumerate(line):
            if sym == 0:
                continue
            galaxy_id_to_point[sym] = Point(x, y)

    g = nx.Graph()

    for i, line in enumerate(expanded_lines):
        for j, sym in enumerate(line):
            current = Point(i, j)
            for ii, jj in HVNeighborsOffsets:
                x = i + ii
                y = j + jj
                target = Point(x, y)
                if x < 0 or x > len(expanded_lines) - 1 or y < 0 or y > len(line) - 1:
                    continue
                if current == target:
                    continue
                g.add_edge(current.name(), target.name())

    return Universe(galaxy_id_to_point, g, expanded_lines, max_galaxy_id)


if __name__ == "__main__":
    universe = load(sys.argv[1])
    res = universe.distance_between_all_points()
    print(res)
