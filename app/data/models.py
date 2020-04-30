from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId as BsonObjectId
from app.data.mongodb import db, counter
from datetime import datetime


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class Item(BaseModel):
    book_id: int
    qty: int


class ItemInDB(Item):
    item_id: int
    book_name: str
    book_price: int


class Book(BaseModel):
    name: str
    author: str
    price: int
    category: str
    qty_all: int


class BookInDB(Book):
    book_id: int


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    address: str = None
    phone_number: str = None


class UserSignUp(User):
    password: str


class UserInDB(User):
    user_id: int
    hashed_password: str
    is_admin: bool = None
    cart_id: int = None

    def add_item_cart(self, book: BookInDB, qty: int):
        item = ItemInDB(item_id=counter("items"), qty=qty, book_id=book.book_id, book_name=book.name,
                        book_price=book.price)
        db.items.insert_one(item.dict())
        if not self.cart_id:
            shopping_cart = ShoppingCart(cart_id=counter("carts"), last_update=datetime.now(), items=[item.item_id])
            db.carts.insert_one(shopping_cart.dict())
            db.users.update_one({"user_id": self.user_id}, {"$set": {"cart_id": shopping_cart.cart_id}})
        else:
            db.carts.update_one(
                {"cart_id": self.cart_id},
                {
                    "$push": {"items": item.item_id},
                    "$set": {"last_update": datetime.now()}
                }
            )
        db.books.update_one({"book_id": book.book_id}, {"$inc": {"qty_all": -qty}})
        return True

    def get_cart_items(self):
        cart = db.carts.find_one({"cart_id": self.cart_id})
        cart_items = db.items.find(
            {"item_id": {"$in": cart["items"]}},
            {"_id": 0}
        )
        return list(cart_items)

    def checkout(self):
        cart_items = self.get_cart_items()
        items_cost_list = [item["book_price"] * item["qty"] for item in cart_items]
        cost_all = sum(items_cost_list)
        items_ids = [item["item_id"] for item in cart_items]
        order = Order(order_id=counter("orders"), user_id=self.user_id, cost=cost_all, items=items_ids, created_at=datetime.now())
        db.orders.insert_one(order.dict())
        return order


class UserUpdate(User):
    username: str = None
    password: str = None


class ShoppingCart(BaseModel):
    cart_id: int
    items: List[int] = []
    last_update: datetime


class Order(BaseModel):
    order_id: int
    user_id: int
    cost: int
    items: List[int]
    created_at: datetime
