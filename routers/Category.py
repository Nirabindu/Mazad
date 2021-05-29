from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from sql_app import database, schemas, models
from sqlalchemy.orm import Session
# from security import hashing, oauth2, tokens
from typing import List, Optional, Dict
# import shortuuid
import shutil


router = APIRouter(tags=['Add Category'])


@router.post('/add_category/')
def add_category(category_name:str,db:Session = Depends(database.get_db)):

    #checking is there any category already added
    checking_category = db.query(models.Category).filter(category_name == models.Category.category_name).first()

    if checking_category:
        return{'Category already added'}
    else:
        #adding new category
        new_category = models.Category(
            category_name = category_name,

        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return{'Category Added'}




@router.post('/add_subcategory/')
def subcategory(category_id:int,subcategory_name:str,db:Session = Depends(database.get_db)):

    # checking correct category_id

    checking_category_id = db.query(models.Category).filter(models.Category.cat_id == category_id).first()

    if not checking_category_id:
        return{'Enter Correct category ID'}

    else:
        # checking is there same subcategory added or not 
        checking_subcategory = db.query(models.SubCategory).filter(subcategory_name ==  models.SubCategory.subcategory_name).first()
        if checking_subcategory:
            return{'SubCategory already Added'}
        else:
            new_subCategory = models.SubCategory(
                subcategory_name = subcategory_name,
                cat_id = category_id
            ) 
            db.add(new_subCategory)
            db.commit()
            db.refresh(new_subCategory)    
            return{'SubCategory added'}   

