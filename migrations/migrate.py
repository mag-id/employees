"""
TODO: improve migrations' / schemas' handling
* research about migrations' / schemas' handling for NoSQL DBs
* find an existing solution
* write custom realization
"""
import os
from sys import argv
from json import load
from pathlib import Path
from pymongo import MongoClient


# TODO: it is not DRY (see retrieve_employees in app.database), but
# let's stay it as is for now because the migration approach may change.
EMPLOYEES_COLLECTION = MongoClient(
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    username=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
).db.employees


def migrate(migration: str):
    if EMPLOYEES_COLLECTION.count_documents(filter={}) == 0:
        with open(Path(migration), mode="r") as file:
            EMPLOYEES_COLLECTION.insert_many(load(file))


if __name__ == "__main__":
    migrate(argv[1])
