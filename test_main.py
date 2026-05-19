def add(x, y):
    return x + y

def test_add():
    assert add(1, 2) == 3
    assert add(6, 7) == 13
    assert add(1, -1) == 0
    assert add(5, 5) == 9 # Wrong example
    assert add(-5, -9) == -14