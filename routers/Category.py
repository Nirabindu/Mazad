from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from pydantic.utils import get_model
from sqlalchemy.sql.functions import mode
from sql_app import database, schemas, models
from sqlalchemy.orm import Session

# from security import hashing, oauth2, tokens
from typing import List, Optional, Dict
import shortuuid
import shutil
from geopy.geocoders import Nominatim


router = APIRouter(tags=["Add Category"])


# adding categories to database


@router.post("/add_category/")
def add_category(
    category_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):

    # checking is there same category already added or not
    checking_category = (
        db.query(models.Category)
        .filter(category_name == models.Category.category_name)
        .first()
    )

    if checking_category:
        return {"Category already added"}
    else:
        # adding new category

        # taking images

        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/category_images/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/category_images/" + file.filename)

        new_category = models.Category(
            category_name=category_name, cat_id=shortuuid.uuid(), image=url
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return {"Category Added"}


# adding subcategory to category


@router.post("/add_subcategory/{category_name}")
def subcategory(
    category_name: str,
    subcategory_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):

    cat_id = (
        db.query(models.Category)
        .filter(models.Category.category_name == category_name)
        .first()
    )

    # checking is there same subcategory added or not
    checking_subcategory = (
        db.query(models.SubCategory)
        .filter(subcategory_name == models.SubCategory.subcategory_name)
        .first()
    )
    if checking_subcategory:
        return {"SubCategory already Added"}
    else:

        # taking images and adding subcategory to database

        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/subcategory_images/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/subcategory_images/" + file.filename)

        new_subCategory = models.SubCategory(
            subcategory_name=subcategory_name,
            subcategory_id=shortuuid.uuid(),
            image=url,
            cat_id=cat_id.cat_id,
        )
        db.add(new_subCategory)
        db.commit()
        db.refresh(new_subCategory)
        return {"SubCategory added"}


# adding brand_name to brand table
@router.post("/add_brand_name/{subcategory_name}")
def brand(
    subcategory_name: str,
    request_body: schemas.Brand,
    db: Session = Depends(database.get_db),
):

    # checking brand name already in database or not

    checking_brand_name = (
        db.query(models.Brand)
        .filter(request_body.brand_name == models.Brand.brand_name)
        .first()
    )

    sub_cat_id = (
        db.query(models.SubCategory)
        .filter(models.SubCategory.subcategory_name == subcategory_name)
        .first()
    )

    if checking_brand_name:
        return {"brand already Added"}

    else:
        # adding new_brand in database
        new_brand = models.Brand(
            brand_id=shortuuid.uuid(),
            brand_name=request_body.brand_name,
            subcategory_id=sub_cat_id.subcategory_id,
        )
        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return {"added"}


# adding models in database
@router.post("/adding_models/{brand_name}")
def model(
    brand_name: str,
    request_body: schemas.Models,
    db: Session = Depends(database.get_db),
):

    # checking models already added or not

    checking_model = (
        db.query(models.Models)
        .filter(request_body.model_name == models.Models.model_name)
        .first()
    )

    brand_id = (
        db.query(models.Brand).filter(models.Brand.brand_name == brand_name).first()
    )

    if checking_model:
        return {"models already added"}

    else:
        # adding new models in database
        new_model = models.Models(
            model_id=shortuuid.uuid(),
            model_name=request_body.model_name,
            brand_id=brand_id.brand_id,
        )
        db.add(new_model)
        db.commit()
        db.refresh(new_model)
        return {"model added"}


# getting address
@router.post("/getting_address/")
def address(
    user_id: int,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(database.get_db),
):

    if state == None and district == None:

        geolocator = Nominatim(user_agent="Mazad")
        location = geolocator.reverse("{}, {}".format(latitude, longitude))

        new_address = models.Address(
            address_id=shortuuid.uuid(),
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            address_get=location.address,
            state=state,
            district=district,
        )
        db.add(new_address)
        db.commit()
        db.refresh(new_address)

        return new_address

    else:
        new_address = models.Address(
            address_id=shortuuid.uuid(),
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            state=state,
            district=district,
        )
        db.add(new_address)
        db.commit()
        db.refresh(new_address)

        return new_address


# post item


@router.post("/post_items/{subcategory_name}/{brand_name}/{model_name}")
def post_item(
    subcategory_name: str,
    brand_name: str,
    model_name: str,
    user_id: str,
    style: Optional[str] = Form(None),
    feature: Optional[str] = Form(None),
    milage: Optional[str] = Form(None),
    km_driven: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    condition: str = Form(...),
    firm_on_my_price: bool = Form(...),
    returnable: bool = Form(...),
    shipping: str = Form(...),
    shipping_method: str = Form(...),
    description: str = Form(...),
    set_product_weight: str = Form(...),
    set_price: float = Form(...),
    file: List[UploadFile] = File(...),
    db: Session = Depends(database.get_db),
):

    get_subcategory = (
        db.query(models.SubCategory)
        .filter(subcategory_name == models.SubCategory.subcategory_name)
        .first()
    )

    get_category_name = (
        db.query(models.models.Category)
        .filter(models.Category.cat_id == models.SubCategory.cat_id)
        .first()
    )

    get_brand_id = (
        db.query(models.Brand).filter(models.Brand.brand_name == brand_name).first()
    )

    get_models_id = (
        db.query(models.Models).filter(models.Models.model_name == model_name).first()
    )

    get_address_id = (
        db.query(models.Address).filter(models.Address.user_id == user_id).first()
    )

    adding_item = models.Post_items(
        item_id=shortuuid.uuid(),
        category_name=get_category_name.category_name,
        subcategory_name=get_subcategory.subcategory_name,
        brand_name=get_brand_id.brand_name,
        model_name=get_models_id.model_name,
        style=style,
        feature=feature,
        milage=milage,
        km_driven=km_driven,
        size=size,
        condition=condition,
        firm_on_my_price=firm_on_my_price,
        returnable=returnable,
        shipping=shipping,
        shipping_method=shipping_method,
        description=description,
        set_product_weight=set_product_weight,
        set_price=set_price,
        # user_id = user_id,
        cat_id=get_category_name.cat_id,
        subcategory_id=get_subcategory.subcategory_id,
        brand_id=get_brand_id.brand_id,
        model_id=get_models_id.model_id,
        address_id=get_address_id.address_id,
    )
    db.add(adding_item)
    db.commit()
    db.refresh(adding_item)

    item = (
        db.query(models.Post_items)
        .filter(models.Post_items.brand_name == brand_name)
        .first()
    )

    # taking images

    for i in file:
        i.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/item_images/" + i.filename, "wb") as img:
            shutil.copyfileobj(i.file, img)
        url = str("static/images/item_images/" + i.filename)

        new_item_img = models.Images_for_item(
            img_id=shortuuid.uuid(), url=url, item_id=item.item_id
        )
        db.add(new_item_img)
        db.commit()
        db.refresh(new_item_img)

        return {"Item Post"}


# GETTING ALL APIS GET


@router.get("/get_post_items/", response_model=List[schemas.get_item])
def get_items(db: Session = Depends(database.get_db)):

    get_items = db.query(models.Post_items).all()

    return get_items


@router.get("/get_categories/", response_model=List[schemas.Get_category])
def get_categories(db: Session = Depends(database.get_db)):

    get_cat = db.query(models.Category).all()

    return get_cat


@router.get("/get_subcategories/", response_model=List[schemas.Get_SubCategory])
def get_subcategories(db: Session = Depends(database.get_db)):

    get_subcat = db.query(models.SubCategory).all()

    return get_subcat


@router.get("/get_brand/", response_model=List[schemas.Get_brand])
def get_brands(db: Session = Depends(database.get_db)):

    get_brd = db.query(models.Brand).all()

    return get_brd


@router.get("/get_models/",response_model=List[schemas.Get_models])
def get_models(db:Session = Depends(database.get_db)):

    get_mod = db.query(models.Models).all()
    return get_mod