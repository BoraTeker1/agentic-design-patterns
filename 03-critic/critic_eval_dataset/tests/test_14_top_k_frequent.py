from generated_code import top_k_frequent

def test_frequency():
    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]

def test_ties():
    assert top_k_frequent([4, 3, 4, 3, 2], 3) == [3, 4, 2]
    assert top_k_frequent([5, -2, 5, -2], 2) == [-2, 5]

def test_zero_k_and_empty():
    assert top_k_frequent([], 0) == []
    assert top_k_frequent([1, 2], 0) == []

def test_no_mutation():
    values = [2, 1, 2, 3]
    assert top_k_frequent(values, 2) == [2, 1]
    assert values == [2, 1, 2, 3]
