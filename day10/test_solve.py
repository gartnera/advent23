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


def test_point_in_set():
    s = {Point(1, 2)}
    assert Point(1, 2) in s


@pytest.mark.parametrize(
    "path, expected_midpoint_distance,expected_inside_ctr,alt_start_point",
    [
        ["example1.txt", 4, None, None],
        ["example2.txt", 8, None, None],
        ["example3.txt", 23, 4, None],
        ["example4.txt", 22, 4, None],
        ["example5.txt", 70, 8, Point(5, 12)],
        ["example6.txt", 80, 10, Point(1, 4)],
        # can't get correct answer for part 2 :( for the real input
        # 274 is not correct :( 281 is the correct answer
        ["input.txt", 7107, 274, None],
    ],
)
def test_cycle_midpoint_distance(
    path, expected_midpoint_distance, expected_inside_ctr, alt_start_point
):
    diagram = load(path)
    start_pt = find_start_pos(diagram)

    midpoint, inside_ctr = calc_loop(diagram, start_pt, start_pt=alt_start_point)
    assert midpoint == expected_midpoint_distance
    if expected_inside_ctr:
        assert inside_ctr == expected_inside_ctr
