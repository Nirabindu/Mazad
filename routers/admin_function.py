from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models, curd
from sqlalchemy.orm import Session
from security import oauth2
from typing import List, Optional
import shortuuid
import shutil


router = APIRouter(tags=["admin_side_function"])


# adding categories to database
@router.post("/admin/add_category/")
def add_category(
    category_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):
    get_user = curd.check_user(db, current_user)

    if get_user.role == "admin":
        checking_category = curd.checking_category(db, category_name)

        if checking_category == None:
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
            return {'status':'category added'}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Category already added"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorize user"
        )


# adding subcategory
@router.post("/admin/add_subcategory/")
def subcategory(
    category_name: str,
    subcategory_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):
    get_user = curd.check_user(db, current_user)

    if get_user.role == "admin":
        get_category_id = curd.checking_category(db, category_name)
        checking_subcategory = curd.checking_subcategory(db, subcategory_name)
        if checking_subcategory == None:
            # getting image
            file.filename = f"{shortuuid.uuid()}.jpg"
            with open("static/images/subcategory_images/" + file.filename, "wb") as img:
                shutil.copyfileobj(file.file, img)
            url = str("static/images/subcategory_images/" + file.filename)

            new_subCategory = models.SubCategory(
                subcategory_name=subcategory_name,
                subcategory_id=shortuuid.uuid(),
                image=url,
                cat_id=get_category_id.cat_id,
            )
            db.add(new_subCategory)
            db.commit()
            db.refresh(new_subCategory)
            return {'status':'subcategory added'}
        else:
            return {'status':'subcategory already added'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized user"
        )


# adding brand_name to brand table
@router.post("/admin/add_brand_name/")
def brand(
    request: schemas.Brand,
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):
    get_user = curd.check_user(db, current_user)

    if get_user.role == "admin":
        checking_subcategory = curd.checking_subcategory(db, request.subcategory_name)
        checking_brand_name_by_name = (
            db.query(models.Brand)
            .filter(models.Brand.brand_name == request.brand_name)
            .having(checking_subcategory.subcategory_id == models.Brand.subcategory_id)
            .first()
        )

        if checking_brand_name_by_name:
            return {"status": "Brand already added"}

        else:

            # adding new_brand in database
            new_brand = models.Brand(
                brand_id=shortuuid.uuid(),
                brand_name=request.brand_name,
                subcategory_id=checking_subcategory.subcategory_id,
            )
            db.add(new_brand)
            db.commit()
            db.refresh(new_brand)
            return {"status": "Brand name add"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized user"
        )


# adding models in database
@router.post("/admin/adding_models/")
def model(
    request: schemas.Models,
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    get_user = curd.check_user(db, current_user)
    if get_user.role == "admin":
        getting_subcategory = curd.checking_subcategory(db, request.subcategory_name)
        getting_brand = (
            db.query(models.Brand)
            .filter(models.Brand.brand_name == request.brand_name)
            .having(models.Brand.subcategory_id == getting_subcategory.subcategory_id)
            .first()
        )
        checking_model = curd.checking_model(db, request.model_name)

        if checking_model:
            return {"status": "model already added"}

        else:
            # adding new models in database
            new_model = models.Models(
                model_id=shortuuid.uuid(),
                model_name=request.model_name,
                brand_id=getting_brand.brand_id,
                subcategory_id=getting_subcategory.subcategory_id,
            )
            db.add(new_model)
            db.commit()
            db.refresh(new_model)
            return {"status": "model added"}


# get all categories
@router.get("/get_categories/", response_model=List[schemas.Get_category])
def get_categories(db: Session = Depends(database.get_db)):

    get_cat = curd.getting_categories(db)
    return get_cat


# get all subcategory
@router.get("/get_subcategories/", response_model=List[schemas.Get_SubCategory])
def get_all_subcategory(db: Session = Depends(database.get_db)):
    get_all_subcategory = curd.getting_all_subcategory(db)
    return get_all_subcategory


# getting all subCategories under particular categories
@router.get(
    "/get_subcategories/{category_name}/", response_model=List[schemas.Get_SubCategory]
)
def get_subcategories_under_categories(category_name: str, db: Session = Depends(database.get_db)):
    getting_particular_category = curd.getting_particular_category(db, category_name)

    get_subcategories_under_category = curd.getting_subcategory_under_category(
        db, getting_particular_category.cat_id
    )
    return get_subcategories_under_category


# getting brand under subcategories
@router.get("/get_brand/{subcategory_name}", response_model=List[schemas.Get_brand])
def get_brands(subcategory_name: str, db: Session = Depends(database.get_db)):

    get_particular_subcategory = curd.get_particular_subcategory(db,subcategory_name)
    get_brand   = curd.get_brand(db,get_particular_subcategory.subcategory_id)
    return get_brand


# getting all models under a  Brand and a subcategory
@router.get("/get_models/{subcategory_name}/{brand_name}", response_model=List[schemas.Get_models])
def get_models(subcategory_name:str, brand_name:str, db: Session = Depends(database.get_db)):

    get_particular_subcategory = curd.get_particular_subcategory(db,subcategory_name)

    get_brands_id = curd.get_brand_by_subcategory_brand_name(db,get_particular_subcategory.subcategory_id,brand_name)

    get_models = curd.get_models(db,get_brands_id.brand_id)

    return get_models












