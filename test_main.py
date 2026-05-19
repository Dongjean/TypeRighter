def add(x, y):
    return x + y

def test_add():
    assert add(1, 2) == 3
    assert add(6, 7) == 13
    assert (1, -1) == 0
    assert (5, 5) == 9 # Wrong example
    assert (-5, -9) == -14