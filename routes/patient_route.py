from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from config.database_config import patient_collection
from schemas.patients_schema import list_serializor, serializor
from models.patient_models import New_Patient, Respond_Patient, Login_User, Patient
from config.hashing import hashing_password, verify_password
from commons.common import generate_random_4_digit_number
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.auth import get_current_user

patient_route = APIRouter(prefix='/patient')


@patient_route.post('/create_patient', tags=["users"], response_model=New_Patient)
def create_patient(new_patient: Patient):
    serialized = new_patient.dict()
    email_exist = patient_collection.find_one({"email": serialized['email']})
    if email_exist:
        raise HTTPException(status_code=400, detail="email already existed")
    try:
        serialized['password'] = hashing_password(serialized['password'])
        serialized['verify'] = False
        serialized['otp'] = generate_random_4_digit_number()
        patient_collection.insert_one(serialized)
        return serialized
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@patient_route.get("/get_patients", tags=["patients"])
async def get_patients(firstName="", lastName="", token: str = Depends(get_current_user)):
    find_object = dict()
    if firstName:
        find_object['firstName'] = firstName
    if lastName:
        find_object['lastName'] = lastName
    patients = list_serializor(patient_collection.find(find_object))
    print(patients, 'patients')
    return {
        "message": "success",
        "patients": patients
    }


@patient_route.post('/verify', tags=['patients'], response_model=Respond_Patient)
def verify_user(verification: New_Patient, token: str = Depends(get_current_user)):
    try:
        serialized = verification.dict()
        user_exit = serializor(patient_collection.find_one({'email': serialized['email']}))
        if not user_exit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not serialized['otp'] == user_exit['otp']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="otp does not match")
        updated_user = serializor(
            patient_collection.find_one_and_update({"email": serialized['email']}, {"$set": {"verify": True}}))
        return updated_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
