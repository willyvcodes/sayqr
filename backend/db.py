import os
import motor.motor_asyncio

from dotenv import load_dotenv
from beanie import Document
from fastapi_users.db import BeanieBaseUser
from fastapi_users_db_beanie import BeanieUserDatabase


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_URI, tls=True, tlsAllowInvalidCertificates=True
)
db = client.sayqr


class User(BeanieBaseUser, Document):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
