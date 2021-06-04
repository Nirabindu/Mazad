import re
from routers.Category import post_item
from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger,
    ForeignKey,
    Boolean,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import column, false, table
from sqlalchemy.sql.sqltypes import DATE
from sql_app import database
import datetime


# Model for Individual User


# models for Category
class Category(database.Base):
    __tablename__ = "category"

    cat_id = Column(String(255), primary_key=True, index=True)
    category_name = Column(String(50), nullable=False, unique=True)
    status = Column(Boolean, default=True)
    image = Column(String(255))
    create_at = Column(DateTime, default=datetime.datetime.utcnow)
    subcategory = relationship("SubCategory", back_populates="category")
    post_item = relationship("Post_items", back_populates="category")


# models for SubCategory
class SubCategory(database.Base):
    __tablename__ = "subcategory"

    subcategory_id = Column(String(255), primary_key=True, index=True)
    subcategory_name = Column(String(50), nullable=False, unique=True)
    image = Column(String(255))
    status = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)
    cat_id = Column(String(255), ForeignKey("category.cat_id"))
    category = relationship("Category", back_populates="subcategory")
    brand = relationship("Brand", back_populates="subcategory")
    post_item = relationship("Post_items", back_populates="subcategory")


# models for Brand Name
class Brand(database.Base):
    __tablename__ = "brand"

    brand_id = Column(String(255), primary_key=True, index=True)
    brand_name = Column(String(255), unique=True)
    subcategory_id = Column(String(255), ForeignKey("subcategory.subcategory_id"))
    subcategory = relationship("SubCategory", back_populates="brand")
    model = relationship("Models", back_populates="brand")
    post_item = relationship("Post_items", back_populates="brand")


# models for Models under brand
class Models(database.Base):
    __tablename__ = "models"

    model_id = Column(String(255), primary_key=True, index=True)
    model_name = Column(String(255), unique=True)
    brand_id = Column(String(255), ForeignKey("brand.brand_id"))
    brand = relationship("Brand", back_populates="model")
    post_item = relationship("Post_items", back_populates="model")


# model for storing address
class Address(database.Base):
    __tablename__ = "address"

    address_id = Column(String(255), primary_key=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address_get = Column(String(255), nullable=True)
    state = Column(String(50), nullable=True)
    district = Column(String(50), nullable=True)
    user_id = Column(String(255))
    post_item = relationship("Post_items", back_populates="address")


class Post_items(database.Base):
    __tablename__ = "items"

    item_id = Column(String(255), primary_key=True, index=True)
    category_name = Column(String(50))
    subcategory_name = Column(String(50))
    brand_name = Column(String(50))
    model_name = Column(String(50), nullable=True)

    style = Column(String(50), nullable=True)
    feature = Column(String(50), nullable=True)
    milage = Column(String(50), nullable=True)
    km_driven = Column(String(50), nullable=True)
    size = Column(String(50), nullable=True)
    condition = Column(String(50), nullable=True)
    firm_on_my_price = Column(Boolean, default=True)
    returnable = Column(Boolean, default=True)
    shipping = Column(String(50), nullable=False)
    shipping_method = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    set_product_weight = Column(String(50), nullable=False)
    set_price = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(String(255))
    cat_id = Column(String(255), ForeignKey("category.cat_id"))
    subcategory_id = Column(String(255), ForeignKey("subcategory.subcategory_id"))
    brand_id = Column(String(255), ForeignKey("brand.brand_id"))
    model_id = Column(String(255), ForeignKey("models.model_id"))
    address_id = Column(String(255), ForeignKey("address.address_id"))

    category = relationship("Category", back_populates="post_item")
    subcategory = relationship("SubCategory", back_populates="post_item")
    address = relationship("Address", back_populates="post_item")
    model = relationship("Models", back_populates="post_item")
    brand = relationship("Brand", back_populates="post_item")
    image_for_item = relationship("Images_for_item", back_populates="post_item")


class Images_for_item(database.Base):
    __tablename__ = "item_image"

    img_id = Column(String(255), primary_key=True, index=True)
    url = Column(String(255))
    item_id = Column(String(255), ForeignKey("items.item_id"))
    post_item = relationship("Post_items", back_populates="image_for_item")
