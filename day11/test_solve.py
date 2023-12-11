import pytest

from solve import *


@pytest.mark.parametrize(
    "path,shape",
    [
        ["example1.txt", ()],
    ],
)
def test_load(path, shape):
    load(path)


@pytest.mark.parametrize(
    "path,point,row_has_galaxy,col_has_galaxy",
    [
        ["example1.txt", Point(7, 2), False, False],
        ["myexample2.txt", Point(0, 1), True, False],
        ["myexample2.txt", Point(1, 0), False, True],
        ["myexample2.txt", Point(1, 2), False, True],
        ["myexample2.txt", Point(1, 1), False, False],
    ],
)
def test_point_has_galaxy(path, point, row_has_galaxy, col_has_galaxy):
    universe = load(path)
    assert universe.lines.row_has_galaxy(point.x) == row_has_galaxy
    assert universe.lines.col_has_galaxy(point.y) == col_has_galaxy
    assert universe.lines.point_has_galaxy(point) == row_has_galaxy or col_has_galaxy


@pytest.mark.parametrize(
    "path,src_id,dst_id,length",
    [
        ["myexample2.txt", 1, 2, 4],
        ["example1.txt", 5, 9, 9],
    ],
)
def test_(path, src_id, dst_id, length):
    universe = load(path)

    assert (
        distance_between_points(
            universe.graph, universe.galaxy_id_to_point[src_id], universe.galaxy_id_to_point[dst_id]
        )
        == length
    )
