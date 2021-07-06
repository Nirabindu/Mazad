from sql_app import models
from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError
import random
import twilio
from twilio.rest import Client


# user data validation
def user_data_validation(db, request):
    try:
        valid = validate_email(request.email)
        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"not a valid email"
        )

    check_email = (
        db.query(models.Individual_user)
        .filter(request.email == models.Individual_user.email)
        .first()
    )
    check_mobile = (
        db.query(models.Individual_user)
        .filter(request.phone == models.Individual_user.phone)
        .first()
    )

    if check_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Email already register"
        )
    if len(request.phone) != 10:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Phone number must be ten digit",
        )

    if check_mobile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"mobile already register"
        )

    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"password must be greater then 6 digit",
        )

    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"password not matched as above",
        )


# getting user by checking mobile and email
def check_user(
    db,
    current_user,
):

    current_user_data_by_email = (
        db.query(models.Individual_user)
        .filter(current_user == models.Individual_user.email)
        .first()
    )
    current_user_data_by_mobile = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == current_user)
        .first()
    )

    if current_user_data_by_email:
        my_data = (
            db.query(models.Individual_user)
            .filter(
                current_user_data_by_email.user_id == models.Individual_user.user_id
            )
            .first()
        )
        return my_data

    else:
        if current_user_data_by_mobile:
            my_data = (
                db.query(models.Individual_user)
                .filter(
                    current_user_data_by_mobile.user_id
                    == models.Individual_user.user_id
                )
                .first()
            )
            return my_data


# user profile edit data validation
def user_profile_edit(request):
    try:
        valid = validate_email(request.email)
        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"not a valid email"
        )

    if len(request.phone) != 10:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Phone number must be ten digit",
        )


# otp
def checking_otp(db, phone):
    checking_otp = db.query(models.Otp).filter(models.Otp.phone == phone).first()
    return checking_otp


# send otp
def create_otp(phone):
    otp = random.randint(100000, 999999)
    account_sid = "AC259347c6a5446e1abc14f27ad008b2d4"
    auth_token = "a30400efd112616f828e4e8b025b5a9a"
    client = Client(account_sid, auth_token)
    phone_number = "+91" + phone
    message = client.messages.create(
        body="Your Mazad.com verification code is:" + str(otp),
        from_="+14159031648",
        to=phone_number,
    )
    return otp


def getting_otp(db, otp):
    getting_otp = db.query(models.Otp).filter(models.Otp.otp == otp).first()
    return getting_otp


# individual user profile related apis
# get won profile data
def get_won_profile_data(db, current_user_id):
    getting_won_data = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.user_id == current_user_id)
        .first()
    )
    return getting_won_data


# admin related work
def checking_category(db, category_name):
    check_category = (
        db.query(models.Category)
        .filter(models.Category.category_name == category_name)
        .first()
    )
    return check_category


def checking_subcategory(db, subcategory_name):
    check_subcategory = (
        db.query(models.SubCategory)
        .filter(models.SubCategory.subcategory_name == subcategory_name)
        .first()
    )
    return check_subcategory


def checking_model(db, model_name):
    checking_model = (
        db.query(models.Models).filter(model_name == models.Models.model_name).first()
    )
    return checking_model


# getting categories


def getting_categories(db):
    get_categories = db.query(models.Category).all()
    return get_categories


# get particular categories by category name
def getting_particular_category(db, category_name):
    get_category = (
        db.query(models.Category)
        .filter(models.Category.category_name == category_name)
        .first()
    )
    return get_category


# get all subcategory
def getting_all_subcategory(db):
    get_subcategories = db.query(models.SubCategory).all()
    return get_subcategories


# getting all sub category under a category
def getting_subcategory_under_category(db, category_id):
    get_subcategory_under_category = (
        db.query(models.SubCategory)
        .filter(models.SubCategory.cat_id == category_id)
        .all()
    )
    return get_subcategory_under_category


# getting particular subcategory
def get_particular_subcategory(db, subcategory_name):
    get_particular_subcategory = (
        db.query(models.SubCategory)
        .filter(models.SubCategory.subcategory_name == subcategory_name)
        .first()
    )
    return get_particular_subcategory


# get brand under subcategory
def get_brand(db, subcat_id):
    get_brand = (
        db.query(models.Brand).filter(models.Brand.subcategory_id == subcat_id).all()
    )
    return get_brand


# get brand by subcategory and brand name
def get_brand_by_subcategory_brand_name(db, subcat_id, brad_name):
    getting_brand = (
        db.query(models.Brand)
        .filter(models.Brand.subcategory_id == subcat_id)
        .having(models.Brand.brand_name == brad_name)
        .first()
    )
    return getting_brand


def get_models(db, brand_id):
    get_models = (
        db.query(models.Models).filter(models.Models.brand_id == brand_id).all()
    )
    return get_models


# get all address
def get_address(db):
    get_address = db.query(models.Address).all()
    return get_address


# get won address
def get_won_address(db, user_id):
    get_won_address = db.query(models.Address).filter(models.Address.user_id == user_id).all()
    return get_won_address

def get_address_by_address_id(db,address_id):
    get_address = db.query(models.Address).filter(models.Address.address_id == address_id).first()
    return get_address


def get_item_all(db):
    get_all = db.query(models.Post_items).all()
    return get_all

def get_item_by_id(db,item_id):
    get_item = db.query(models.Post_items).filter(models.Post_items.item_id == item_id).first()
    return get_item


def get_won_post_items(db,user_id):
    get_won_items = (
        db.query(models.Post_items)
        .filter(models.Post_items.user_id == user_id)
        .all()
    )
    return get_won_items