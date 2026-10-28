from generated_code import max_consecutive_ones

def test_standard():
    assert max_consecutive_ones([1, 1, 0, 1, 1, 1]) == 3

def test_empty_and_zeros():
    assert max_consecutive_ones([]) == 0
    assert max_consecutive_ones([0, 0, 0]) == 0

def test_all_ones():
    assert max_consecutive_ones([1, 1, 1, 1]) == 4

def test_edges_and_unchanged():
    values = [1, 0, 1, 1, 0, 1]
    assert max_consecutive_ones(values) == 2
    assert values == [1, 0, 1, 1, 0, 1]
