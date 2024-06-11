from datetime import datetime
from fastapi import APIRouter, Body
from loguru import logger
from app.schema.base import build_response
from app.schema.product import (ProductSchema, ProductResponse,
                                FetchProductsSchema, FetchProductsResponse,
                                CreateProductSchema)
from app.controller.product import ProductController

router = APIRouter(
    prefix="/product",
    tags=["product"]
)


@router.get(path="/all",
            description="Fetch all products",
            response_model=FetchProductsResponse)
async def fetch_products():
    try:
        products = await ProductController.fetch_all_cached_products()
        product_schemas = [ProductSchema(**product) for product in products]
        fetch_products_schema = FetchProductsSchema(products=product_schemas, total=len(product_schemas))
        return build_response(success=True, data=fetch_products_schema, status_code=200)
    except Exception:
        logger.exception("fetch_products")
        return build_response(success=False, error="An error occurred while fetching products", status_code=500)


@router.get(path="/{product_id}",
            description="Get a product by id",
            response_model=ProductResponse)
async def get_product(product_id: str):
    try:
        product = await ProductController.fetch_cached_product(product_id)
        if not product:
            return build_response(success=False, error="No records found", status_code=404)
        product_schema = ProductSchema(**product)
        return build_response(success=True, data=product_schema, status_code=200)
    except Exception:
        logger.exception("get_product")
        return build_response(success=False, error="An error occurred while fetching this product", status_code=500)


@router.post(path="/new",
             description="Create a new product",
             response_model=ProductResponse)
async def new_product(product: CreateProductSchema = Body(...)):
    try:
        product_dict = product.model_dump()
        product_dict["createdAt"] = datetime.now()
        product_dict["id"] = await ProductController.create_product(product_dict)
        product_schema = ProductSchema(**product_dict)
        return build_response(success=True, data=product_schema, status_code=200)
    except Exception:
        logger.exception("create_product")
        return build_response(success=False, error="An error occurred while creating a new product", status_code=500)


@router.put(path="/update",
            description="Update a product",
            response_model=ProductResponse)
async def product_update(product: ProductSchema = Body(...)):
    try:
        product_dict = product.model_dump()
        product_dict["updatedAt"] = datetime.now()
        updated = await ProductController.update_product(product_dict)
        if not updated:
            return build_response(success=False,
                                  error=f"product {product_dict['id']} was not updated",
                                  status_code=403)

        product_schema = ProductSchema(**product_dict)
        return build_response(success=True, data=product_schema, status_code=200)
    except Exception:
        logger.exception("product_update")
        return build_response(success=False, error="An error occurred while updating a product", status_code=500)
