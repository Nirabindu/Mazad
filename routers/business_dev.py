from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import schemas, database, models
from sqlalchemy.orm import Session
import shortuuid
from security import hashing, tokens, oauth2
from typing import List, Optional
from email_validator import validate_email, EmailNotValidError
import shutil


router = APIRouter(tags=["Business-Owner"])

# BUSINESS REGISTRATION


@router.post("/business_registration/")
async def user_registration(
    request: schemas.User_registration, db: Session = Depends(database.get_db)
):

    try:
        valid = validate_email(request.email)
        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return {"Not a valid email address"}

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

    if len(request.password) < 6:
        return {"password must be in 6 charecter"}

    if request.password != request.confirm_password:
        return {"password not matched as above"}

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

    return {"registration success please login"}


# # user registration for business
# @router.post("/Business_registration/")
# async def business_registration(
#     request: schemas.Business_registration, db: Session = Depends(database.get_db)
# ):

#     try:
#         valid = validate_email(request.email)
#         # Update with the normalized form.
#         email = valid.email
#     except EmailNotValidError as e:
#         # email is not valid, exception message is human-readable
#         return {"Not a valid email address"}

#     if len(request.phone) != 10:
#         return {"phone number must be 10 digit"}

#     if len(request.password) < 6:
#         return {"password must be in 6 charecter"}

#     if request.password != request.confirm_password:
#         return {"password not matched as above"}

#     check_email = (
#         db.query(models.Business_owner)
#         .filter(request.email == models.Business_owner.email)
#         .first()
#     )

#     if check_email:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Email already register"
#         )

#     check_mobile = (
#         db.query(models.Business_owner)
#         .filter(request.phone == models.Business_owner.phone)
#         .first()
#     )

#     if check_mobile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"mobile already register"
#         )

#     adding_user = models.Business_owner(
#         business_owner_id=shortuuid.uuid(),
#         user_name=request.user_name,
#         phone=request.phone,
#         email=request.email,
#         password=hashing.bcrypt(request.password),
#     )
#     db.add(adding_user)
#     db.commit()
#     db.refresh(adding_user)

#     return {"registration success please login"}


# # Business login apis
# @router.post("/business_login/")
# def login_user(
#     request: oauth2.OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(database.get_db),
# ):

#     check = True  # for mobile

#     for i in request.username:
#         if i == "@":
#             check = False
#             break

#     if check == True:
#         checking_phone = (
#             db.query(models.Business_owner)
#             .filter(
#                 models.Business_owner.phone == request.username
#             )  # user name is default for oauth2 validation
#             .first()
#         )
#         if not checking_phone:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Mobile no you enter is not register",
#             )
#         else:
#             if not hashing.verify_password(request.password, checking_phone.password):
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password"
#                 )
#         access_token = tokens.create_access_token(data={"sub": checking_phone.phone})
#         return {"access_token": access_token, "token_type": "bearer"}

#     if check == False:  # for email
#         checking_email = (
#             db.query(models.Business_owner)
#             .filter(models.Business_owner.email == request.username)
#             .first()
#         )
#         if not checking_email:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"email you enter is not register",
#             )
#         else:
#             if not hashing.verify_password(request.password, checking_email.password):
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password"
#                 )
#         access_token = tokens.create_access_token(data={"sub": checking_email.email})
#         return {"access_token": access_token, "token_type": "bearer"}


# GETTING BUSINESS LOCATION
@router.post("/getting_business_Location/")
def business_details(
    store_name: str = Form(...),
    store_category: str = Form(...),
    state: str = Form(...),
    district: str = Form(...),
    city: str = Form(...),
    street: Optional[str] = Form(None),
    building: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    getting_bs_owner_by_mobile = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == current_user)
        .first()
    )

    getting_bs_owner_by_email = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.email == current_user)
        .first()
    )

    # checking_bs_owner_by_mobile = (
    #     db.query(models.Business_location)
    #     .filter(
    #         models.Business_location.business_owner_id
    #         == getting_bs_owner_by_mobile.user_id
    #     )
    #     .first()
    # )

    # checking_bs_owner_by_email = (
    #     db.query(models.Business_location)
    #     .filter(
    #         models.Business_location.business_owner_id
    #         == getting_bs_owner_by_email.user_id
    #     )
    #     .first()
    # )

    # if checking_bs_owner_by_mobile:
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user already added"
    #     )
    # elif checking_bs_owner_by_email:
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user already added"
    # )

    if getting_bs_owner_by_mobile and getting_bs_owner_by_mobile.role == "business":

        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/store_sign/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/store_sign/" + file.filename)

        new_location = models.Business_location(
            business_details_id=shortuuid.uuid(),
            store_name=store_name,
            store_category=store_category,
            state=state,
            district=district,
            city=city,
            street=street,
            building=building,
            store_sign=url,
            business_owner_id=getting_bs_owner_by_mobile.user_id,
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        return {"location added"}
    elif getting_bs_owner_by_email and getting_bs_owner_by_email.role == "business":
        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/store_sign/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/store_sign/" + file.filename)

        new_location = models.Business_location(
            business_details_id=shortuuid.uuid(),
            store_name=store_name,
            store_category=store_category,
            state=state,
            district=district,
            city=city,
            street=street,
            building=building,
            store_sign=url,
            business_owner_id=getting_bs_owner_by_email.user_id,
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        return {"location added"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"you do not have the right to access this url",
        )


# UPLOADING MAROOF
@router.post("/uploading_maroof_details/")
def maroof(
    maroof_id: str = Form(...),
    maroof_expire_date: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    getting_bs_owner_by_mobile = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == current_user)
        .first()
    )

    getting_bs_owner_by_email = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.email == current_user)
        .first()
    )

    if getting_bs_owner_by_mobile and getting_bs_owner_by_mobile.role == "business":

        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/maroof/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/maroof/" + file.filename)

        new_maroof = models.Maroof_certificate(
            certificate_id=shortuuid.uuid(),
            maroof_id=maroof_id,
            maroof_expire_date=maroof_expire_date,
            image=url,
            business_owner_id=getting_bs_owner_by_mobile.user_id,
        )

        db.add(new_maroof)
        db.commit()
        db.refresh(new_maroof)
        return {"added"}
    elif getting_bs_owner_by_email and getting_bs_owner_by_email.role == "business":
        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/maroof/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/maroof/" + file.filename)

        new_maroof = models.Maroof_certificate(
            certificate_id=shortuuid.uuid(),
            maroof_id=maroof_id,
            maroof_expire_date=maroof_expire_date,
            image=url,
            business_owner_id=getting_bs_owner_by_email.user_id,
        )

        db.add(new_maroof)
        db.commit()
        db.refresh(new_maroof)
        return {"added"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"you do not have the right to access this url",
        )


# UPLOADIND CR DETAILS
@router.post("/uploading_commercial_details/")
def commercial_upload(
    commercial_id: str = Form(...),
    commercial_expire_date: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):

    getting_bs_owner_by_mobile = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == current_user)
        .first()
    )

    getting_bs_owner_by_email = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.email == current_user)
        .first()
    )

    if getting_bs_owner_by_mobile and getting_bs_owner_by_mobile.role == "business":

        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/commercial/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/commercial/" + file.filename)

        new_commercial = models.Commercial_certificate(
            certificate_id=shortuuid.uuid(),
            commercial_id=commercial_id,
            commercial_expire_date=commercial_expire_date,
            image=url,
            business_owner_id=getting_bs_owner_by_mobile.user_id,
        )
        db.add(new_commercial)
        db.commit()
        db.refresh(new_commercial)
        return {"added"}
    elif getting_bs_owner_by_email and getting_bs_owner_by_email.role == "business":
        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/commercial/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/commercial/" + file.filename)

        new_commercial = models.Commercial_certificate(
            certificate_id=shortuuid.uuid(),
            commercial_id=commercial_id,
            commercial_expire_date=commercial_expire_date,
            image=url,
            business_owner_id=getting_bs_owner_by_email.user_id,
        )
        db.add(new_commercial)
        db.commit()
        db.refresh(new_commercial)
        return {"added"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"you do not have the right to access this url",
        )


# UPLOADIND VAT DETAILS
@router.post("/uploading_Vat_details/")
def vat(
    vat_number: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: schemas.User_login = Depends(oauth2.get_current_user),
):
    getting_bs_owner_by_mobile = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == current_user)
        .first()
    )

    getting_bs_owner_by_email = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.email == current_user)
        .first()
    )

    if getting_bs_owner_by_mobile and getting_bs_owner_by_mobile.role == "business":

        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/vat/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/vat/" + file.filename)

        new_vat = models.Vat(
            vat_id=shortuuid.uuid(),
            vat_number=vat_number,
            image=url,
            business_owner_id=getting_bs_owner_by_mobile.user_id,
        )
        db.add(new_vat)
        db.commit()
        db.refresh(new_vat)
        return {"added"}
    elif getting_bs_owner_by_email and getting_bs_owner_by_email.role == "business":
        file.filename = f"{shortuuid.uuid()}.jpg"
        with open("static/images/vat/" + file.filename, "wb") as img:
            shutil.copyfileobj(file.file, img)
        url = str("static/images/vat/" + file.filename)

        new_vat = models.Vat(
            vat_id=shortuuid.uuid(),
            vat_number=vat_number,
            image=url,
            business_owner_id=getting_bs_owner_by_email.user_id,
        )
        db.add(new_vat)
        db.commit()
        db.refresh(new_vat)
        return {"added"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"you do not have the right to access this url",
        )
