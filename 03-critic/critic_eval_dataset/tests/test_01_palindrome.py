from generated_code import is_palindrome

def test_palindromes():
    assert is_palindrome('racecar') is True
    assert is_palindrome('abba') is True

def test_not_palindromes():
    assert is_palindrome('hello') is False
    assert is_palindrome('abca') is False

def test_empty_and_single():
    assert is_palindrome('') is True
    assert is_palindrome('z') is True

def test_case_and_spaces():
    assert is_palindrome('Aa') is False
    assert is_palindrome('a a') is True
