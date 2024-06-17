from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from config.database_config import patient_collection
from schemas.patients_schema import list_serializor, serializor
from models.patient_models import New_Patient, Respond_Patient, Login_User, Patient, Single_Patient
from config.hashing import hashing_password, verify_password
from commons.common import generate_random_4_digit_number
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.auth import get_current_user, create_access_token
from bson import ObjectId

patient_route = APIRouter(prefix='/patient')


@patient_route.post('/create_patient', tags=["users"], status_code=status.HTTP_201_CREATED)
def create_patient(new_patient: Patient):
    serialized = new_patient.dict()
    email_exist = patient_collection.find_one({"email": serialized['email']})
    if email_exist:
        raise HTTPException(status_code=400, detail="email already existed")
    try:
        serialized['password'] = hashing_password(serialized['password'])
        serialized['verify'] = False
        serialized['otp'] = generate_random_4_digit_number()
        saved_user = patient_collection.insert_one(serialized)
        saved_user_id = saved_user.inserted_id
        serialized['id'] = str(saved_user_id)
        token = create_access_token(data={"id": str(saved_user_id)})
        return {
            "message": "success",
            "token": token,
            "patient": serializor(serialized)
        }
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


@patient_route.post('/verify', tags=['patients'])
def verify_user(verification: New_Patient, token: str = Depends(get_current_user)):
    try:
        serialized = verification.dict()
        email_exist = serializor(patient_collection.find_one({"_id": ObjectId(serialized['patient_id'])}))
        print(email_exist,'email_exist')
        if not serialized['otp'] == email_exist['otp']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="otp does not match")
        patient_collection.find_one_and_update({"_id": ObjectId(serialized['patient_id'])}, {"$set": {"verify": True}})
        return {
            "message": "verified",
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
