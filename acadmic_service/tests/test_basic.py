import pytest
# def test_basic():
#     result = 1 + 2
#     assert result == 3

# def divide():
#     return 10/0

# def test_divide():
#     with pytest.raises(ZeroDivisionError):
#         divide()

@pytest.fixture
def sample_student():
    return {
        "id": 1,
        "name": "Rohit",
        "email": "rohit@test.com",
        "age": 25
    }

def test_sample_student(sample_student):
    assert sample_student["name"] == "Rohitesh"
    assert sample_student["email"] == "rohit@test.com"
    assert sample_student["age"] == 25