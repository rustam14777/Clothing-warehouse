from datetime import date

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.clothing.models import Clothing
from src.order.models import Order


async def get_order(db: AsyncSession, email: EmailStr, name_clothing: str) -> Order:
    order = select(Order).filter(
        Order.email_user == email, Order.name_clothing == name_clothing
    )
    ref = await db.execute(order)
    return ref.scalars().first()


async def add_order(
        db: AsyncSession, name: str, birthdate: date, email: EmailStr,
        name_clothing: str, size: str
) -> Order:
    order = Order(name_user=name, birthdate=birthdate,
                  email_user=email, name_clothing=name_clothing, size=size)
    db.add(order)
    return order


async def update_quantity_size(db: AsyncSession, clothing_size: Clothing, size: str):
    quantity_size = next(s for s in clothing_size.sizes if s.size == size)
    quantity_size.quantity -= 1
    db.add(quantity_size)
