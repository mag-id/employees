"""
TODO: Fields can be improved, Figure out exact requirements.
* `Employee.name` should not contain special characters
* `Employee.email` may contain part of special characters
* `Employee.company` may contain part of special characters
* `Employee.join_date` may receive different date and time formats. 
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

TEXT_FIELD = Field(None, max_length=60)


class Employee(BaseModel):
    name: Optional[str] = TEXT_FIELD
    email: Optional[str] = TEXT_FIELD
    age: Optional[int] = Field(None, ge=14, le=140)
    company: Optional[str] = TEXT_FIELD
    join_date: Optional[datetime]
    job_title: Optional[str] = TEXT_FIELD
    gender: Optional[str] = TEXT_FIELD
    salary: Optional[int] = Field(None, ge=0, le=100_000)

    @validator("join_date")
    def get_datetime_in_isoformat(cls, join_date: datetime) -> str | None:
        if join_date is not None:
            return join_date.isoformat(sep="T")
