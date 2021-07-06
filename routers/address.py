from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models, curd
from sqlalchemy.orm import Session
from security import oauth2
from geopy.geocoders import Nominatim
import shortuuid
from typing import List, Optional


router = APIRouter(tags=["address"])


# getting address
@router.post("/getting_address/")
def address(
    latitude: float = Form(None),
    longitude: float = Form(None),
    state: str = Form(None),
    district=Form(None),
    city=Form(None),
    street=Form(None),
    building=Form(None),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):

    getting_user = curd.check_user(db, current_user)

    if (
        getting_user.role == "individual"
        or getting_user.role == "business"
        or getting_user.role == "admin"
    ):

        if latitude != None and longitude != None:

            geolocator = Nominatim(user_agent="Tejarh")
            location = geolocator.reverse("{}, {}".format(latitude, longitude))

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized user"
        )


# get user address
@router.get("/get_won_address/", response_model=List[schemas.Get_address])
def get_won_address(
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    get_current_user = curd.check_user(db, current_user)
    if get_current_user.role == 'admin' or 'business' or 'individual':
        get_won_address = curd.get_won_address(db, get_current_user.user_id)
        return get_won_address
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'unauthorized user')



#edit address




# delete address
@router.delete("/delete_address/{id}")
def delete_address(
    id: str,
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    get_current_user = curd.check_user(db, current_user)
    if get_current_user.role == 'individual' or 'admin' or 'business':
        get_address = curd.get_address_by_address_id(db, id)

        get_particular_address = (
            db.query(models.Address)
            .filter(get_address.address_id == id)
            .having(models.Address.user_id == get_current_user.user_id)
            .first()
        )
        if get_particular_address:
            db.delete(get_particular_address)
            db.commit()
            return {'status':'address delete'}
        else:
            return{'status':'address not found'}    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'unauthorized user')

# get all address
@router.get("/get_all_address/", response_model=List[schemas.Get_address])
def get_all_address(db: Session = Depends(database.get_db)):
    get_address = curd.get_address(db)
    return get_address
