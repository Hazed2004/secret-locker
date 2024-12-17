from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError
from database import models
from database.connection import get_db
from auth.schemas import UserData
from auth.constants import SECRET_KEY, ALGORITHM

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("uuid")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user

@router.get("/get_user", response_model=UserData)
async def get_user(current_user: models.User = Depends(get_current_user)):
    
    return UserData(
        id=str(current_user.id),
        username=current_user.username,
        role=current_user.role,
        secret=current_user.secret
    )