from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from sql_app import database, schemas, models
from sqlalchemy.orm import Session
from security import hashing, oauth2, tokens
from typing import List, Optional, Dict


router = APIRouter(tags=["Home Filter"])



# session.query(Item).filter(Item.cost_price.between(10, 50)).all()