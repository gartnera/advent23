from solve import *

def test_int_hand_repr():
    assert int_hand_repr("J8484") == [11, 8, 4, 8, 4]

def test_basic_hand_rank():
    assert basic_hand_rank(int_hand_repr("32T3K")) == 20

def test_example():
    assert calc_total_winnings("example.txt") == 6440

def test_allhands():
    res = sum(list(map(lambda x: x[0] * x[1], zip(range(1,8), range(1,8)))))
    assert calc_total_winnings("allhands.txt") == res