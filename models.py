from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_pwd = Column(String)

    college_id = Column(ForeignKey("colleges.id"), nullable=True)


    college = relationship("College")

class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    state = Column(String, index=True)

