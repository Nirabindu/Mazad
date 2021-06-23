import random
from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.responses import JSONResponse
from sql_app import schemas, models, database
from sqlalchemy.orm import Session
import shortuuid
from security import hashing, tokens, oauth2
from typing import List
from email_validator import validate_email, EmailNotValidError



router = APIRouter(tags=["users-individuals"])

# user registration for individual
@router.post("/registration/")
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
        role = "individual"
    )
    db.add(adding_user)
    db.commit()
    db.refresh(adding_user)

    return "rrr"





# login apis
@router.post("/login/")
def login_user(
    request: oauth2.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):  # request: schemas.User_login


    inv_role = db.query(models.Individual_user).filter(models.Individual_user.role == "individual").first()


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



# find won data


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
    if current_user_data_by_email:
        my_data = (
            db.query(models.Individual_user)
            .filter(current_user_data_by_email.user_id == models.Individual_user.user_id)
            .first()
        )
        return my_data

    current_user_data_by_mobile = (
        db.query(models.Individual_user)
        .filter(models.Individual_user.phone == current_user)
        .first()
    )

    if current_user_data_by_mobile:
        my_data = (
            db.query(models.Individual_user)
            .filter(
                current_user_data_by_mobile.user_id == models.Individual_user.user_id
            )
            .first()
        )
        return my_data


# # @router.get("/get_all_user/")
# # async def get_user(
# #     db: Session = Depends(database.get_db),
# #     current_user: schemas.User_login = Depends(oauth2.get_current_user),
# # ):
# #     get_user = db.query(models.Individual_user).all()
# #     return get_user


# Edit  user frofile profile
# @router.put("/edit_profile/")
# async def edit_profile(
#     request: schemas.User_update,
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User_login = Depends(oauth2.get_current_user),
# ):

#     get_data = (
#         db.query(models.Individual_user)
#         .filter(current_user.user_id == models.Individual_user.user_id)
#         .first()
#     )

#     try:
#         valid = validate_email(request.email)
#         # Update with the normalized form.
#         email = valid.email
#     except EmailNotValidError as e:
#         # email is not valid, exception message is human-readable
#         return {"Not a valid email address"}

#     check_email = (
#         db.query(models.Individual_user)
#         .filter(request.email == models.Individual_user.email)
#         .first()
#     )

#     if check_email:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Email already register"
#         )
#     if len(request.phone) != 10:
#         return {"phone number must be 10 digit"}

#     check_mobile = (
#         db.query(models.Individual_user)
#         .filter(request.phone == models.Individual_user.phone)
#         .first()
#     )

#     if check_mobile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"mobile already register"
#         )

#     get_data.user_name = request.user_name
#     get_data.email = request.email
#     get_data.phone = request.phone

#     db.commit()
#     db.refresh(get_data)
#     return {"Saved Data"}


# @router.patch("/change_password/")
# def change_password(
#     request: schemas.Chang_password,
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User_login = Depends(oauth2.get_current_user),
# ):

#     get_user = (
#         db.query(models.Individual_user)
#         .filter(models.Individual_user.user_id == current_user.user_id)
#         .first()
#     )

#     password = request.current_password

#     password_verify = hashing.verify_password(password, get_user.password)
#     if password_verify == True:
#         new_password = request.new_password
#         confirm_password = request.confirm_password
#         if len(new_password) < 6:
#             raise HTTPException(
#                 status_code=status.HTTP_411_LENGTH_REQUIRED,
#                 detail=f"password must be in 6 charecter",
#             )

#         check_if_new_password_same_as_old = hashing.verify_password(
#             new_password, get_user.password
#         )
#         if check_if_new_password_same_as_old == True:
#             raise HTTPException(
#                 status_code=status.HTTP_406_NOT_ACCEPTABLE,
#                 detail=f"old password no acceptable as new password",
#             )

#         if new_password == confirm_password:
#             get_user.password = hashing.bcrypt(confirm_password)
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"password not matched as confirm password",
#             )
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"your current password not valid enter password again",
#         )

#     db.commit()
#     db.refresh(get_user)
#     raise HTTPException(
#         status_code=status.HTTP_201_CREATED,
#         detail=f"password changes please login again",
#     )
