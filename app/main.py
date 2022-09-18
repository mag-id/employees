from fastapi import FastAPI, Depends
from app.database import find_employees
from app.models import Employee

APP = FastAPI()


@APP.get("/employees", response_model=list[Employee])
async def get_employees(query: Employee = Depends()) -> list[Employee]:
    return find_employees(query)
