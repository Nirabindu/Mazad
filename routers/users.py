import random
from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from sql_app import schemas, database, models
from sqlalchemy.orm import Session
import shortuuid
from security import hashing, tokens, oauth2
from typing import List
from email_validator import validate_email, EmailNotValidError
import twilio
from twilio.rest import Client


router = APIRouter(tags=["users-individuals"])

# user registration for individual
@router.post("/registration/")
async def user_registration(
    request: schemas.User_registration, db: Session = Depends(database.get_db)
):
    # email = schemas.email

    try:
        valid = validate_email(request.email)
        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return {"Not a valid email address"}

    if len(request.phone) != 10:
        return {"phone number must be 10 digit"}

    if len(request.password) < 6:
        return {"password must be in 6 charecter"}

    check_email = (
        db.query(models.Individual_user)
        .filter(request.email == models.Individual_user.email)
        .first()
    )

    if check_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Email already register"
        )

    check_mobile = (
        db.query(models.Individual_user)
        .filter(request.phone == models.Individual_user.phone)
        .first()
    )

    if check_mobile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"mobile already register"
        )

    adding_user = models.Individual_user(
        user_id=shortuuid.uuid(),
        user_name=request.user_name,
        phone=request.phone,
        email=request.email,
        password=hashing.bcrypt(request.password),
    )
    db.add(adding_user)
    db.commit()
    db.refresh(adding_user)

    return {"registration success please login"}

# sending otp
@router.post("/send_otp/")
def send_otp():
    otp = random.randint(1000, 9999)
    account_sid = "AC259347c6a5446e1abc14f27ad008b2d4"
    auth_token = "a30400efd112616f828e4e8b025b5a9a"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Your Mazad.com verification code is:" + str(otp),
        from_="+14159031648",
        to="+917557823759",
    )

    # print(message.sid)
    return {"otp send to your mobile"}

# login apis
@router.post("/login/")
def login_user(request:oauth2.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):   #request: schemas.User_login

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
            if not hashing.verify_password(request.password,checking_phone.password):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password"
                )
        access_token = tokens.create_access_token(data={"sub": checking_phone.phone })
        return {"access_token": access_token, "token_type": "bearer"}       

    if check == False:  #for email
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
            if not hashing.verify_password(request.password,checking_email.password):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password"
                )
        access_token = tokens.create_access_token(data={"sub": checking_email.email })
        return {"access_token": access_token, "token_type": "bearer"}