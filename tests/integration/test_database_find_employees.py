"""
TODO:
    * Keep in mind that the `find_employees` returns' order is not guaranteed. Let's refactor tests according to it.
    * Usage of `Employee` makes tests more coupled. Try to add mocks.
"""
from pytest import mark, param

from app.database import find_employees
from app.models import Employee
from conftest import ALEX_SMITH_FOO, ALEX_SMITH_BAR, SAM_JONES_BAR

ALEX_SMITH_FOO = Employee.parse_obj(ALEX_SMITH_FOO)
ALEX_SMITH_BAR = Employee.parse_obj(ALEX_SMITH_BAR)
SAM_JONES_BAR = Employee.parse_obj(SAM_JONES_BAR)


@mark.parametrize(
    ["query", "response"],
    [
        param(Employee(name=""), [], id="not founded"),
        param(
            Employee(),
            [ALEX_SMITH_FOO, ALEX_SMITH_BAR, SAM_JONES_BAR],
            id="find all",
        ),
        param(
            Employee(name=ALEX_SMITH_FOO.name),
            [ALEX_SMITH_FOO, ALEX_SMITH_BAR],
            id="find by name",
        ),
        param(
            Employee(age=ALEX_SMITH_FOO.age),
            [ALEX_SMITH_FOO, SAM_JONES_BAR],
            id="find by age",
        ),
        param(
            Employee(join_date=ALEX_SMITH_FOO.join_date),
            [ALEX_SMITH_FOO],
            id="find by join_name",
        ),
        param(
            Employee(name=ALEX_SMITH_BAR.name, age=SAM_JONES_BAR.age),
            [ALEX_SMITH_FOO],
            id="find by name and age",
        ),
        param(SAM_JONES_BAR, [SAM_JONES_BAR], id="find by filled model"),
    ]
)
def test_find_employees_unique(query: Employee, response: list[Employee]):
    assert find_employees(query) == response
