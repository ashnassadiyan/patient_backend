from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime


class Patient(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    userType: Literal['admin', 'patient']
    gender: str
    dateOfBirth: datetime
    password: str


class New_Patient(BaseModel):
    otp: int
    patient_id: str


class Login_User(BaseModel):
    email: EmailStr
    password: str


class Single_Patient(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    userType: str
    gender: str
    dateOfBirth: str
    verify: bool
    otp: int


class Respond_Patient(BaseModel):
    message: str
    data: Single_Patient
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str
