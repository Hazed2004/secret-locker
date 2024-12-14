from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import bcrypt
from database import models
from database.connection import get_db
from auth.schemas import UserLogin, TokenResponse
from auth.jwt_utils import create_access_token

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(models.User).filter(models.User.username == user.username))
    user_in_db = existing_user.scalars().first()

    if not user_in_db or not bcrypt.checkpw(user.password.encode('utf-8'), user_in_db.password_hash.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{"msg":"Invalid credentials"}])

    access_token = create_access_token(data={"uuid": str(user_in_db.id)})

    return TokenResponse(
        token=access_token
    )