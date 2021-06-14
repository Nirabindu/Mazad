from sql_app.database import Base
from sql_app import models
from sqlalchemy import orm
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class User_registration(BaseModel):
    user_name:str
    email:str
    phone:str
    password:str




class User_login(BaseModel):
    phone_or_email:str
    password:str

    
class User_update(BaseModel):
    user_name:str
    email:str
    phone:str


class Chang_password(BaseModel):
    current_password:str
    new_password:str
    confirm_password:str





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
    latitude: Optional[float]=None
    longitude: Optional[float]=None
    state: Optional[str]=None
    district: Optional[str]=None
    city:Optional[str]=None
    street:Optional[str]=None
    Building:Optional[str]=None
    class Config:
        orm_mode = True

class Get_address(BaseModel):
    state: Optional[str]=None
    district: Optional[str]=None
    city:Optional[str]=None
    street:Optional[str]=None
    Building:Optional[str]=None
    address_get:Optional[str]=None
    class Config:
        orm_mode = True



class Images_for_item(BaseModel):
    url: str

    class Config:
        orm_mode = True


class get_item(Post_items):
    address: Get_address
    image_for_item: List[Images_for_item] = []


class Upload_story(BaseModel):
    url : str
    class Config():
        orm_mode = True


class Get_story(BaseModel):
    url:str
    post_item:Post_items
    






# for b2c
class Business_registration(BaseModel):
    user_name :str
    phone:str
    email:str
    password:str

class Business_login(BaseModel):
    phone_or_email:str
    password:str


# class Business_location()













class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user: Optional[str] = None