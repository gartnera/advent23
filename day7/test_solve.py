from solve import *
import pytest

def test_int_hand_repr():
    assert int_hand_repr("J8484") == [1, 8, 4, 8, 4]

def test_basic_hand_rank():
    assert basic_hand_rank(int_hand_repr("32T3K")) == HandType.PAIR

@pytest.mark.parametrize("hand,hand_type", [
    ("JJJJJ", HandType.FIVE),
    ("JKKKK", HandType.FIVE),
    ("JJJKK", HandType.FIVE),
    ("JQKKK", HandType.FOUR),
    ("J3335", HandType.FOUR),
    ("J3345", HandType.THREE),
    ("J2345", HandType.PAIR),
    ("TTKKJ", HandType.FULL),
    ("JJKKQ", HandType.FOUR),
    ("JJJKQ", HandType.FOUR),
])
def test_jokers(hand, hand_type):
    assert basic_hand_rank(int_hand_repr(hand)) == hand_type

def test_example():
    assert calc_total_winnings("example.txt") == 5905

def test_allhands():
    res = sum(list(map(lambda x: x[0] * x[1], zip(range(1,8), range(1,8)))))
    assert calc_total_winnings("allhands.txt") == res