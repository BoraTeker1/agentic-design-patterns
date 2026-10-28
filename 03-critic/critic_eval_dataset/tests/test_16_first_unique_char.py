from generated_code import first_unique_char

def test_basic():
    assert first_unique_char('leetcode') == 'l'
    assert first_unique_char('swiss') == 'w'

def test_none():
    assert first_unique_char('aabbcc') is None
    assert first_unique_char('') is None

def test_case():
    assert first_unique_char('aAab') == 'A'

def test_single():
    assert first_unique_char('x') == 'x'
