from flask_login import UserMixin
from sqlalchemy import *

from extentions import db


class User(db.Model ,UserMixin):
    __tablename__='users'
    id = Column(Integer,primary_key=True)
    password = Column(String,nullable=False)
    username = Column(String,nullable=False,unique=True)
    first_name = Column(String,nullable=False) 
    last_name = Column(String,nullable=False)
    phone= Column(String(11),nullable=False,unique=True)
    email= Column(String,nullable=False,unique=False)
    address= Column(String,nullable=False)
