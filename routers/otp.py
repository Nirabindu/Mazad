import random
from fastapi import APIRouter, HTTPException, Depends, status
from sql_app import schemas, models, database,curd
from sqlalchemy.orm import Session
from datetime import datetime




router = APIRouter(tags=["OTP"])


# sending otp
@router.post("/send_otp/")
def sending_otp(request: schemas.Send_otp, db: Session = Depends(database.get_db)):

    checking_otp = curd.checking_otp(db,request.phone)
    if checking_otp:
        db.delete(checking_otp)
        db.commit()

        getting_otp = curd.create_otp(request.phone)

        current_time = datetime.today()

        save_otp = models.Otp(otp=getting_otp, phone=request.phone, create_at=current_time)
        db.add(save_otp)
        db.commit()
        db.refresh(save_otp)
        return {'status':'otp send'}
    else:
        getting_otp = curd.create_otp(request.phone)
        current_time = datetime.today()

        save_otp = models.Otp(otp=getting_otp, phone=request.phone, create_at=current_time)
        db.add(save_otp)
        db.commit()
        db.refresh(save_otp)
        return {'status':'otp send'}    

# verify otp
@router.post("/verify_otp/")
def otp_verify(request: schemas.Verify_otp, db: Session = Depends(database.get_db)):
    getting_otp = curd.getting_otp(db,request.enter_otp)
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
            return {'status':'otp verified'}
        else:
            db.delete(getting_otp)
            db.commit()
            return {'status':'otp expire'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"otp you entered not matched"
        )
