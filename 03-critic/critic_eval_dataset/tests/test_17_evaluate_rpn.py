from generated_code import evaluate_rpn

def test_basic():
    assert evaluate_rpn(['2', '1', '+', '3', '*']) == 9
    assert evaluate_rpn(['4', '13', '5', '/', '+']) == 6

def test_order_subtract():
    assert evaluate_rpn(['5', '2', '-']) == 3
    assert evaluate_rpn(['2', '5', '-']) == -3

def test_division_toward_zero():
    assert evaluate_rpn(['-7', '3', '/']) == -2
    assert evaluate_rpn(['7', '-3', '/']) == -2

def test_single_and_complex():
    assert evaluate_rpn(['-12']) == -12
    assert evaluate_rpn(['10', '6', '9', '3', '+', '-11', '*', '/', '*', '17', '+', '5', '+']) == 22

def test_unchanged():
    tokens = ['3', '4', '+']
    assert evaluate_rpn(tokens) == 7
    assert tokens == ['3', '4', '+']
