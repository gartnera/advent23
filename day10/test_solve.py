from solve import *
import pytest


@pytest.mark.parametrize(
    "path, expected_start_pos",
    [
        ["example1.txt", Point(1, 1)],
        ["example2.txt", Point(2, 0)],
        ["example3.txt", Point(1, 1)],
        ["example4.txt", Point(1, 1)],
        ["example5.txt", Point(4, 12)],
        ["input.txt", Point(92, 43)],
    ],
)
def test_load(path, expected_start_pos):
    diagram = load(path)
    start_pt = find_start_pos(diagram)
    assert start_pt == expected_start_pos


@pytest.mark.parametrize(
    "path, expected_midpoint_distance,alt_start_point",
    [
        ["example1.txt", 4, Point(1, 2)],
        ["example2.txt", 8, Point(3, 0)],
        ["example3.txt", 23, Point(1, 2)],
        ["example4.txt", 22, Point(1, 2)],
        ["example5.txt", 70, None],
        ["input.txt", 7107, Point(92, 42)],
    ],
)
def test_cycle_midpoint_distance(path, expected_midpoint_distance, alt_start_point):
    diagram = load(path)
    start_pt = find_start_pos(diagram)

    assert calc_loop(diagram, start_pt) == expected_midpoint_distance
    assert calc_loop(diagram, start_pt, start_pt=alt_start_point) == expected_midpoint_distance


def test_point_in_set():
    s = {Point(1, 2)}
    assert Point(1, 2) in s
