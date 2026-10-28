from generated_code import second_largest

def test_basic():
    assert second_largest([4, 1, 7, 2]) == 4
    assert second_largest([5, 5, 3, 2]) == 3

def test_insufficient_distinct():
    assert second_largest([]) is None
    assert second_largest([8]) is None
    assert second_largest([6, 6, 6]) is None

def test_negatives():
    assert second_largest([-10, -4, -2, -2]) == -4

def test_input_unchanged():
    values = [7, 2, 7, 4]
    assert second_largest(values) == 4
    assert values == [7, 2, 7, 4]
