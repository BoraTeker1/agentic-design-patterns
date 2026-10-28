from generated_code import flatten_once

def test_basic():
    assert flatten_once([[1, 2], [3], [4, 5]]) == [1, 2, 3, 4, 5]

def test_empty():
    assert flatten_once([]) == []
    assert flatten_once([[], []]) == []

def test_empty_middle():
    assert flatten_once([[1], [], [2]]) == [1, 2]

def test_input_unchanged():
    values = [[1], [2, 3]]
    assert flatten_once(values) == [1, 2, 3]
    assert values == [[1], [2, 3]]
