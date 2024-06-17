from fastapi.security import OAuth2PasswordRequestForm
from config.database_config import patient_collection
from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from config.hashing import verify_password
from models.patient_models import Respond_Patient, Login_User, Token
from routes.patient_route import OAuth2PasswordBearer
from schemas.patients_schema import serializor
from config.auth import create_access_token

auth_route = APIRouter(prefix='/auth')


@auth_route.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_exist = serializor(patient_collection.find_one({"email": form_data.email}))
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(form_data.password, user_exist['password']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    access_token = create_access_token(
        data={"id": user_exist['id']})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_route.post('/login', tags=['auth'], response_model=Respond_Patient, status_code=status.HTTP_200_OK)
def login(login_user: Login_User):
    try:
        user_exist = serializor(patient_collection.find_one({"email": login_user.email}))
        if not user_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        if not verify_password(login_user.password, user_exist['password']):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
        token = create_access_token(
            data={"id": user_exist['id']})
        return Respond_Patient(message="success", data=user_exist,token=token)
    except Exception as e:
        print(f"patient error {e}")
        raise HTTPException(status_code=500, detail=str(e))
