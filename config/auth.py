import datetime
from datetime import datetime, timedelta
from config.database_config import patient_collection
from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from jose import JWTError, jwt
from bson.objectid import ObjectId
from routes.patient_route import OAuth2PasswordBearer
from schemas.patients_schema import serializor

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        user_exist = serializor(patient_collection.find_one({"_id": ObjectId(user_id)}))
        if not user_exist:
            raise credential_exception
        return token
    except JWTError:
        raise credential_exception
