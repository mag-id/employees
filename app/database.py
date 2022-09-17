import os
from typing import Collection
from pymongo import MongoClient
from app.models import Employee


def find_employees(query: Employee) -> list[Employee]:
    kwargs = query.dict(exclude_none=True)
    found = connect_to_employees().find(kwargs)
    return list(map(Employee.parse_obj, found))


def connect_to_employees() -> Collection:
    return MongoClient(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        username=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
    ).db.employees
