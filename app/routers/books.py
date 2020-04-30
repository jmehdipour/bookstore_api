from fastapi import APIRouter, Depends
from typing import List
from app.data.mongodb import db, counter
from app.data.models import *
from app.security import auth


router = APIRouter()


@router.post("/books", dependencies=[Depends(auth.is_admin)])
async def create_book(book: Book):
    book_dict = book.dict()
    book_dict.update({"book_id": counter("books")})
    db.books.insert_one(book_dict)
    return {"detail": "book successfully created"}


@router.get("/books", dependencies=[Depends(auth.get_current_user)], response_model=List[Book])
async def get_books():
    books_list = [book for book in db.books.find({}, {"_id": 0})]
    return books_list


@router.get("/books/{book_id}", dependencies=[Depends(auth.get_current_user)])
async def get_book(book_id: int):
    book = db.books.find_one({"book_id": book_id}, {"_id": 0})
    if book:
        return book
    return {"detail": f"there is no book with id: {book_id}"}


@router.get("/categories/{category}", dependencies=[Depends(auth.get_current_user)])
async def get_books_by_category(category: str):
    books_list = [book for book in db.books.find({"category": category}, {"_id": 0})]
    if books_list:
        return books_list
    return {"detail": f"there is no book with category : {category}"}
