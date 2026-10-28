from generated_code import group_anagrams

def test_groups_and_order():
    assert group_anagrams(['eat', 'tan', 'tea', 'nat', 'bat']) == [['eat', 'tea'], ['tan', 'nat'], ['bat']]

def test_identical_words():
    assert group_anagrams(['ab', 'ab', 'ba']) == [['ab', 'ab', 'ba']]

def test_empty_and_empty_words():
    assert group_anagrams([]) == []
    assert group_anagrams(['', 'a', '']) == [['', ''], ['a']]

def test_group_first_appearance():
    assert group_anagrams(['b', 'ac', 'ca', 'a']) == [['b'], ['ac', 'ca'], ['a']]
