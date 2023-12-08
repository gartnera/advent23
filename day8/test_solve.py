from solve import *
import pytest

def test_load():
    _, mappings = load("example1.txt")
    assert len(mappings) == 7

def test_load_example3():
    _, mappings = load("example3.txt")
    assert len(mappings) == 8

def test_example1():
    directions, mappings = load("example1.txt")
    assert solve(directions, mappings) == 2

def test_example2():
    directions, mappings = load("example2.txt")
    assert solve(directions, mappings) == 6

def test_example3_brute():
    directions, mappings = load("example3.txt")
    assert solve2brute(directions, mappings) == 6

def test_example3():
    directions, mappings = load("example3.txt")
    assert solve2(directions, mappings) == 6

@pytest.mark.parametrize("cycle_iterations", [1,2,3])
def test_cyclesize(cycle_iterations):
    directions, mappings = load("cycle1.txt")
    assert cycle_size("AAA", directions, mappings, cycle_iterations=cycle_iterations) == 2

    directions, mappings = load("cycle2.txt")
    assert cycle_size("AAA", directions, mappings, cycle_iterations=cycle_iterations) == 2

    directions, mappings = load("cycle2.txt")
    assert cycle_size("AAA", directions, mappings, cycle_iterations=cycle_iterations) == 2

    directions, mappings = load("example1.txt")
    assert cycle_size("AAA", directions, mappings, cycle_iterations=cycle_iterations) == 1