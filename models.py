from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserBase(BaseModel):
    """Fields shared across create/update/read operations."""
    name: str = Field(..., min_length=1, max_length=100, examples=["Alice Smith"])
    age: int = Field(..., ge=0, le=150, examples=[28])
    place: str = Field(..., min_length=1, max_length=100, examples=["Bengaluru"])
    gender: Gender = Field(..., examples=["female"])
    date_of_birth: date = Field(..., examples=["1997-05-14"])


class UserCreate(UserBase):
    """Schema used when creating a new user. Client does not supply an id."""
    pass


class UserUpdate(BaseModel):
    """Schema used for partial updates (PATCH). All fields optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    place: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None


class User(UserBase):
    """Schema returned to the client, includes the server-assigned id."""
    id: int

    class Config:
        from_attributes = True