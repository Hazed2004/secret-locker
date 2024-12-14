from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(...)

class UserRegister(UserLogin):
    password: str = Field(..., min_length=8)

class UserData(BaseModel):
    id: UUID
    username: str = Field(..., min_length=1, max_length=50)
    role: str = Field(...)
    secret: Optional[str]

    class Config:
        orm_mode = True

class SecretParse(BaseModel):
    secret: str


class TokenResponse(BaseModel):
    token: str

    class Config:
        orm_mode = True