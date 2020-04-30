from fastapi import FastAPI, HTTPException, status
from app.security import auth
from app.data.models import *
from app.data.mongodb import db, counter
from app.routers import users
from app.routers import books
from app.routers import cart
from app.routers import orders

app = FastAPI(
    title="Bookstore project",
    description="a very simple bookstore Api",
)
app.include_router(auth.router)
app.include_router(users.router, tags=["users"])
app.include_router(books.router, tags=["books"])
app.include_router(cart.router, tags=["cart"])
app.include_router(orders.router, tags=["orders"])


@app.post("/init", tags=["init"], description="initialize the api")
async def init(user: UserSignUp):
    if db.users.find_one({"is_admin": True}):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The program has already been initialized"
        )
    user_dict = user.dict()
    user_dict.update({"user_id": counter("users"), "is_admin": True,
                      "hashed_password": auth.get_password_hash(user_dict["password"])})
    del user_dict["password"]
    db.users.insert_one(user_dict)
    return {"detail": "Application initialized successfully."}
