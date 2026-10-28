from generated_code import run_length_encode

def test_basic():
    assert run_length_encode('aaabbc') == 'a3b2c1'

def test_single_and_empty():
    assert run_length_encode('x') == 'x1'
    assert run_length_encode('') == ''

def test_case_sensitive():
    assert run_length_encode('aAAa') == 'a1A2a1'

def test_long_run_and_spaces():
    assert run_length_encode('a' * 12) == 'a12'
    assert run_length_encode('  ') == ' 2'
