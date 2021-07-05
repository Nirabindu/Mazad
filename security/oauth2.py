from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from security import tokens
from sql_app import models, database, schemas
from sqlalchemy.orm import Session, session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: session = Depends(database.get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate Credential",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return tokens.verify_token(token, credential_exception, db)
