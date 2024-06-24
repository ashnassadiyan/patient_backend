from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from models.doctors_models import Doctor
from config.database_config import doctor_collection
from schemas.doctors_schema import list_serializor, serializor
from config.auth import get_current_user
from bson import ObjectId

doctors_route = APIRouter(prefix='/doctor')


@doctors_route.post('/create_doctor', status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: Doctor, token: str = Depends(get_current_user)):
    try:
        serialized = doctor.dict()
        existing_doctor = doctor_collection.find_one({"email": serialized['email']})
        if existing_doctor:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='email already exist')
        doctor_collection.insert_one(serialized)
        return {
            "message": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@doctors_route.get('/get_doctors', status_code=status.HTTP_200_OK)
def get_doctors(firstName: str = "", lastName: str = "", specialized: str = "", page: int = 1, limit: int = 10,
                token: str = Depends(get_current_user)):
    filter_fields = dict()
    try:
        if firstName:
            filter_fields['firstName'] = firstName
        if specialized:
            filter_fields['specialized'] = specialized
        if lastName:
            filter_fields['lastName'] = lastName
        doctors = list_serializor(doctor_collection.find(filter_fields).skip((page - 1) * limit).limit(limit))
        doctors_count = doctor_collection.count_documents(filter_fields)
        return {
            "message": "success",
            'data': doctors,
            "total": doctors_count
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@doctors_route.put('/update_doctor/{doctor_id}', status_code=status.HTTP_200_OK)
def create_doctor(doctor_id: str, doctor: Doctor, token: str = Depends(get_current_user)):
    try:
        serialized = doctor.dict()
        existing_doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})
        if not existing_doctor:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='data cannot be found')
        doctor_collection.update_one({"_id": ObjectId(doctor_id)}, {"$set": serialized})
        return {
            "message": "updated"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@doctors_route.get('/get_doctor/{doctor_id}', status_code=status.HTTP_200_OK)
def create_doctor(doctor_id: str, token: str = Depends(get_current_user)):
    try:
        existing_doctor = serializor(doctor_collection.find_one({"_id": ObjectId(doctor_id)}))
        if not existing_doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='data cannot be found')
        return {
            "message": "success",
            "data": existing_doctor
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


