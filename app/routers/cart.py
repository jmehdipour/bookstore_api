from fastapi import APIRouter, Depends
from app.data.mongodb import db, counter
from app.data.models import *
from app.security import auth

router = APIRouter()


@router.post("/items")
async def add_item_to_shopping_cart(item: Item, current_user: UserInDB = Depends(auth.get_current_user)):
    book = db.books.find_one({"book_id": item.book_id})
    if not book:
        return {"detail": f"there is no book with id: {item.book_id}"}
    if item.qty > book["qty_all"]:
        return {"detail": f"There are not enough copies of the book: {book.name}."}

    current_user.add_item_cart(BookInDB(**book), item.qty)
    return {"detail": "item added successfully to your cart."}


@router.get("/users/me/cart")
async def get_my_shopping_cart_items(current_user: UserInDB = Depends(auth.get_current_user)):
    return current_user.get_cart_items()


@router.get("/users/me/checkout")
async def checkout(current_user: UserInDB = Depends(auth.get_current_user)):
    order = current_user.checkout()
    return order
