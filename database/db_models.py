from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     fullname = Column(String)
#     nickname = Column(String)

#     addresses = relationship("Address", back_populates="user")