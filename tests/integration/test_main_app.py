"""
TODO: More tests can be added.
"""
from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import mark, param

from app.main import APP
from conftest import ALEX_SMITH_FOO, ALEX_SMITH_BAR, SAM_JONES_BAR

CLIENT = TestClient(APP)


@mark.asyncio
@mark.parametrize(
    ["route", "status", "body"],
    [
        param("/", HTTPStatus.NOT_FOUND, {"detail": "Not Found"}),
        param(
            "/employees",
            HTTPStatus.OK,
            [ALEX_SMITH_FOO, ALEX_SMITH_BAR, SAM_JONES_BAR]
        ),
        param(
            "/employees?name=Alex Smith",
            HTTPStatus.OK,
            [ALEX_SMITH_FOO, ALEX_SMITH_BAR]
        ),
        param(
            "/employees?age=30",
            HTTPStatus.OK,
            [ALEX_SMITH_FOO, SAM_JONES_BAR]
        ),
        param(
            "/employees?join_date=2015-12-30T23:59:59-08:00",
            HTTPStatus.OK,
            [ALEX_SMITH_FOO]
        ),
        param(
            "/employees?name=Alex Smith&age=30",
            HTTPStatus.OK,
            [ALEX_SMITH_FOO]
        ),
        param(
            "/employees?name=Sam Jones&email=Sam.Jones@bar.com&age=30&company=Bar Inc&join_date=2020-12-30T23:59:59-07:00&job_title=middle developer&gender=male&salary=3000",
            HTTPStatus.OK,
            [SAM_JONES_BAR]
        ),
    ]
)
async def test_get_employees(route: str, status: HTTPStatus, body: dict | list[dict]):
    response = CLIENT.get(route)
    assert response.status_code == status
    assert response.json() == body
