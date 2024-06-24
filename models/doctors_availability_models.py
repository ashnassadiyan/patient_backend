from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class Doctors_Availability(BaseModel):
    doctor_id: str
    available: datetime
    number_of_appointments: int = Field(default=10)


class Availability_Array(BaseModel):
    Availability_data: List[Doctors_Availability]
