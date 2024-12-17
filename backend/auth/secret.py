from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from jose import jwt, JWTError
from database import models
from database.connection import get_db
from auth.schemas import UserData, SecretParse
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

@router.post("/add_secret", response_model=UserData)
async def get_user(user_secret: SecretParse, current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    await db.execute(
        update(models.User)
        .where(models.User.id == current_user.id)
        .values(secret=user_secret.secret)
    )
    
    await db.commit()

    return UserData(
        id=str(current_user.id),
        username=current_user.username,
        role=current_user.role,
        secret=user_secret.secret
    )

@router.get("/delete_secret", response_model=UserData)
async def get_user(current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    await db.execute(
        update(models.User)
        .where(models.User.id == current_user.id)
        .values(secret="")
    )
    
    await db.commit()

    return UserData(
        id=str(current_user.id),
        username=current_user.username,
        role=current_user.role,
        secret=""
    )

@router.get("/get_all")
async def get_user(current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    if str(current_user.role).lower() == "admin":
        existing_user = await db.execute(select(models.User))
    else:
        existing_user = "you are not admin lol"
        
    return existing_user