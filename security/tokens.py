from datetime import datetime, timedelta
from jose import JWTError, jwt
from sql_app import schemas, models

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception, db):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: str = payload.get("sub")

        if user is None:
            raise credentials_exception

        token_data = schemas.TokenData(user=user)

    except JWTError:
        raise credentials_exception
    return token_data.user
    # user_phone = (
    #     db.query(models.Individual_user)
    #     .filter(models.Individual_user.phone == token_data.user)
    #     .first()
    # )
    # user_email = (
    #     db.query(models.Individual_user)
    #     .filter(models.Individual_user.email == token_data.user)
    #     .first()
    # )

    # if user_phone:
    #     return user_phone
    # elif user_email:
    #     return user_email
    # else:
    #     raise credentials_exception
