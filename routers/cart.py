from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models, curd
from sqlalchemy.orm import Session
from security import hashing, oauth2
from typing import List, Optional
import shortuuid
import shutil
from geopy.geocoders import Nominatim
from email_validator import validate_email, EmailNotValidError
from fastapi.responses import JSONResponse


router = APIRouter(tags=["cart_system"])




#adding item in cart
@router.post("/add_to_cart/")
def Cart(request:schemas.Cart,db:Session=Depends(database.get_db),current_user: schemas.User_login = Depends(oauth2.get_current_user)):
    user = curd.check_user(db,current_user)

    if user and user.role == 'individual' or user.role =='admin':
        get_item = db.query(models.Post_items).filter(models.Post_items.item_id == request.item_id).first()
        if get_item:
            add_to_cart = models.Cart(
                item_id = get_item.item_id,
                quantity = request.quantity,
                user_id = user.user_id,

            )
            db.add(get_item)
            db.commit()
            db.refresh()
            return JSONResponse('Item added to cart')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'item not found')

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= f'unauthorized user')        



# get_cart

@router.post(/get_cart/,request:schemas.Get_cart)
def get_cart(db:Session=Depends(database.get_db),)