from sqlalchemy import *

from extentions import db


class Product(db.Model):
    __tablename__='products'
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False , unique=True) 
    description = Column(String,nullable=False)
    quantity = Column(Integer,nullable=False)
    price = Column(Integer,nullable=False , default=0)
