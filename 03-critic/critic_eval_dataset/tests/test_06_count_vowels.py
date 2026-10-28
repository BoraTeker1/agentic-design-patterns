from generated_code import count_vowels

def test_regular():
    assert count_vowels('Education') == 5
    assert count_vowels('hello') == 2

def test_case():
    assert count_vowels('AEIOUaeiou') == 10

def test_empty_and_no_vowels():
    assert count_vowels('') == 0
    assert count_vowels('rhythm') == 0

def test_accented():
    assert count_vowels('éüa') == 1
