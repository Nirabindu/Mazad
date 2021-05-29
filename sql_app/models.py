from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import column, false, table
from sqlalchemy.sql.sqltypes import DATE
from sql_app import database
import datetime




class Category(database.Base):
    __tablename__ = 'category'

    cat_id = Column(BigInteger,primary_key=True,index=True)
    category_name = Column(String(50),nullable=False,unique=True)
    status = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)
    sub_category = relationship('SubCategory',back_populates='category')



class SubCategory(database.Base):
    __tablename__='subcategory'

    subcategory_id = Column(BigInteger,primary_key = True,index = True)
    subcategory_name = Column(String(50),nullable = False,unique = True)
    status = Column(Boolean, default = True)
    create_at = Column(DateTime,default = datetime.datetime.utcnow)
    cat_id = Column(BigInteger,ForeignKey('category.cat_id'))
    category = relationship('Category',back_populates='sub_category')
