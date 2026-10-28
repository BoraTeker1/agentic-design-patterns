from generated_code import missing_ranges

def test_multiple_gaps():
    assert missing_ranges([0, 1, 3, 50, 75], 0, 99) == [(2, 2), (4, 49), (51, 74), (76, 99)]

def test_no_gaps():
    assert missing_ranges([1, 2, 3], 1, 3) == []

def test_empty():
    assert missing_ranges([], 3, 5) == [(3, 5)]

def test_boundaries():
    assert missing_ranges([2, 3], 1, 4) == [(1, 1), (4, 4)]
    assert missing_ranges([2], 2, 2) == []

def test_negative_and_unchanged():
    values = [-2, 0]
    assert missing_ranges(values, -3, 1) == [(-3, -3), (-1, -1), (1, 1)]
    assert values == [-2, 0]
