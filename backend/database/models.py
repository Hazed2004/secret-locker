import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from database.constants import USERS_TABLE

Base = declarative_base()

class User(Base):
    __tablename__ = USERS_TABLE
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    role = Column(String(50))
    password_hash = Column(String(255), nullable=False)
    secret = Column(String(255), nullable=True)