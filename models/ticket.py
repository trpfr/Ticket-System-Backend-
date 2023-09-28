#  This file contains the Ticket model, which is used to create the database table
import json
import re
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Column, Integer, String, TypeDecorator, event, ForeignKey
from database import Base


#  This class is used to store a dictionary in the database as a JSON string (for the labels)
class JsonEncodedDict(TypeDecorator):
    impl = String

    #  This function is used to convert a dictionary to a JSON string
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    #  This function is used to convert a JSON string to a dictionary
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class TicketStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    userEmail = Column(String, index=True)
    creationTime = Column(Integer, index=True)
    labels = Column(JsonEncodedDict, default=[])
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN)
    user_id = Column(String, ForeignKey('users.id'), index=True, nullable=True)


email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')


@event.listens_for(Ticket, 'before_insert')
def validate_email(mapper, connection, target):
    if not email_regex.match(target.userEmail):
        raise ValueError(f"'{target.userEmail}' is not a valid email address")
