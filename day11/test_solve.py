import pytest

from solve import *


@pytest.mark.parametrize(
    "path,shape",
    [
        ["myexample1.txt", Point(4, 4)],
        ["myexample2.txt", Point(4, 4)],
        ["example1.txt", Point(13, 12)],
    ],
)
def test_load(path, shape: Point):
    universe = load(path)
    assert len(universe.lines) == shape.y
    assert len(universe.lines[0]) == shape.x


@pytest.mark.parametrize(
    "path,src_id,dst_id,length",
    [
        ["myexample2.txt", 1, 2, 6],
        ["example1.txt", 5, 9, 9],
        ["example1.txt", 1, 7, 15],
        ["example1.txt", 3, 6, 17],
    ],
)
def test_distance_between_points(path, src_id, dst_id, length):
    universe = load(path)

    src_point = universe.galaxy_id_to_point[src_id]
    dst_point = universe.galaxy_id_to_point[dst_id]
    assert universe.distance_between_points(src_point, dst_point) == length
