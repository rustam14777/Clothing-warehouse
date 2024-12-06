from datetime import date

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User


async def get_user_email(db: AsyncSession, email: EmailStr) -> User:
    user = select(User).filter(User.email == email)
    result = await db.execute(user)
    return result.scalars().first()


async def add_user(
        db: AsyncSession, name: str, surname: str, birthdate: date, email: EmailStr,
        hashed_password: str
) -> User:
    user = User(
        name=name, surname=surname, birthdate=birthdate, email=email,
        hashed_password=hashed_password)
    db.add(user)
    return user


async def get_admin(db: AsyncSession) -> User:
    admin = select(User).filter(User.is_admin == True) # noqa
    result = await db.execute(admin)
    return result.scalars().first()
