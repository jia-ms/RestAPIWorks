from typing import List

from fastapi import FastAPI, HTTPException, status

import database
from models import User, UserCreate, UserUpdate

app = FastAPI(
    title="User Service",
    description="A simple CRUD API for managing users.",
    version="1.0.0",
)


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user_in: UserCreate) -> User:
    """Create a new user."""
    return database.create_user(user_in)


@app.get("/users", response_model=List[User], tags=["Users"])
def list_users() -> List[User]:
    """Retrieve all users."""
    return database.get_all_users()


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int) -> User:
    """Retrieve a single user by id."""
    user = database.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
def replace_user(user_id: int, user_in: UserCreate) -> User:
    """Replace a user entirely (all fields required)."""
    user = database.replace_user(user_id, user_in)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.patch("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, user_in: UserUpdate) -> User:
    """Partially update a user (only send the fields you want to change)."""
    user = database.update_user(user_id, user_in)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int) -> None:
    """Delete a user by id."""
    deleted = database.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok"}