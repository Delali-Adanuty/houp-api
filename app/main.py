from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, SecretStr, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from .schemas import UserCreate, UserUpdate, UserResponse
import uuid


app = FastAPI()


#Dummy data
users = {
    "234":{
        "email": "eg@eg.com",
        "password": "password",
        "id": "234"
    }
}

@app.post("/create-user/")
def create_user(user_input: UserCreate):
    if user_input.email in users:
        raise HTTPException(status_code = 400, detail = "Email already exists")
    
    new_user_entry = {
        "id": uuid.uuid4(),
        "email": user_input.email,
        "password": user_input.password.get_secret_value(),
        "created_at": datetime.now()
    }

    users[user_input.email] = new_user_entry

    return new_user_entry

@app.get("/get-user-by-email/{user_email}")
def get_user(user_email: EmailStr):    
    for key, value in users.items():
        if value["email"] == user_email:
            return users[key]


    raise HTTPException(status_code = 400, detail = "User email does not exist")

@app.get("/get-user-by-id/{user_id}")
def get_user(user_id):
    if user_id not in users:
        raise HTTPException(status_code = 400, detail = "User ID does not exist")
    
    return users[user_id]

@app.patch("/update-user/{user_email}")
def update_user(user_email: EmailStr, user_update: UserUpdate):
    for key, value in users.items():
        if value["email"] == user_email:
            current_user = users[key]

            if user_update.email is not None:
                current_user["email"] = user_update.email
            
            if user_update.password is not None:
                current_user["password"] = user_update.password

            users[user_email] = current_user

            return current_user            
        

    raise HTTPException(status_code = 400, detail = "User does not exist")