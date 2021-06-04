from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models
from sqlalchemy.orm import Session

# from security import hashing, oauth2, tokens
from typing import List, Optional, Dict
import shortuuid
import shutil
from geopy.geocoders import Nominatim


router = APIRouter(tags=["Add Category"])


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
        return {"Category Already added"}
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


@router.post("/add_subcategory/{category_id}")
def subcategory(
    category_id: str,
    subcategory_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):

    # checking correct category_id

    checking_category_id = (
        db.query(models.Category).filter(models.Category.cat_id == category_id).first()
    )

    if not checking_category_id:
        return {"Enter Correct category ID"}

    else:
        # checking is there same subcategory added or not
        checking_subcategory = (
            db.query(models.SubCategory)
            .filter(subcategory_name == models.SubCategory.subcategory_name)
            .first()
        )
        if checking_subcategory:
            return {"SubCategory already Added"}
        else:
            # taking images

            file.filename = f"{shortuuid.uuid()}.jpg"
            with open("static/images/subcategory_images/" + file.filename, "wb") as img:
                shutil.copyfileobj(file.file, img)
            url = str("static/images/subcategory_images/" + file.filename)

            new_subCategory = models.SubCategory(
                subcategory_name=subcategory_name,
                subcategory_id=shortuuid.uuid(),
                image=url,
                cat_id=category_id,
            )
            db.add(new_subCategory)
            db.commit()
            db.refresh(new_subCategory)
            return {"SubCategory added"}


# addind brand_name to brand table
@router.post("/add_brand_name/{subcategory_id}")
def brand(
    subcategory_id: str,
    request_body: schemas.Brand,
    db: Session = Depends(database.get_db),
):

    # checking brand name already in database or not

    checking_brand_name = (
        db.query(models.Brand)
        .filter(request_body.brand_name == models.Brand.brand_name)
        .first()
    )

    if checking_brand_name:
        return {"brand already Added"}

    else:
        # adding new_brand in database
        new_brand = models.Brand(
            brand_id=shortuuid.uuid(),
            brand_name=request_body.brand_name,
            subcategory_id=subcategory_id,
        )
        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return {"added"}


# adding models in database
@router.post("/adding_models/{brand_id}")
def model(
    brand_id: str, request_body: schemas.Models, db: Session = Depends(database.get_db)
):

    # checking models already added or not

    checking_model = (
        db.query(models.Models)
        .filter(request_body.model_name == models.Models.model_name)
        .first()
    )

    if checking_model:
        return {"models already added"}

    else:
        # adding new models in database
        new_model = models.Models(
            model_id=shortuuid.uuid(),
            model_name=request_body.model_name,
            brand_id=brand_id,
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


@router.post("/post_items/{subcategory_id}/{brand_id}/{model_id}")
def post_item(
    subcategory_id: str,
    brand_id: str,
    model_id: str,
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

    subcategory = (
        db.query(models.SubCategory)
        .filter(subcategory_id == models.SubCategory.subcategory_id)
        .first()
    )

    category_name = (
        db.query(models.Category)
        .filter(models.Category.cat_id == models.SubCategory.cat_id)
        .filter(models.SubCategory.subcategory_id == subcategory_id)
        .first()
    )

    brand_name = (
        db.query(models.Brand).filter(models.Brand.brand_id == brand_id).first()
    )

    models_name = (
        db.query(models.Models).filter(models.Models.model_id == model_id).first()
    )

    address_id = (
        db.query(models.Address).filter(models.Address.user_id == user_id).first()
    )

    adding_item = models.Post_items(
        item_id=shortuuid.uuid(),
        category_name=category_name.category_name,
        subcategory_name=subcategory.subcategory_name,
        brand_name=brand_name.brand_name,
        model_name=models_name.model_name,
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
        cat_id=category_name.cat_id,
        subcategory_id=subcategory.subcategory_id,
        brand_id=brand_name.brand_id,
        model_id=models_name.model_id,
        address_id=address_id.address_id,
    )
    db.add(adding_item)
    db.commit()
    db.refresh(adding_item)

    item = (
        db.query(models.Post_items)
        .filter(models.Post_items.brand_id == brand_id)
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


@router.get("/get_post_items/", response_model=List[schemas.get_item])
def get_items(db: Session = Depends(database.get_db)):

    get_items = db.query(models.Post_items).all()

    return get_items
