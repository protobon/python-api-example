import orjson
from redis import StrictRedis
from typing import List
from os import getenv

from app.common.constants import Env


class Cache:
    client = StrictRedis(host=getenv(Env.REDIS.host),
                         port=getenv(Env.REDIS.port),
                         password=getenv(Env.REDIS.password),
                         db=0,
                         decode_responses=True,
                         socket_keepalive=True)

    @classmethod
    async def get_one(cls, collection: str, document_id: str) -> dict | None:
        key = f'{collection}:{document_id}'
        value = cls.client.get(key)
        return orjson.loads(value) if value else None

    @classmethod
    async def get_all(cls, collection: str) -> List[dict]:
        pattern = f'{collection}:*'
        keys = cls.client.keys(pattern)
        values = cls.client.mget(keys)
        return [orjson.loads(value) for value in values if value is not None]

    @classmethod
    async def insert_one(cls, collection: str, doc: dict):
        key = f"{collection}:{doc['id']}"
        cls.client.set(name=key, value=orjson.dumps(doc))

    @classmethod
    async def update_one(cls, collection: str, doc: dict):
        item = await cls.get_one(collection, doc["id"])
        if item:
            if doc.get("enabled") is False:
                await cls.delete_one(collection, doc["id"])
                return
            for key in doc.keys():
                item[key] = doc[key]
            await cls.insert_one(collection, item)

    @classmethod
    async def delete_one(cls, collection: str, document_id: str):
        key = f"{collection}:{document_id}"
        await cls.client.delete(key)
