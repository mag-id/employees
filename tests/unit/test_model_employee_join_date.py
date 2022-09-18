from datetime import datetime, timedelta, timezone

from pydantic.error_wrappers import ValidationError
from pytest import mark, param, raises

from app.models import Employee


def test_join_date_none():
    assert Employee().join_date is None
    assert Employee(join_date=None).join_date is None


@mark.parametrize(
    "raw",
    [
        param("", id="empty string"),
        param(" ", id="space string"),
        param("no date str", id="not datetime string"),
        param("2000-01-01", id="datetime string in an unrecognized format"),
    ]
)
def test_join_date_wrong_formats(raw: str | datetime):
    with raises(ValidationError, match="invalid datetime format"):
        Employee(join_date=raw)


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
