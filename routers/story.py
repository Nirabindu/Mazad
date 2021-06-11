from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models
from sqlalchemy.orm import Session

from security import hashing, oauth2, tokens
from typing import List, Optional, Dict
import shortuuid
import cloudinary
import cloudinary.uploader
import shutil

router = APIRouter(tags=["story"])


@router.post("/upload_story/{item_id}")
def Story(
    item_id:str,
    db: Session = Depends(database.get_db),
    file: UploadFile = File(...),
    current_user: schemas.User_login = Depends(oauth2.get_current_user)
):
    

    item = db.query(models.Post_items).filter(models.Post_items.item_id == item_id).first()


    res = cloudinary.uploader.upload_large(
        file.file,
        resource_type="video",
        quality="auto",
        chunk_size=6000000
        )

    url = res.get("url")

    new_story = models.Story(
        story_id=shortuuid.uuid(),
        url = url,
        item_id = item.item_id,
        user_id = current_user.user_id
    )

    db.add(new_story)
    db.commit()
    db.refresh(new_story)
    return{'Story uploaded'}


#problem
@router.get('/get_story/',response_model=List[schemas.Get_story])
def Get_story(db: Session = Depends(database.get_db),current_user : schemas.User_login = Depends(oauth2.get_current_user)):

    
    
    Get_story = db.query(models.Story).filter(models.Individual_user.user_id == current_user.user_id).all()

    return Get_story