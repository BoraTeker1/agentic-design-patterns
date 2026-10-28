from generated_code import valid_ipv4

def test_valid():
    assert valid_ipv4('0.0.0.0') is True
    assert valid_ipv4('192.168.1.255') is True

def test_range():
    assert valid_ipv4('256.1.2.3') is False
    assert valid_ipv4('-1.1.2.3') is False

def test_format():
    assert valid_ipv4('1.2.3') is False
    assert valid_ipv4('1.2.3.4.5') is False
    assert valid_ipv4('1..2.3') is False

def test_leading_zeros_spaces():
    assert valid_ipv4('01.2.3.4') is False
    assert valid_ipv4('1.2.3.4 ') is False

def test_ascii_digits():
    assert valid_ipv4('١.2.3.4') is False
