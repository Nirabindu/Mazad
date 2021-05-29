from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime



class Category(BaseModel):
    category_id: int
    category_name: str
    status: bool
    create_at: datetime


class SubCategory(BaseModel):
    subcategory_id: int
    subcategory_name: str
    status: bool
    create_at: datetime