from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.responses import JSONResponse
from sql_app import schemas, models, database, curd
from sqlalchemy.orm import Session
import shortuuid
from security import hashing, tokens, oauth2
from typing import List
from email_validator import validate_email, EmailNotValidError


router = APIRouter(tags=[" users_auth"])

# user registration for admin
@router.post("/auth/registration/as_admin/")
async def user_registration_admin(
    request: schemas.User_registration, db: Session = Depends(database.get_db)
):

    user_validate = curd.user_data_validation(db, request)

    if user_validate == None:

        adding_user = models.Individual_user(
            user_id=shortuuid.uuid(),
            user_name=request.user_name,
            phone=request.phone,
            email=request.email,
            password=hashing.bcrypt(request.password),
            role="admin",
        )
        db.add(adding_user)
        db.commit()
        db.refresh(adding_user)
        return JSONResponse("Registration Success")


# user registration for individual
@router.post("/auth/registration/as_individual/")
async def user_registration_individual(
    request: schemas.User_registration, db: Session = Depends(database.get_db)
):

    user_validate = curd.user_data_validation(db, request)

    if user_validate == None:

        adding_user = models.Individual_user(
            user_id=shortuuid.uuid(),
            user_name=request.user_name,
            phone=request.phone,
            email=request.email,
            password=hashing.bcrypt(request.password),
            role="individual",
        )
        db.add(adding_user)
        db.commit()
        db.refresh(adding_user)
        return JSONResponse("Registration Success")


# user registration for business
@router.post("/auth/registration/as_business/")
async def user_registration_business(
    request: schemas.User_registration, db: Session = Depends(database.get_db)
):
    user_validate = curd.user_data_validation(db, request)

    if user_validate == None:

        adding_user = models.Individual_user(
            user_id=shortuuid.uuid(),
            user_name=request.user_name,
            phone=request.phone,
            email=request.email,
            password=hashing.bcrypt(request.password),
            role="business",
        )
        db.add(adding_user)
        db.commit()
        db.refresh(adding_user)
        return JSONResponse("Registration Success")




# user login
@router.post("/auth/login/")
def login_user(
    request: oauth2.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):  # request: schemas.User_login

    check = True  # for mobile

    for i in request.username:
        if i == "@":
            check = False
            break

    if check == True:
        checking_phone = (
            db.query(models.Individual_user)
            .filter(models.Individual_user.phone == request.username)
            .first()
        )
        if not checking_phone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mobile no you enter is not register",
            )
        else:
            if not hashing.verify_password(request.password, checking_phone.password):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password"
                )
        access_token = tokens.create_access_token(data={"sub": checking_phone.phone})
        return {"access_token": access_token, "token_type": "bearer"}

    if check == False:  # for email
        checking_email = (
            db.query(models.Individual_user)
            .filter(models.Individual_user.email == request.username)
            .first()
        )
        if not checking_email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"email you enter is not register",
            )
        else:
            if not hashing.verify_password(request.password, checking_email.password):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password"
                )
        access_token = tokens.create_access_token(data={"sub": checking_email.email})
        return {"access_token": access_token, "token_type": "bearer"}