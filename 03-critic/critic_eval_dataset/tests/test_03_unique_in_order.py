from generated_code import unique_in_order

def test_duplicates():
    assert unique_in_order([2, 1, 2, 3, 1]) == [2, 1, 3]

def test_empty_and_single():
    assert unique_in_order([]) == []
    assert unique_in_order([9]) == [9]

def test_negative_numbers():
    assert unique_in_order([-1, 0, -1, -2, 0]) == [-1, 0, -2]

def test_unchanged():
    values = [4, 4, 1]
    assert unique_in_order(values) == [4, 1]
    assert values == [4, 4, 1]
