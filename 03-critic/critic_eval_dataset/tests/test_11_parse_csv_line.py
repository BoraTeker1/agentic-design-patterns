from generated_code import parse_csv_line

def test_basic():
    assert parse_csv_line('a,b,c') == ['a', 'b', 'c']

def test_quoted_commas():
    assert parse_csv_line('"a,b",c') == ['a,b', 'c']

def test_escaped_quotes():
    assert parse_csv_line('"a""b",x') == ['a"b', 'x']
    assert parse_csv_line('"""hi"""') == ['"hi"']

def test_empty_fields():
    assert parse_csv_line('') == ['']
    assert parse_csv_line('a,,') == ['a', '', '']
    assert parse_csv_line('"",b') == ['', 'b']

def test_keep_spaces():
    assert parse_csv_line(' a ,"b c"') == [' a ', 'b c']
