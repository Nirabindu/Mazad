from sqlalchemy_utils import EmailType
from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger,
    ForeignKey,
    Boolean,
    DateTime,
    Float,
    Time
)
from sqlalchemy.orm import relationship
from sql_app import database
import datetime


# Model for  User
class Individual_user(database.Base):
    __tablename__ = "individual_user"

    user_id = Column(String(255), primary_key=True, index=True)
    user_name = Column(String(100), nullable=True)
    email = Column(EmailType, unique=True)
    phone = Column(String(10), unique=True)
    password = Column(String(255))
    status = Column(Boolean, default=True)
    role = Column(String(20))
    create_at = Column(DateTime, default=datetime.datetime.today())

    post_item = relationship("Post_items", back_populates="individual_user")
    address = relationship("Address", back_populates="individual_user")
    story = relationship("Story", back_populates="individual_user")


    bs_location = relationship("Business_location", back_populates="bs_owner")
    mr_certificate = relationship("Maroof_certificate", back_populates="bs_owner")
    cr = relationship("Commercial_certificate", back_populates="bs_owner")
    vt = relationship("Vat", back_populates="bs_owner")


    # cart = relationship("Cart",back_populates="individual_user")


# models for otp


class Otp(database.Base):
    __tablename__ = "otp"
    id  = Column(Integer,primary_key=True,index=True)
    otp = Column(Integer)
    phone = Column(String(100))
    create_at = Column(DateTime)


# models for Category
class Category(database.Base):
    __tablename__ = "category"

    cat_id = Column(String(255), primary_key=True, index=True)
    category_name = Column(String(50), nullable=False, unique=True)
    status = Column(Boolean, default=True)
    image = Column(String(255))
    create_at = Column(DateTime, default=datetime.datetime.today())
    subcategory = relationship("SubCategory", back_populates="category")
    post_item = relationship("Post_items", back_populates="category")


# models for SubCategory admin
class SubCategory(database.Base):
    __tablename__ = "subcategory"

    subcategory_id = Column(String(255), primary_key=True, index=True)
    subcategory_name = Column(String(50), nullable=False, unique=True)
    image = Column(String(255))
    status = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.datetime.today())
    cat_id = Column(String(255), ForeignKey("category.cat_id"))
    category = relationship("Category", back_populates="subcategory")
    brand = relationship("Brand", back_populates="subcategory")
    post_item = relationship("Post_items", back_populates="subcategory")
    model = relationship("Models",back_populates="subcategory")


# models for Brand Name
class Brand(database.Base):
    __tablename__ = "brand"

    brand_id = Column(String(255), primary_key=True, index=True)
    brand_name = Column(String(255))
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
    subcategory_id = Column(String(255),ForeignKey("subcategory.subcategory_id"))
    brand = relationship("Brand", back_populates="model")
    subcategory = relationship("SubCategory",back_populates="model")

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
    city = Column(String(50), nullable=True)
    street = Column(String(100), nullable=True)
    building = Column(String(100), nullable=True)
    user_id = Column(String(255), ForeignKey("individual_user.user_id"))

    individual_user = relationship("Individual_user", back_populates="address")
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
    user_id = Column(String(255), ForeignKey("individual_user.user_id"))
    cat_id = Column(String(255), ForeignKey("category.cat_id"))
    subcategory_id = Column(String(255), ForeignKey("subcategory.subcategory_id"))
    brand_id = Column(String(255), ForeignKey("brand.brand_id"))
    model_id = Column(String(255), ForeignKey("models.model_id"))
    address_id = Column(String(255), ForeignKey("address.address_id"))

    individual_user = relationship("Individual_user", back_populates="post_item")
    category = relationship("Category", back_populates="post_item")
    subcategory = relationship("SubCategory", back_populates="post_item")
    address = relationship("Address", back_populates="post_item")
    model = relationship("Models", back_populates="post_item")
    brand = relationship("Brand", back_populates="post_item")
    image_for_item = relationship("Images_for_item", back_populates="post_item")
    story = relationship("Story", back_populates="post_item")
    # cart = relationship("Cart",back_populates='post_item')


class Images_for_item(database.Base):
    __tablename__ = "item_image"
    img_id = Column(String(255), primary_key=True, index=True)
    url = Column(String(255))
    item_id = Column(String(255), ForeignKey("items.item_id"))
    post_item = relationship("Post_items", back_populates="image_for_item")


class Story(database.Base):
    __tablename__ = "story"
    story_id = Column(String(255), primary_key=True, index=True)
    url = Column(String(255))
    item_id = Column(String(255), ForeignKey("items.item_id"))
    user_id = Column(String(255), ForeignKey("individual_user.user_id"))

    post_item = relationship("Post_items", back_populates="story")
    individual_user = relationship("Individual_user", back_populates="story")


# for business registration


# class Business_owner(database.Base):
#     __tablename__ = "business_owner"

#     business_owner_id = Column(String(255), primary_key=True, index=True)
#     user_name = Column(String(100))
#     phone = Column(String(100), unique=True)
#     email = Column(EmailType, unique=True)
#     password = Column(String(255))
#     status = Column(Boolean, default=True)
#     role = Column(String(20), default="business")
#     create_at = Column(DateTime, default=datetime.datetime.utcnow)

#     bs_location = relationship("Business_location", back_populates="bs_owner")
#     mr_certificate = relationship("Maroof_certificate", back_populates="bs_owner")
#     cr = relationship("Commercial_certificate", back_populates="bs_owner")
#     vt = relationship("Vat", back_populates="bs_owner")


class Business_location(database.Base):
    __tablename__ = "business_location"

    business_details_id = Column(String(255), primary_key=True, index=True)
    store_name = Column(String(100))
    store_category = Column(String(100))
    store_sign = Column(String(255), nullable=True)
    state = Column(String(100))
    district = Column(String(100))
    city = Column(String(100))
    street = Column(String(100), nullable=True)
    building = Column(String(100), nullable=True)
    business_owner_id = Column(
        String(255), ForeignKey("individual_user.user_id")
    )
    bs_owner = relationship("Individual_user", back_populates="bs_location")


class Maroof_certificate(database.Base):
    __tablename__ = "maroof"

    certificate_id = Column(String(255), primary_key=True, index=True)
    maroof_id = Column(String(100))
    maroof_expire_date = Column(String(100))
    image = Column(String(255))
    business_owner_id = Column(
        String(255), ForeignKey("individual_user.user_id")
    )

    bs_owner = relationship("Individual_user", back_populates="mr_certificate")


class Commercial_certificate(database.Base):
    __tablename__ = "commercial_certificate"

    certificate_id = Column(String(255), primary_key=True, index=True)
    commercial_id = Column(String(100), unique=True)
    commercial_expire_date = Column(String(100))
    image = Column(String(255))
    business_owner_id = Column(
        String(255), ForeignKey("individual_user.user_id")
    )

    bs_owner = relationship("Individual_user", back_populates="cr")


class Vat(database.Base):
    __tablename__ = "vat"
    vat_id = Column(String(100), primary_key=True, index=True)
    vat_number = Column(String(100), unique=True, nullable=True)
    image = Column(String(100))
    business_owner_id = Column(
        String(255), ForeignKey("individual_user.user_id")
    )

    bs_owner = relationship("Individual_user", back_populates="vt")


class Cart(database.Base):
    __tablename__ = "cart"
    cart_id = Column(Integer,primary_key = True,index=True)
    quantity = Column(Integer,default=1)
    # item_id = ForeignKey('items.item_id')
    
    # use_id = ForeignKey('individual_user.user_id')
    # post_item = relationship("Post_items",back_populates="cart")
    # individual_user = relationship("Individual_user",back_populates="cart")
