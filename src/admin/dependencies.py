from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.clothing.models import Clothing, Size
from src.order.models import Order


async def get_users(db: AsyncSession) -> [User]:
    user = select(User)
    result = await db.execute(user)
    return result.scalars().all()


async def get_clothing(db: AsyncSession, name: str) -> Clothing | None:
    clothing = select(Clothing).filter(Clothing.name == name)
    result = await db.execute(clothing)
    return result.scalars().first()


async def add_clothing(db: AsyncSession, name: str) -> Clothing:
    new_clothing = Clothing(name=name)
    db.add(new_clothing)
    return new_clothing


async def get_size(db, size: str, clothing_id: int) -> Size | None:
    size = select(Size).filter(Size.size == size, Size.clothing_id == clothing_id)
    result = await db.execute(size)
    return result.scalars().first()


async def update_size(db: AsyncSession, clothing_id: int, increment_quantity: int) -> Size | None:
    add_quantity = update(Size).filter(Size.clothing_id == clothing_id).values(
        quantity=increment_quantity).returning(Size)
    result = await db.execute(add_quantity)
    return result.scalars().first()


async def add_size(db: AsyncSession, id_clothing: int, size: str, quantity: int) -> Size:
    size = Size(clothing_id=id_clothing, size=size, quantity=quantity)
    db.add(size)
    return size


async def delete_user(db: AsyncSession, user: User) -> User:
    await db.delete(user)
    return user


async def delete_clothing(db: AsyncSession, clothing: Clothing) -> Clothing:
    await db.delete(clothing)
    return clothing


async def get_orders_user(db: AsyncSession, email: EmailStr) -> [Order]:
    orders = select(Order).filter(Order.email_user == email)
    result = await db.execute(orders)
    return result.scalars().all()


async def order_delete(db: AsyncSession, order: Order):
    await db.delete(order)
    return order
