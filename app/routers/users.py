from fastapi import APIRouter, Depends
from app.data.mongodb import db, counter
from app.data.models import *
from app.security import auth

router = APIRouter()


@router.post("/users")
async def create_user(user: UserSignUp):
    user_dict = user.dict()
    user_dict.update({"user_id": counter("users"), "hashed_password": auth.get_password_hash(user_dict["password"])})
    del user_dict["password"]
    db.users.insert_one(user_dict)
    return {"detail": "user successfully created"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(auth.get_current_user)):
    return current_user


@router.put("/users/me")
async def update_user(user_update: UserUpdate, current_user: UserInDB = Depends(auth.get_current_user)):
    if not user_update.dict(exclude_unset=True):
        return {"detail": "update body is empty"}
    db.users.update_one({"username": current_user.username}, {"$set": user_update.dict(exclude_unset=True)})
    return {"detail": "user updated successfully"}
