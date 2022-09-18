"""
TODO: Usage of `Employee` makes tests more coupled. Try to add mocks.
"""
from pytest import fixture

from app.database import connect_to_employees
from app.models import Employee

RECORD_ALEX_SMITH_FOO = {
    "name": "Alex Smith",
    "email": "Alex.Smith@foo.com",
    "age": 30,
    "company": "Foo Inc",
    "join_date": "2015-12-30T23:59:59-08:00",
    "job_title": "senior developer",
    "gender": "female",
    "salary": 5000
}
RECORD_ALEX_SMITH_BAR = {
    "name": "Alex Smith",
    "email": "Alex.Smith@bar.com",
    "age": 25,
    "company": "Bar Inc",
    "join_date": "2022-12-30T23:59:59-07:00",
    "job_title": "junior developer",
    "gender": "male",
    "salary": 1000
}
RECORD_SAM_JONES_BAR = {
    "name": "Sam Jones",
    "email": "Sam.Jones@bar.com",
    "age": 30,
    "company": "Bar Inc",
    "join_date": "2020-12-30T23:59:59-07:00",
    "job_title": "middle developer",
    "gender": "male",
    "salary": 3000
}
ALEX_SMITH_FOO = Employee.parse_obj(RECORD_ALEX_SMITH_FOO)
ALEX_SMITH_BAR = Employee.parse_obj(RECORD_ALEX_SMITH_BAR)
SAM_JONES_BAR = Employee.parse_obj(RECORD_SAM_JONES_BAR)


@fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "27017")
    monkeypatch.setenv("DB_USERNAME", "username")
    monkeypatch.setenv("DB_PASSWORD", "password")
    yield
    monkeypatch.delenv("DB_HOST")
    monkeypatch.delenv("DB_PORT")
    monkeypatch.delenv("DB_USERNAME")
    monkeypatch.delenv("DB_PASSWORD")


@fixture(autouse=True)
def prepare_records():
    employees = connect_to_employees()
    employees.insert_many([
        RECORD_ALEX_SMITH_FOO,
        RECORD_ALEX_SMITH_BAR,
        RECORD_SAM_JONES_BAR,
    ])
    yield
    employees.delete_many({})
