from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

from app.schema.base import BodySchema, ResponseSchema


"""  PRODUCT SCHEMAS
"""


class ProductSchema(BaseModel):
    id: str = Field(None, description="Unique document id")
    title: str = Field(None, description="Product title", min_length=2, max_length=125)
    quantity: int = Field(0, description="Quantity (units)", ge=0)
    createdAt: datetime = Field(None, description="Creation date")
    updatedAt: datetime = Field(None, description="Last update")


class ProductBody(BodySchema):
    data: ProductSchema


class ProductResponse(ResponseSchema):
    body: ProductBody


""" CREATE
"""


class CreateProductSchema(BaseModel):
    title: str = Field(None, description="Product title", min_length=2, max_length=125)
    quantity: int = Field(0, description="Quantity (units)", ge=0)


""" UPDATE
"""


class UpdateProductSchema(BaseModel):
    id: str = Field(None, description="Unique document id")
    title: Optional[str] = Field(None, description="Product title", min_length=2, max_length=125)
    quantity: Optional[int] = Field(None, description="Quantity (units)", ge=0)


class UpdateProductBody(BodySchema):
    data: UpdateProductSchema


class UpdateProductResponse(ResponseSchema):
    body: UpdateProductBody


""" FETCH
"""


class FetchProductsSchema(BaseModel):
    products: List[ProductSchema] = []
    total: int = 0


class FetchProductsBody(BodySchema):
    data: FetchProductsSchema


class FetchProductsResponse(ResponseSchema):
    body: FetchProductsBody


""" DELETE
"""


class DeleteProductSchema(BaseModel):
    message: str


class DeleteProductBody(BodySchema):
    data: DeleteProductSchema


class DeleteProductResponse(ResponseSchema):
    body: DeleteProductBody
