import json
import re
import time

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer,  event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from database import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    registrationTime = Column(Integer, default=lambda: int(time.time() * 1000))
    # TODO: Реализовать функционал обновления времени последнего обновления
    lastUpdate = Column(Integer, default=lambda: int(time.time() * 1000))
    tickets = relationship("Ticket", backref="user")


email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')


@event.listens_for(User, 'before_insert')
def validate_email(mapper, connection, target):
    if not email_regex.match(target.email):
        raise ValueError(f"'{target.email}' is not a valid email address")



