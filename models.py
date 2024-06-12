from sqlalchemy import Column, Integer, String, Boolean
from db import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_pwd = Column(String)

