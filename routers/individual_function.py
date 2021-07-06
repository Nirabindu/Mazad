from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models, curd
from sqlalchemy.orm import Session
from security import oauth2
from typing import List, Optional
import shortuuid
import shutil


router = APIRouter(tags=["individual_function"])

# post an item


@router.post("/user/post_items/")
def post_item(
    subcategory_name: str,
    brand_name: str,
    model_name: str,
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
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    get_user = curd.check_user(db, current_user)
    if get_user.role == "individual" or "admin":

        get_subcategory = curd.get_particular_subcategory(db,subcategory_name)

        get_category_name = (
            db.query(models.Category)
            .filter(models.Category.cat_id == get_subcategory.cat_id)
            .first()
        )

        get_brand_id = (
            db.query(models.Brand).filter(models.Brand.brand_name == brand_name).first()
        )

        get_models_id = (
            db.query(models.Models)
            .filter(models.Models.model_name == model_name)
            .first()
        )

        get_address_id = (
            db.query(models.Address)
            .filter(models.Address.user_id == get_user.user_id)
            .first()
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
            user_id=get_user.user_id,
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
            .filter(models.Post_items.item_id == adding_item.item_id)  
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


#get item in home



@router.get("/get_post_items_home/", response_model=List[schemas.Get_minimal_details_of_item])
def get_items(db: Session = Depends(database.get_db)):

    get_items = curd.get_item_all(db)

    return get_items

@router.get("/get_post_items_detail_view/{item_id}/",response_model=schemas.Get_item)
def get_item(item_id:str,db: Session = Depends(database.get_db)):

    get_item = curd.get_item_by_id(db,item_id)

    return get_item



# getting all post item post by user
@router.get("/my_post_items/", response_model=List[schemas.Get_item])
def get_my_items(
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):
    check_user = curd.check_user(db,current_user)
    get_won_items = curd.get_won_post_items(db,check_user.user_id)
    return get_won_items
    

