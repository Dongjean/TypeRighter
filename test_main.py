def add(x, y):
    return x + y

@pytest.mark.parametrize("x, y, expected", [
    (1, 2, 3),
    (6, 7, 13),
    (1, -1, 0),
    (5, 5, 9), # wrong example
    (-5, -9, -14) # this runs too
])
def test_add(x, y, expected):
    assert add(x, y) == expected