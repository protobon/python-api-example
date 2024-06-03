from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from app.common.constants import Env

client = AsyncIOMotorClient(getenv(Env.MONGODB.uri))
db = client[getenv(Env.MONGODB.db)]
