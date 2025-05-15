from fastapi import FastAPI, HTTPException, status, APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# --- Database Setup ---
client = MongoClient("mongodb://localhost:27017")
db = client['starcoach-clinic']
users_col = db['users']
doctors_col = db['doctors']
appointments_col = db['appointments']

# --- Pydantic Schemas ---
class UserCreate(BaseModel):
    name: str
    email: str

class User(UserCreate):
    id: Optional[str] = Field(alias="_id")

    class Config:
        populate_by_name = True

class DoctorCreate(BaseModel):
    name: str
    specialty: str

class Doctor(DoctorCreate):
    id: Optional[str] = Field(alias="_id")

    class Config:
        populate_by_name = True

class AppointmentCreate(BaseModel):
    user_id: str
    doctor_id: str
    datetime: datetime
    reason: Optional[str]

class Appointment(AppointmentCreate):
    id: Optional[str] = Field(alias="_id")

    class Config:
        populate_by_name = True

# --- FastAPI App ---
app = FastAPI()

# --- User Endpoints ---
user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    res = users_col.insert_one(user.dict())
    return User(id=str(res.inserted_id), **user.dict())

@user_router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    user = users_col.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(404, "User not found")
    user["_id"] = str(user["_id"])
    return user

@user_router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user: UserCreate):
    result = users_col.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
    if result.matched_count == 0:
        raise HTTPException(404, "User not found")
    updated_user = users_col.find_one({"_id": ObjectId(user_id)})
    updated_user["_id"] = str(updated_user["_id"])
    return updated_user

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    result = users_col.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "User not found")

# --- Doctor Endpoints ---
doctor_router = APIRouter(prefix="/doctors", tags=["doctors"])

@doctor_router.post("", response_model=Doctor, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: DoctorCreate):
    res = doctors_col.insert_one(doctor.dict())
    return Doctor(id=str(res.inserted_id), **doctor.dict())

@doctor_router.get("/{doctor_id}", response_model=Doctor)
def get_doctor(doctor_id: str):
    doc = doctors_col.find_one({"_id": ObjectId(doctor_id)})
    if not doc:
        raise HTTPException(404, "Doctor not found")
    doc["_id"] = str(doc["_id"])
    return doc

@doctor_router.put("/{doctor_id}", response_model=Doctor)
def update_doctor(doctor_id: str, doctor: DoctorCreate):
    result = doctors_col.update_one({"_id": ObjectId(doctor_id)}, {"$set": doctor.dict()})
    if result.matched_count == 0:
        raise HTTPException(404, "Doctor not found")
    updated_doc = doctors_col.find_one({"_id": ObjectId(doctor_id)})
    updated_doc["_id"] = str(updated_doc["_id"])
    return updated_doc

@doctor_router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: str):
    result = doctors_col.delete_one({"_id": ObjectId(doctor_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Doctor not found")

# --- Appointment Endpoints ---
appt_router = APIRouter(prefix="/appointments", tags=["appointments"])

@appt_router.post("", response_model=Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appt: AppointmentCreate):
    user_oid = ObjectId(appt.user_id)
    doctor_oid = ObjectId(appt.doctor_id)

    if not users_col.find_one({"_id": user_oid}):
        raise HTTPException(404, "User not found")
    if not doctors_col.find_one({"_id": doctor_oid}):
        raise HTTPException(404, "Doctor not found")

    res = appointments_col.insert_one(appt.dict())
    return Appointment(id=str(res.inserted_id), **appt.dict())

@appt_router.get("/{appt_id}", response_model=Appointment)
def get_appointment(appt_id: str):
    appt = appointments_col.find_one({"_id": ObjectId(appt_id)})
    if not appt:
        raise HTTPException(404, "Appointment not found")
    appt["_id"] = str(appt["_id"])
    appt["user_id"] = str(appt["user_id"])
    appt["doctor_id"] = str(appt["doctor_id"])
    return appt

@appt_router.get("", response_model=List[Appointment])
def list_appointments():
    appts = list(appointments_col.find())
    for appt in appts:
        appt["_id"] = str(appt["_id"])
        appt["user_id"] = str(appt["user_id"])
        appt["doctor_id"] = str(appt["doctor_id"])
    return appts

@appt_router.delete("/{appt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appt_id: str):
    result = appointments_col.delete_one({"_id": ObjectId(appt_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Appointment not found")

# --- Include Routers ---
app.include_router(user_router)
app.include_router(doctor_router)
app.include_router(appt_router)

# --- Run with: uvicorn appointment:app --reload ---
