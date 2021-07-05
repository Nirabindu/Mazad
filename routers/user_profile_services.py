from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.responses import JSONResponse
from sql_app import schemas, models, database, curd
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from security import hashing, oauth2
from typing import List
from email_validator import validate_email, EmailNotValidError
import random
import twilio
from twilio.rest import Client

router = APIRouter(tags=["user_profile_service"])

# Get won data
@router.get("/user/get_won_data/", response_model=schemas.Show_profile_data)
async def get_won(
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):
    getting_current_user_data = curd.check_user(db, current_user)

    if (
        getting_current_user_data
        and getting_current_user_data.role == "individual"
        or getting_current_user_data.role == "business"
        or getting_current_user_data.role == "admin"
    ):
        get_profile_data = curd.get_won_profile_data(
            db, getting_current_user_data.user_id
        )

        return get_profile_data
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized user"
        )


# Change password
@router.put("/user/reset_password/")
def change_password(
    request: schemas.Chang_password,
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):
    getting_user = curd.check_user(db, current_user)

    password = request.current_password

    if (
        getting_user.role == "individual"
        or getting_user.role == "admin"
        or getting_user.role == "business"
    ):
        password_verify = hashing.verify_password(password, getting_user.password)
        if password_verify == True:
            new_password = request.new_password
            confirm_password = request.confirm_password
            if len(new_password) < 6:
                raise HTTPException(
                    status_code=status.HTTP_411_LENGTH_REQUIRED,
                    detail=f"password must be in 6 charecter",
                )

            check_if_new_password_same_as_old = hashing.verify_password(
                new_password, getting_user.password
            )
            if check_if_new_password_same_as_old == True:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f"old password no acceptable as new password",
                )

            if new_password == confirm_password:
                getting_user.password = hashing.bcrypt(confirm_password)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"password not matched as confirm password",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"your current password not valid enter password again",
            )

        db.commit()
        db.refresh(getting_user)
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=f"password changes please login again",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized user"
        )


# edit profile
@router.put("/user/edit_profile/")
async def edit_profile(
    request: schemas.User_update,
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    getting_user = curd.check_user(db, current_user)
    if getting_user == None:
        return {"status": "login again"}

    if (
        getting_user.role == "individual"
        or getting_user.role == "business"
        or getting_user.role == "admin"
    ):
        validating_data = curd.user_profile_edit(request)
        if validating_data == None:
            check_email = (
                db.query(models.Individual_user)
                .filter(request.email == models.Individual_user.email)
                .first()
            )
            check_mobile = (
                db.query(models.Individual_user)
                .filter(request.phone == models.Individual_user.phone)
                .first()
            )
            if check_email and check_email.email != getting_user.email:
                return {"status": "email already register"}
            if check_mobile and check_mobile.phone != getting_user.phone:
                return {"status": "mobile already register"}

            if (
                check_email
                and check_email.email == getting_user.email
                and check_mobile
                and check_mobile.phone == getting_user.phone
            ):
                getting_user.user_name = request.user_name
                getting_user.email = request.email
                getting_user.phone = request.phone
                db.commit()
                db.refresh(getting_user)
                return {"status": "details update"}

            if (
                check_email == None
                and check_mobile
                and check_mobile.phone == request.phone
            ):
                getting_user.user_name = request.user_name
                getting_user.email = request.email
                getting_user.phone = request.phone
                db.commit()
                db.refresh(getting_user)
                return {"status": "details update"}

            if (
                check_mobile == None
                and check_email
                and check_email.email == request.email
            ):
                getting_user.user_name = request.user_name
                getting_user.email = request.email
                getting_user.phone = request.phone
                db.commit()
                db.refresh(getting_user)
                return {"status": "details update"}

            if check_email == None and check_mobile == None:
                getting_user.user_name = request.user_name
                getting_user.email = request.email
                getting_user.phone = request.phone
                db.commit()
                db.refresh(getting_user)
                return {"status": "details update"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized user"
        )


# forgot password
@router.post("/user/forgot_password/")
def forgot_password(request: schemas.Send_otp, db: Session = Depends(database.get_db)):
    validate_phone = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == request.phone)
        .first()
    )

    if validate_phone:
        checking_otp = (
            db.query(models.Otp).filter(models.Otp.phone == request.phone).first()
        )

        if checking_otp:
            db.delete(checking_otp)
            db.commit()
            send_otp = curd.create_otp(request.phone)

            current_time = datetime.today()

            save_otp = models.Otp(
                otp=send_otp, phone=request.phone, create_at=current_time
            )
            db.add(save_otp)
            db.commit()
            db.refresh(save_otp)
            return {"status": "otp send"}
        else:
            send_otp = curd.create_otp(request.phone)
            current_time = datetime.today()

            save_otp = models.Otp(
                otp=send_otp, phone=request.phone, create_at=current_time
            )
            db.add(save_otp)
            db.commit()
            db.refresh(save_otp)
            return {"status": "otp send"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"mobile no not register please sign up",
        )


@router.put("/change_forgot_password/{phone_number}")
def change_pass(
    phone_number: str,
    request: schemas.New_password,
    db: Session = Depends(database.get_db),
):
    geting_details = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == phone_number)
        .first()
    )

    new_password = request.new_password
    if len(request.new_password) != 6:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"password should be at least six charecter",
        )

    if new_password == request.confirm_password:

        geting_details.password = hashing.bcrypt(request.confirm_password)
        db.commit()
        db.refresh(geting_details)
        return JSONResponse("New Password set please login")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"password not matched as above",
        )
