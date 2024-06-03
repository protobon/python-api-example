from bson.objectid import ObjectId
from app.common.db import db


async def fetch_all_products():
    products = await db.product.find().to_list(1000)
    return products


async def fetch_product_by_id(product_id: str):
    product = await db.product.find_one({"_id": ObjectId(product_id)})
    return product


async def create_product(product_data: dict):
    result = await db.product.insert_one(product_data)
    return result.inserted_id


async def update_product(product_data: dict):
    _id = ObjectId(product_data.pop("id"))
    result = await db.product.update_one({"_id": _id}, {"$set": product_data})
    return result.modified_count
