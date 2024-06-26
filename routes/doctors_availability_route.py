from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from config.database_config import doctor_availability
from config.auth import get_current_user
from models.doctors_availability_models import Doctors_Availability, Availability_Array
from schemas.availability_schema import serializor, list_serializor
from bson import ObjectId

availability_route = APIRouter(prefix='/availability')


@availability_route.post('/create_availability', status_code=status.HTTP_201_CREATED)
def create_availability(new_availability: Availability_Array, token: str = Depends(get_current_user)):
    try:
        print(new_availability, 'new_availability')
        for item in new_availability.Availability_data:
            available = {
                "doctor_id": ObjectId(item.doctor_id),
                "available": item.available,
                "number_of_appointments": item.number_of_appointments
            }
            doctor_availability.insert_one(available)
        return {
            "success": "saved successfully",
            "token": token
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@availability_route.get('/availability/{doctor_id}', status_code=status.HTTP_201_CREATED)
def create_availability(doctor_id: str = None, token: str = Depends(get_current_user)):
    filter_data = dict()
    try:
        if doctor_id:
            filter_data['doctor_id'] = ObjectId(doctor_id)
        availabilities = list_serializor(doctor_availability.find(filter_data))
        return {
            "message": "success",
            "availabilities": availabilities,
            token: token
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


