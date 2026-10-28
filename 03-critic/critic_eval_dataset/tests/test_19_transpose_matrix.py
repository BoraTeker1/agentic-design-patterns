from generated_code import transpose_matrix

def test_rectangular():
    assert transpose_matrix([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]

def test_square():
    assert transpose_matrix([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]

def test_empty():
    assert transpose_matrix([]) == []
    assert transpose_matrix([[], []]) == []

def test_single_row_column():
    assert transpose_matrix([[8, 9]]) == [[8], [9]]
    assert transpose_matrix([[2], [3]]) == [[2, 3]]

def test_no_mutation():
    data = [[1, 2], [3, 4]]
    assert transpose_matrix(data) == [[1, 3], [2, 4]]
    assert data == [[1, 2], [3, 4]]
