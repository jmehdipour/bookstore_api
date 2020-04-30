import schedule
from datetime import datetime, timedelta
from app.data.mongodb import db


def expire_carts():
    now = datetime.now()
    timeout = 3600 * 2
    threshold = now - timedelta(timeout)

    carts = db.carts.find({"last_update": {"$lt": threshold}})

    for cart in carts:
        for item in db.items.find({"item_id": {"$in": cart["items"]}}):
            db.books.update_one(
                {"book_id": item.book_id},
                {"qty_all": {"$inc": item.qty}}
            )

    cart_ids = [cart["cart_id"] for cart in carts]
    query = {"cart_id": {"$in": cart_ids}}
    db.carts.delete_many(query)
    db.users.update_many(query, {"$set": {"cart_id": None}})


schedule.every().hour.do(expire_carts)
