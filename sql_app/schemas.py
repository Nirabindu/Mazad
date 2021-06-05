from sql_app.database import Base
from sqlalchemy import orm
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Category(BaseModel):
    category_name: str
    image: str


class Get_category(BaseModel):
    category_name:str
    class Config():
        orm_mode = True


class SubCategory(BaseModel):
    subcategory_name: str
    image: str



class Get_SubCategory(BaseModel):
    subcategory_name: str
    class Config():
        orm_mode = True


class Brand(BaseModel):
    brand_name: str



class Get_brand(BaseModel):
    brand_name: str
    class Config():
        orm_mode = True


class Models(BaseModel):
    model_name: str



class Get_models(BaseModel):
    model_name:str
    class Config():
        orm_mode = True



class Post_items(BaseModel):
    category_name: str
    subcategory_name: str
    brand_name: str
    model_name: Optional[str]
    style: Optional[str]
    feature: Optional[str]
    milage: Optional[str]
    km_driven: Optional[str]
    size: Optional[str]
    condition: str
    firm_on_my_price: bool
    returnable: bool
    shipping: str
    shipping_method: str
    description: str
    set_product_weight: str
    set_price: float
    date: datetime

    class Config:
        orm_mode = True


class Address(BaseModel):
    latitude: float
    longitude: float
    state: str
    district: str


class Get_address(BaseModel):
    state: Optional[str]
    district: Optional[str]
    address_get: Optional[str]

    class Config:
        orm_mode = True


class Images_for_item(BaseModel):
    url: str

    class Config:
        orm_mode = True


class get_item(Post_items):
    address: Get_address
    image_for_item: List[Images_for_item] = []

