from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import bcrypt
import uuid
from database import models
from database.connection import get_db
from auth.schemas import UserRegister, TokenResponse
from auth.jwt_utils import create_access_token

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(
    select(models.User).filter(
        (models.User.username == user.username)
        )
    )
    user_found = existing_user.scalars().first()
    if user_found:
        if user_found.username == user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{"msg":"Username already registered"}])

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = models.User(
        id=uuid.uuid4(),
        username=user.username,
        password_hash=hashed_password.decode('utf-8'),
        role="user"
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token(data={"uuid": str(new_user.id)})

    return TokenResponse(
        token=access_token
    )
