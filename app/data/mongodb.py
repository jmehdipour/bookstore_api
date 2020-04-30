from pymongo import MongoClient, ReturnDocument
from app.config.config import get_setting


client = MongoClient(get_setting().MONGO_URL)
db = client[get_setting().DATABASE_NAME]


def counter(collection_name):
    result = db.counters.find_one_and_update(
        {"_id": collection_name},
        {"$inc": {"count": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return result.get("count")
