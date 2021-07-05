
from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models, curd
from sqlalchemy.orm import Session
from security import oauth2
from geopy.geocoders import Nominatim
import shortuuid



router = APIRouter(tags=["address"])




# getting address
@router.post("/getting_address/")
def address(
     latitude:float = Form(None),
     longitude:float = Form(None),
     state:str = Form(None),
     district = Form(None),
     city = Form(None),
     street = Form(None),
     building = Form(None),

    
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):

    getting_user = curd.check_user(db,current_user)

    if getting_user.role == 'individual' or getting_user.role == 'business' or getting_user.role == 'admin':


        if latitude != None and longitude != None:

            geolocator = Nominatim(user_agent="Tejarh")
            location = geolocator.reverse(
                "{}, {}".format(latitude,longitude)
            )

            new_address = models.Address(
                address_id=shortuuid.uuid(),
                user_id=getting_user.user_id,
                latitude=latitude,
                longitude=longitude,
                address_get=location.address,
                state=state,
                district=district,
                city=city,
                street=street,
                building=building,
            )
            db.add(new_address)
            db.commit()
            db.refresh(new_address)

            return new_address

        else:
            new_address = models.Address(
                address_id=shortuuid.uuid(),
                user_id=getting_user.user_id,
                latitude=latitude,
                longitude=longitude,
                state=state,
                district=district,
                city=city,
                street=street,
                building=building,
            )
            db.add(new_address)
            db.commit()
            db.refresh(new_address)

            return new_address

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'unauthorized user')        