from datetime import datetime, timedelta, timezone
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


@mark.parametrize(
    ["raw", "processed"],
    [
        param(
            "2000-01-01T00:00:00-08:00",
            "2000-01-01T00:00:00-08:00",
            id="datetime string full",
        ),
        param(
            "2000-01-01T01:01:01",
            "2000-01-01T01:01:01",
            id="datetime string without timezone",
        ),
        param(
            "2000-01-01 01:01:01-08:00",
            "2000-01-01T01:01:01-08:00",
            id="datetime string without separator",
        ),
        param(
            datetime(2000, 1, 1, tzinfo=timezone(timedelta(hours=-8))),
            "2000-01-01T00:00:00-08:00",
            id="datetime object full",
        ),
        param(
            datetime(2000, 1, 1, 1, 1, 1),
            "2000-01-01T01:01:01",
            id="datetime object without timezone",
        ),
        param(
            datetime(2000, 1, 1),
            "2000-01-01T00:00:00",
            id="datetime object without specified time",
        ),
    ]
)
def test_join_date_conversion(raw: str | datetime, processed: str):
    assert Employee(join_date=raw).join_date == processed


@mark.parametrize(
    "raw",
    [
        param("no date str", id="not datetime string"),
        param("2000-01-01", id="datetime string in an unrecognized format"),
    ]
)
def test_join_date_wrong_formats(raw: str | datetime):
    with raises(ValidationError, match="invalid datetime format"):
        Employee(join_date=raw)
