from datetime import datetime
from pydantic import BaseModel
from typing import Any


class Doctors_Availability(BaseModel):
    doctor_id: str
    available: datetime


