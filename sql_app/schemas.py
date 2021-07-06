from sql_app.database import Base
from sql_app import models
from sqlalchemy import orm
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# schemas for user registration
class User_registration(BaseModel):
    user_name: str
    email: str
    phone: str
    password: str
    confirm_password: str


# schemas for user login
class User_login(BaseModel):
    phone_or_email: str
    password: str


# schemas for OTP
class Send_otp(BaseModel):
    phone: str


class Verify_otp(BaseModel):
    enter_otp: int


# user profile related
class Show_profile_data(BaseModel):
    user_name: str
    email: str
    phone: str

    class Config:
        orm_mode = True


class User_update(BaseModel):
    user_name: str
    email: str
    phone: str


class Chang_password(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class New_password(BaseModel):
    new_password: str
    confirm_password: str


# individual function
# post item
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


# For getting address
class Address(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    state: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    Building: str

    class Config:
        orm_mode = True

# get all address
class Get_address(BaseModel):
    address_id:str
    state: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    Building: Optional[str] = None
    address_get: Optional[str] = None
    user_id:str

    class Config:
        orm_mode = True


class Images_for_item(BaseModel):
    url: str

    class Config:
        orm_mode = True


#get items

class Get_item(Post_items):
    address: Get_address
    image_for_item: List[Images_for_item] = []

    class Config:
        orm_mode = True


# get minimal details of items
class Get_minimal_details_of_item(BaseModel):
    item_id:str
    subcategory_name: str
    brand_name: str
    model_name: Optional[str]
    shipping: str
    description: str
    set_price: float
    date: datetime
    class Config:
        orm_mode = True





class Upload_story(BaseModel):
    url: str

    class Config:
        orm_mode = True


class Get_story(BaseModel):
    url: str
    post_item: Post_items


class Search(BaseModel):
    item_id: str
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
    set_price: float
    date: datetime


# for b2c
class Business_registration(BaseModel):
    user_name: str
    phone: str
    email: str
    password: str
    confirm_password: str


# For admin side
class Category(BaseModel):
    category_name: str
    image: str


class Sub_category(BaseModel):
    subcategory_name: str
    image: str


class Brand(BaseModel):
    subcategory_name: str
    brand_name: str


class Models(BaseModel):
    subcategory_name: str
    brand_name: str
    model_name: str




#get all data
class Get_category(BaseModel):
    cat_id: str
    category_name: str
    image: str

    class Config:
        orm_mode = True


class Get_SubCategory(BaseModel):
    subcategory_id: str
    subcategory_name: str
    image: str

    class Config:
        orm_mode = True


class Get_brand(BaseModel):
    brand_id: str
    brand_name: str

    class Config:
        orm_mode = True


class Get_models(BaseModel):
    model_id:str
    model_name: str

    class Config:
        orm_mode = True


# cart related


class Cart(BaseModel):
    item_id: str
    quantity: int


# class Get_cart(BaseModel):


# class Cart_item(BaseModel):


# For token related
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user: Optional[str] = None
