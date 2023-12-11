import networkx
import typing as T
from methodtools import lru_cache
import sys
import networkx as nx
import matplotlib.pyplot as plt
from print_color import print


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


class Universe(T.NamedTuple):
    galaxy_id_to_point: IdPointMapT
    graph: nx.Graph
    lines: Lines


def show_graph(graph: nx.Graph):
    elarge = [(u, v) for (u, v, d) in graph.edges(data=True)]

    esmall = [(u, v) for (u, v, d) in graph.edges(data=True)]

    pos = nx.spring_layout(graph)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(graph, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(graph, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(
        graph, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    )
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, "weight"))
    nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")

    plt.axis("off")
    plt.show()


HVNeighborsOffsets = [
    [-1, 0],
    [0, 1],
    [1, 0],
    [0, -1],
]


def load(path: str, diagonals: bool = False) -> Universe:
    with open(path) as f:
        raw_lines = f.readlines()

    # convert to numeric
    galaxy_id = 1
    lines: Lines = Lines()
    galaxy_id_to_point: IdPointMapT = {}
    for x, raw_line in enumerate(raw_lines):
        line = []
        for y, sym in enumerate(raw_line.strip()):
            if sym == "#":
                line.append(galaxy_id)
                galaxy_id_to_point[galaxy_id] = Point(x, y)
                galaxy_id += 1
            else:
                line.append(0)
        lines.append(line)

    g = nx.Graph()

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
                weight = (
                    1 if lines.point_has_galaxy(current) and lines.point_has_galaxy(target) else 2
                )
                g.add_edge(current.name(), target.name(), weight=weight)

    return Universe(galaxy_id_to_point, g, lines)


def distance_between_points(graph: nx.Graph, a: Point, b: Point) -> int:
    path = nx.shortest_path(graph, a.name(), b.name(), weight="weight")
    print(path)
    weights = [graph[path[i]][path[i + 1]]["weight"] for i in range(len(path) - 1)]
    print(weights)
    return sum(weights)


if __name__ == "__main__":
    universe = load(sys.argv[1])
    show_graph(universe.graph)
