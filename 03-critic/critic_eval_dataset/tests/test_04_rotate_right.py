from generated_code import rotate_right

def test_standard_rotation():
    assert rotate_right([1, 2, 3, 4], 1) == [4, 1, 2, 3]
    assert rotate_right([1, 2, 3, 4], 2) == [3, 4, 1, 2]

def test_large_and_zero():
    assert rotate_right([1, 2, 3], 7) == [3, 1, 2]
    assert rotate_right([1, 2], 0) == [1, 2]

def test_negative():
    assert rotate_right([1, 2, 3, 4], -1) == [2, 3, 4, 1]

def test_empty_and_unchanged():
    assert rotate_right([], 100) == []
    values = [1, 2, 3]
    assert rotate_right(values, 1) == [3, 1, 2]
    assert values == [1, 2, 3]
