import random
from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sql_app import schemas, models, database
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from security import hashing, tokens, oauth2
import twilio
from twilio.rest import Client


router = APIRouter(tags=["OTP"])


# sending otp
@router.post("/send_otp/")
def sending_otp(request: schemas.Send_otp, db: Session = Depends(database.get_db)):

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


@router.post("/verify_otp/")
def otp_verify(request: schemas.Verify_otp, db: Session = Depends(database.get_db)):
    getting_otp = (
        db.query(models.Otp).filter(request.enter_otp == models.Otp.otp).first()
    )

    if getting_otp:

        date_time = datetime.today().replace(microsecond=0)

        date_from_database = getting_otp.create_at

        diff = date_time - date_from_database

        day = diff.days

        sec = diff.seconds

        hr = sec // 3600

        min = (sec // 60) % 60

        if day == 0 and hr < 1 and min <= 1 and sec <= 30:
            db.delete(getting_otp)
            db.commit()
            return JSONResponse("otp verified")
        else:
            db.delete(getting_otp)
            db.commit()
            return JSONResponse("Otp Expire")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"otp you entered not matched"
        )
