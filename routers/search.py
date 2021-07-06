from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models, curd
from sqlalchemy.orm import Session
from security import oauth2
from typing import List, Optional





router = APIRouter(tags=["search"])

@router.get("/search/{search_string}", response_model=List[schemas.Get_item])
def search(search_string: str, db: Session = Depends(database.get_db)):

    item = (
        db.query(models.Post_items)
        .filter(models.Post_items.model_name.ilike(f"%{search_string}%"))
        .all()
    )
    sub_category = (
        db.query(models.Post_items)
        .filter(models.SubCategory.subcategory_name.ilike(f"%{search_string}%"))
        .filter(models.SubCategory.subcategory_id == models.Post_items.subcategory_id)
        .all()
    )
    model = (
        db.query(models.Post_items)
        .filter(models.Models.model_name.ilike(f"%{search_string}%"))
        .filter(models.Models.model_id == models.Post_items.model_id)
        .all()
    )
    if item:
        return item
    elif sub_category:
        return sub_category

    elif model:
        return model
    else:
        return {"Search item not found"}