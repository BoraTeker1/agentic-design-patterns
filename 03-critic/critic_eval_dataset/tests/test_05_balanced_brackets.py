from generated_code import balanced_brackets

def test_nested():
    assert balanced_brackets('([{}])') is True
    assert balanced_brackets('x{a[2+(3)]}') is True

def test_mismatched():
    assert balanced_brackets('([)]') is False
    assert balanced_brackets('(]') is False

def test_missing_close_or_open():
    assert balanced_brackets('(()') is False
    assert balanced_brackets('a)b') is False

def test_empty_non_brackets():
    assert balanced_brackets('') is True
    assert balanced_brackets('abc 123') is True
