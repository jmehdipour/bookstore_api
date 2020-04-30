from fastapi import APIRouter, Depends
from app.data.mongodb import db, counter
from app.data.models import *
from app.security import auth

router = APIRouter()


@router.get("/users/{user_id}/orders", dependencies=[Depends(auth.is_admin)])
async def get_user_orders(user_id: int):
    orders = db.orders.find({"user_id": user_id}, {"_id": 0})
    return list(orders)


@router.get("/orders", dependencies=[Depends(auth.is_admin)])
async def get_user_orders():
    orders = db.orders.find({}, {"_id": 0})
    return list(orders)


@router.get("/users/me/orders")
async def get_my_orders(current_user: UserInDB = Depends(auth.get_current_user)):
    orders = db.orders.find({"user_id": current_user.user_id}, {"_id": 0})
    return list(orders)
