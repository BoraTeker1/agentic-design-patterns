from generated_code import is_palindrome


def test_nonpalindrome():
    assert is_palindrome("hello") == False

def test_palindrome():
    assert is_palindrome('racecar') == True


    