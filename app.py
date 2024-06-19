from fastapi import FastAPI
from routes.patient_route import patient_route
from routes.auth_route import auth_route
from routes.doctors_route import doctors_route
from routes.doctors_availability_route import availability_route
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",  # Adjust as per your frontend server
    "https://patient-frontend-six.vercel.app"  # Add your frontend domains here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

app.include_router(patient_route)
app.include_router(auth_route)
app.include_router(doctors_route)
app.include_router(availability_route)


@app.get('/index')
def index():
    return {
        "success": "server is working"
    }
