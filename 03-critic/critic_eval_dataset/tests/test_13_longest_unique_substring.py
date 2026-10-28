from generated_code import longest_unique_substring

def test_basic():
    assert longest_unique_substring('abcabcbb') == 3
    assert longest_unique_substring('pwwkew') == 3

def test_all_same():
    assert longest_unique_substring('bbbbb') == 1

def test_empty_single():
    assert longest_unique_substring('') == 0
    assert longest_unique_substring('a') == 1

def test_case_and_spaces():
    assert longest_unique_substring('aA') == 2
    assert longest_unique_substring('abba') == 2

def test_end_window():
    assert longest_unique_substring('dvdf') == 3
