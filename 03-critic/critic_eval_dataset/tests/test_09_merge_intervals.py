from generated_code import merge_intervals

def test_overlapping():
    assert merge_intervals([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]

def test_touching():
    assert merge_intervals([(1, 2), (2, 4)]) == [(1, 4)]

def test_out_of_order_nested():
    assert merge_intervals([(5, 7), (1, 10), (2, 3)]) == [(1, 10)]

def test_empty_and_single():
    assert merge_intervals([]) == []
    assert merge_intervals([(3, 3)]) == [(3, 3)]

def test_not_modified():
    values = [(5, 6), (1, 2)]
    assert merge_intervals(values) == [(1, 2), (5, 6)]
    assert values == [(5, 6), (1, 2)]


def test_adjacent_without_touching():
    assert merge_intervals([(1, 2), (3, 4)]) == [
        (1, 2), (3, 4)
    ]