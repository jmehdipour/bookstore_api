from os import getenv
from functools import lru_cache
from pydantic import BaseSettings


class Setting(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017/"
    DATABASE_NAME: str = "bookstore"
    JWT_SECRET_KEY: str = "ThisIsSimpleKey"
    JWT_ALGORITHM: str = "HS256"
    JWT_ENABLE_EXPIRE_TOKEN: int = 30

    # MONGO_URL: str = getenv("MONGO_URL", default="mongodb://localhost:27017/")
    # DATABASE_NAME: str = getenv("DATABASE_NAME", default="bookstore")
    # JWT_SECRET_KEY: str = getenv("JWT_SECRET_KEY", default="ThisIsSimpleKey")
    # JWT_ALGORITHM: str = getenv("JWT_ALGORITHM", default="HS256")
    # JWT_ENABLE_EXPIRE_TOKEN: int = int(getenv("JWT_ENABLE_EXPIRE_TOKEN", default=30))

    class Config:
        env_file = "../../config.env"


@lru_cache()
def get_setting():
    return Setting()
