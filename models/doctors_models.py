from pydantic import BaseModel, EmailStr


class Doctor(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    specialized: str
