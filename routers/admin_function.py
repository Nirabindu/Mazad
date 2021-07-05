from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models, curd
from sqlalchemy.orm import Session
from security import oauth2
from typing import List, Optional
import shortuuid
import shutil

from fastapi.responses import JSONResponse


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
            return JSONResponse("Category Added")
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
            return JSONResponse("SubCategory added")
        else:
            return JSONResponse("Sub category already added")
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

    get_models = (
        db.query(models.Models)
        .filter(models.Models.brand_id == get_brands_id.brand_id)
        .all()
    )

    return get_models











# # post item


# @router.post("/post_items/{subcategory_name}/{brand_name}/{model_name}")
# def post_item(
#     subcategory_name: str,
#     brand_name: str,
#     model_name: str,
#     style: Optional[str] = Form(None),
#     feature: Optional[str] = Form(None),
#     milage: Optional[str] = Form(None),
#     km_driven: Optional[str] = Form(None),
#     size: Optional[str] = Form(None),
#     condition: str = Form(...),
#     firm_on_my_price: bool = Form(...),
#     returnable: bool = Form(...),
#     shipping: str = Form(...),
#     shipping_method: str = Form(...),
#     description: str = Form(...),
#     set_product_weight: str = Form(...),
#     set_price: float = Form(...),
#     file: List[UploadFile] = File(...),
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User_login = Depends(oauth2.get_current_user),
# ):

#     get_subcategory = (
#         db.query(models.SubCategory)
#         .filter(subcategory_name == models.SubCategory.subcategory_name)
#         .first()
#     )

#     get_category_name = (
#         db.query(models.Category)
#         .filter(models.Category.cat_id == get_subcategory.cat_id)
#         .first()
#     )

#     get_brand_id = (
#         db.query(models.Brand).filter(models.Brand.brand_name == brand_name).first()
#     )

#     get_models_id = (
#         db.query(models.Models).filter(models.Models.model_name == model_name).first()
#     )

#     get_address_id = (
#         db.query(models.Address)
#         .filter(models.Address.user_id == current_user.user_id)
#         .first()
#     )

#     adding_item = models.Post_items(
#         item_id=shortuuid.uuid(),
#         category_name=get_category_name.category_name,
#         subcategory_name=get_subcategory.subcategory_name,
#         brand_name=get_brand_id.brand_name,
#         model_name=get_models_id.model_name,
#         style=style,
#         feature=feature,
#         milage=milage,
#         km_driven=km_driven,
#         size=size,
#         condition=condition,
#         firm_on_my_price=firm_on_my_price,
#         returnable=returnable,
#         shipping=shipping,
#         shipping_method=shipping_method,
#         description=description,
#         set_product_weight=set_product_weight,
#         set_price=set_price,
#         user_id=current_user.user_id,
#         cat_id=get_category_name.cat_id,
#         subcategory_id=get_subcategory.subcategory_id,
#         brand_id=get_brand_id.brand_id,
#         model_id=get_models_id.model_id,
#         address_id=get_address_id.address_id,
#     )
#     db.add(adding_item)
#     db.commit()
#     db.refresh(adding_item)

#     item = (
#         db.query(models.Post_items)
#         .filter(models.Post_items.item_id == adding_item.item_id)  # problems
#         .first()
#     )

#     # taking images

#     for i in file:
#         i.filename = f"{shortuuid.uuid()}.jpg"
#         with open("static/images/item_images/" + i.filename, "wb") as img:
#             shutil.copyfileobj(i.file, img)
#         url = str("static/images/item_images/" + i.filename)

#         new_item_img = models.Images_for_item(
#             img_id=shortuuid.uuid(), url=url, item_id=item.item_id
#         )
#         db.add(new_item_img)
#         db.commit()
#         db.refresh(new_item_img)

#     return {"Item Post"}


# # GETTING ALL APIS GET


# @router.get("/get_post_items/", response_model=List[schemas.Get_item])
# def get_items(db: Session = Depends(database.get_db)):

#     get_items = db.query(models.Post_items).all()

#     return get_items


# # getting all post item post by user
# @router.get("/my_post_items/", response_model=List[schemas.Get_item])
# def get_my_items(
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User_login = Depends(oauth2.get_current_user),
# ):
#     get_won_items = (
#         db.query(models.Post_items)
#         .filter(models.Post_items.user_id == current_user.user_id)
#         .all()
#     )
#     return get_won_items





# # search apis


# @router.get("/search/{search_string}", response_model=List[schemas.Get_item])
# def search(search_string: str, db: Session = Depends(database.get_db)):

#     item = (
#         db.query(models.Post_items)
#         .filter(models.Post_items.model_name.ilike(f"%{search_string}%"))
#         .all()
#     )
#     sub_category = (
#         db.query(models.Post_items)
#         .filter(models.SubCategory.subcategory_name.ilike(f"%{search_string}%"))
#         .filter(models.SubCategory.subcategory_id == models.Post_items.subcategory_id)
#         .all()
#     )
#     model = (
#         db.query(models.Post_items)
#         .filter(models.Models.model_name.ilike(f"%{search_string}%"))
#         .filter(models.Models.model_id == models.Post_items.model_id)
#         .all()
#     )
#     if item:
#         return item
#     elif sub_category:
#         return sub_category

#     elif model:
#         return model
#     else:
#         return {"Search item not found"}
