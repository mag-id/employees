from pytest import fixture, mark, param
from app.database import connect_to_employees, find_employees
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
MODEL_ALEX_SMITH_FOO = Employee.parse_obj(RECORD_ALEX_SMITH_FOO)

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
MODEL_ALEX_SMITH_BAR = Employee.parse_obj(RECORD_ALEX_SMITH_BAR)

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
MODEL_SAM_JONES_BAR = Employee.parse_obj(RECORD_SAM_JONES_BAR)

RECORDS = [RECORD_ALEX_SMITH_FOO, RECORD_ALEX_SMITH_BAR, RECORD_SAM_JONES_BAR]
MODELS = [MODEL_ALEX_SMITH_FOO, MODEL_ALEX_SMITH_BAR, MODEL_SAM_JONES_BAR]


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
    employees.insert_many(RECORDS)
    yield
    employees.delete_many({})


def test_no_founded():
    assert find_employees(Employee(name="")) == []


def test_find_by_name():
    employee = Employee(name=MODEL_ALEX_SMITH_FOO.name)
    assert find_employees(employee) == [MODEL_ALEX_SMITH_FOO, MODEL_ALEX_SMITH_BAR]


def test_find_by_age():
    employee = Employee(age=MODEL_ALEX_SMITH_FOO.age)
    assert find_employees(employee) == [MODEL_ALEX_SMITH_FOO, MODEL_SAM_JONES_BAR]


def test_find_by_join_date():
    employee = Employee(age=MODEL_ALEX_SMITH_FOO.join_date)
    # TODO: Test, failed. Fix join_date processing
    assert find_employees(employee) == [MODEL_ALEX_SMITH_FOO]


def test_find_by_name_and_age():
    employee = Employee(
        name=MODEL_ALEX_SMITH_BAR.name,
        age=MODEL_SAM_JONES_BAR.age,
    )
    assert find_employees(employee) == [MODEL_ALEX_SMITH_FOO]


@mark.parametrize("model", MODELS)
def test_find_by_filled_models(model: Employee):
    # TODO: Test, failed. Fix join_date processing
    assert find_employees(model) == [model]


def test_find_all():
    assert find_employees(Employee()) == MODELS
