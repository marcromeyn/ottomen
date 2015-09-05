def func(x):
    return x + 1


def test_answer(db):
    assert func(4) == 5
