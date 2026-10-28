from generated_code import normalize_whitespace

def test_regular_spaces():
    assert normalize_whitespace('  hello   world  ') == 'hello world'

def test_newlines_tabs():
    assert normalize_whitespace('a\t\tb\n c') == 'a b c'

def test_empty_whitespace():
    assert normalize_whitespace('') == ''
    assert normalize_whitespace('\n \t ') == ''

def test_already_clean():
    assert normalize_whitespace('one two') == 'one two'
