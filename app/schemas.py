from pydantic import BaseModel, SecretStr, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: SecretStr

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None

class UserResponse(UserBase):
    model_config = ConfigDict(
        from_attributes = True
    )

    id: str
    created_at: datetime