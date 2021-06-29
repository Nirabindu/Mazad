from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.responses import JSONResponse
from sql_app import schemas, models, database
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from security import hashing, oauth2
from typing import List
from email_validator import validate_email, EmailNotValidError
import random
import twilio
from twilio.rest import Client

router = APIRouter(tags=["individual account related service"])

# GET WON DATA
@router.get("/get_won_data/")
async def get_won(
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    current_user_data_by_email = (
        db.query(models.Individual_user)
        .filter(current_user == models.Individual_user.email)
        .first()
    )
    current_user_data_by_mobile = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == current_user)
        .first()
    )
    if current_user_data_by_email and current_user_data_by_email.role == "individual":
        my_data = (
            db.query(models.Individual_user)
            .filter(
                current_user_data_by_email.user_id == models.Individual_user.user_id
            )
            .first()
        )
        return my_data

    elif (
        current_user_data_by_mobile and current_user_data_by_mobile.role == "individual"
    ):
        my_data = (
            db.query(models.Individual_user)
            .filter(
                current_user_data_by_mobile.user_id == models.Individual_user.user_id
            )
            .first()
        )
        return my_data
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You do not have the right to access this url",
        )


# CHANGE PASSWORD


@router.patch("/change_password/")
def change_password(
    request: schemas.Chang_password,
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    get_user_by_email = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.email == current_user)
        .first()
    )
    get_user_by_phone = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == current_user)
        .first()
    )
    password = request.current_password

    if get_user_by_email and get_user_by_email.role == "individual":

        password_verify = hashing.verify_password(password, get_user_by_email.password)
        if password_verify == True:
            new_password = request.new_password
            confirm_password = request.confirm_password
            if len(new_password) < 6:
                raise HTTPException(
                    status_code=status.HTTP_411_LENGTH_REQUIRED,
                    detail=f"password must be in 6 charecter",
                )

            check_if_new_password_same_as_old = hashing.verify_password(
                new_password, get_user_by_email.password
            )
            if check_if_new_password_same_as_old == True:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f"old password no acceptable as new password",
                )

            if new_password == confirm_password:
                get_user_by_email.password = hashing.bcrypt(confirm_password)
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
        db.refresh(get_user_by_email)
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=f"password changes please login again",
        )
    elif get_user_by_phone and get_user_by_phone.role == "individual":
        password_verify = hashing.verify_password(password, get_user_by_phone.password)
        if password_verify == True:
            new_password = request.new_password
            confirm_password = request.confirm_password
            if len(new_password) < 6:
                raise HTTPException(
                    status_code=status.HTTP_411_LENGTH_REQUIRED,
                    detail=f"password must be in 6 charecter",
                )

            check_if_new_password_same_as_old = hashing.verify_password(
                new_password, get_user_by_phone.password
            )
            if check_if_new_password_same_as_old == True:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f"old password no acceptable as new password",
                )

            if new_password == confirm_password:
                get_user_by_phone.password = hashing.bcrypt(confirm_password)
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
        db.refresh(get_user_by_phone)
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=f"password changes please login again",
        )


# EDIT PROFILE
@router.put("/edit_profile/")
async def edit_profile(
    request: schemas.User_update,
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    get_user_by_email = (
        db.query(models.Individual_user)
        .filter(current_user == models.Individual_user.email)
        .first()
    )
    get_user_by_phone = db.query(models.Individual_user).filter(
        models.Individual_user.phone == current_user
    ).first()

    if get_user_by_email and get_user_by_email.role == "individual":
        try:
            valid = validate_email(request.email)
            # Update with the normalized form.
            email = valid.email
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"not a valid email"
            )

        check_email = (
            db.query(models.Individual_user)
            .filter(request.email == models.Individual_user.email)
            .first()
        )

        if check_email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Email already register"
            )
        if len(request.phone) != 10:
            return {"phone number must be 10 digit"}

        check_mobile = (
            db.query(models.Individual_user)
            .filter(request.phone == models.Individual_user.phone)
            .first()
        )

        if check_mobile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"mobile already register"
            )

        get_user_by_email.user_name = request.user_name
        get_user_by_email.email = request.email
        get_user_by_email.phone = request.phone

        db.commit()
        db.refresh(get_user_by_email)
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f"details update")

    elif get_user_by_phone and get_user_by_phone.role == "individual":
        try:
            valid = validate_email(request.email)
            # Update with the normalized form.
            email = valid.email
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"not a valid email"
            )

        check_email = (
            db.query(models.Individual_user)
            .filter(request.email == models.Individual_user.email)
            .first()
        )

        if check_email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Email already register"
            )
        if len(request.phone) != 10:
            return {"phone number must be 10 digit"}

        check_mobile = (
            db.query(models.Individual_user)
            .filter(request.phone == models.Individual_user.phone)
            .first()
        )

        if check_mobile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"mobile already register"
            )

        get_user_by_phone.user_name = request.user_name
        get_user_by_phone.email = request.email
        get_user_by_phone.phone = request.phone

        db.commit()
        db.refresh(get_user_by_phone)
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f"details update")


@router.post("/auth/forgot_password/")
def forgot_password(request:schemas.Send_otp,db:Session = Depends(database.get_db)):
    validate_phone = db.query(models.Individual_user).filter(models.Individual_user.phone == request.phone).first()
    if validate_phone:
        checking_otp = db.query(models.Otp).filter(models.Otp.phone == request.phone).first()

        if checking_otp:
            db.delete(checking_otp)
            db.commit()
            otp = random.randint(1000, 9999)
            account_sid = "AC259347c6a5446e1abc14f27ad008b2d4"
            auth_token = "a30400efd112616f828e4e8b025b5a9a"
            client = Client(account_sid, auth_token)
            phone_number = "+91" + request.phone
            message = client.messages.create(
                body="Your Mazad.com verification code is:" + str(otp),
                from_="+14159031648",
                to=phone_number,
            )
            current_time = datetime.today()

            save_otp = models.Otp(otp=otp, phone=request.phone, create_at=current_time)
            db.add(save_otp)
            db.commit()
            db.refresh(save_otp)
            return JSONResponse("otp send")
        else:
            otp = random.randint(1000, 9999)
            account_sid = "AC259347c6a5446e1abc14f27ad008b2d4"
            auth_token = "a30400efd112616f828e4e8b025b5a9a"
            client = Client(account_sid, auth_token)
            phone_number = "+91" + request.phone
            message = client.messages.create(
                body="Your Mazad.com verification code is:" + str(otp),
                from_="+14159031648",
                to=phone_number,
            )
            current_time = datetime.today()

            save_otp = models.Otp(otp=otp, phone=request.phone, create_at=current_time)
            db.add(save_otp)
            db.commit()
            db.refresh(save_otp)
            return JSONResponse("otp send")    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'mobile no not register please sign up')


@router.put('/change_forgot_password/{phone_number}')
def change_pass(phone_number:str,request:schemas.New_password,db:Session = Depends(database.get_db)):
    geting_details = db.query(models.Individual_user).filter(models.Individual_user.phone == phone_number).first()

    new_password = request.new_password
    if len(request.new_password) !=6:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'password should be at least six charecter')

    if new_password == request.confirm_password:

        geting_details.password = hashing.bcrypt(request.confirm_password)
        db.commit()
        db.refresh(geting_details)
        return JSONResponse('New Password set please login')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'password not matched as above')  



        

