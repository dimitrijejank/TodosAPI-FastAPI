import pytest

def test_equal_or_not_q_equal():
    assert 3 == 3

class Student:
    def __init__(self, first_name: str,last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student("Dimitrije", "Jankovic", "Computer Science", 3)

def test_person_initialization(default_employee):
    assert default_employee.first_name == "Dimitrije", "Dimitrije should be first name"
    assert default_employee.last_name == "Jankovic", "Jankovic should be a last name"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3