from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class UserBase(SQLModel):
    email: str


class User(UserBase, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    hashed_password: str

    rides_as_rider: List["Ride"] = Relationship(
            back_populates="rider",
            sa_relationship_kwargs={"foreign_keys": "Ride.rider_id"}
    )
        
    rides_as_driver: List["Ride"] = Relationship(
            back_populates="driver",
            sa_relationship_kwargs={"foreign_keys": "Ride.driver_id"}
    )

class UserRead(UserBase):
    id: int



class RideBase(SQLModel):
    pickup_location: str
    dropoff_location: str


class RideCreate(RideBase):
    pass

class Ride(RideBase, table=True):
    __tablename__ = 'rides'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    status: str
    
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    driver_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    driver: Optional[User] = Relationship(
        back_populates="rides_as_driver",
        sa_relationship_kwargs={"foreign_keys": "[Ride.driver_id]"}
    )

    rider_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    
    rider: Optional[User] = Relationship(
        back_populates="rides_as_rider",
        sa_relationship_kwargs={"foreign_keys": "[Ride.rider_id]"}
    )



class RideRead(RideBase):
    id: int
    status: str
    requested_at: datetime
    rider_id: int