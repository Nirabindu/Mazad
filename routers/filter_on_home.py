from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
import sql_app
from sqlalchemy.orm import Session
from security import hashing, oauth2, tokens
from typing import List, Optional, Dict


router = APIRouter(tags=["Home Filter"])



# session.query(Item).filter(Item.cost_price.between(10, 50)).all()