from asyncio import ensure_future
from datetime import datetime
from bson.objectid import ObjectId
from app.common.db import db
from app.cache.base import Cache
from app.common.utils import transform_mongo_document
from typing import List


class ProductController:
    @staticmethod
    async def fetch_all_products() -> List[dict]:
        products = await db.product.find({"enabled": {"$ne": False}}).to_list(1000)
        return products

    @staticmethod
    async def fetch_all_cached_products() -> List[dict]:
        return await Cache.get_all("product")

    @staticmethod
    async def fetch_product_by_id(product_id: str) -> dict | None:
        product = await db.product.find_one({"_id": ObjectId(product_id)})
        return product

    @staticmethod
    async def fetch_cached_product(product_id: str) -> dict | None:
        product = await Cache.get_one("product", product_id)
        if not product:
            product = ProductController.fetch_product_by_id(product_id)
            transform_mongo_document(product)
        return product

    @staticmethod
    async def create_product(product_data: dict) -> str:
        await db.product.insert_one(product_data)
        transform_mongo_document(product_data)
        ensure_future(Cache.insert_one("product", product_data))
        return product_data["id"]

    @staticmethod
    async def update_product(product_data: dict) -> int:
        _id = product_data.pop("id")
        product_data["updatedAt"] = datetime.now()
        result = await db.product.update_one(
            {"_id": ObjectId(_id)},
            {"$set": product_data}
        )
        if result.modified_count:
            product_data["id"] = _id
            ensure_future(Cache.update_one("product", product_data))
        return result.modified_count
