from sqlalchemy.orm import Session
from . import schemas, database, models
from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from security import oauth2
from email_validator import validate_email, EmailNotValidError


# user data validation
def user_data_validation(db, request):
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
    check_mobile = (
        db.query(models.Individual_user)
        .filter(request.phone == models.Individual_user.phone)
        .first()
    )

    if check_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Email already register"
        )
    if len(request.phone) != 10:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Phone number must be ten digit",
        )

    if check_mobile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"mobile already register"
        )

    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"password must be greater then 6 digit",
        )

    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"password not matched as above",
        )


# getting user by checking mobile and email
def check_user(
    db,
    current_user,
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

    if current_user_data_by_email:
        my_data = (
            db.query(models.Individual_user)
            .filter(
                current_user_data_by_email.user_id == models.Individual_user.user_id
            )
            .first()
        )
        return my_data

    else:
        if current_user_data_by_mobile:
            my_data = (
                db.query(models.Individual_user)
                .filter(
                    current_user_data_by_mobile.user_id
                    == models.Individual_user.user_id
                )
                .first()
            )
            return my_data
