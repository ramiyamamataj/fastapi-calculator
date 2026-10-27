import pytest
from app.operations import add, subtract, multiply, divide

def test_add():
    assert add(10, 5) == 15
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(5, 10) == -5

def test_multiply():
    assert multiply(3, 5) == 15
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(20, 4) == 5
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)
