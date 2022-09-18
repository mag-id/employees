from pydantic.error_wrappers import ValidationError
from pytest import mark, param, raises

from app.models import Employee

VALIDATION_ERROR_MESSAGE_GREATER = "ensure this value is greater than or equal to [0-9]+"
VALIDATION_ERROR_MESSAGE_LESS = "ensure this value is less than or equal to [0-9]+"


def test_initialization():
    employee = Employee(name="Anna", age=20)

    assert employee.name == "Anna"
    assert employee.age == 20

    assert employee.email == None
    assert employee.company == None
    assert employee.join_date == None
    assert employee.job_title == None
    assert employee.gender == None
    assert employee.salary == None


def test_text_field_max_length_acceptable():
    long_name = "".join("G" for _ in range(60))
    assert Employee(name=long_name)


def test_text_field_max_length_exception():
    long_name = "".join("G" for _ in range(61))
    with raises(ValidationError, match="ensure this value has at most [0-9]+ characters"):
        Employee(name=long_name)


@mark.parametrize("age", [14, 140])
def test_age_acceptable(age: int):
    assert Employee(age=age)


@mark.parametrize(
    ["age", "exception_pattern"],
    [
        param(-140, VALIDATION_ERROR_MESSAGE_GREATER),
        param(-14, VALIDATION_ERROR_MESSAGE_GREATER),
        param(13, VALIDATION_ERROR_MESSAGE_GREATER),
        param(141, VALIDATION_ERROR_MESSAGE_LESS)
    ],
)
def test_age_exception(age: int, exception_pattern: str):
    with raises(ValidationError, match=exception_pattern):
        Employee(age=age)


@mark.parametrize("salary", [-0, 0, 100_000])
def test_salary_acceptable(salary: int):
    assert Employee(salary=salary)


@mark.parametrize(
    ["salary", "exception_pattern"],
    [
        param(-100_000, VALIDATION_ERROR_MESSAGE_GREATER),
        param(-1, VALIDATION_ERROR_MESSAGE_GREATER),
        param(100_001, VALIDATION_ERROR_MESSAGE_LESS),
    ],
)
def test_salary_exception(salary: int, exception_pattern: str):
    with raises(ValidationError, match=exception_pattern):
        Employee(salary=salary)
