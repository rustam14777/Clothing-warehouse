from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.clothing.models import Clothing


async def get_clothing_and_size(db: AsyncSession, clothing_name: str) -> Clothing:
    clothing_sizes = select(Clothing).filter(Clothing.name == clothing_name).options(
        selectinload(Clothing.sizes)
    )
    result = await db.execute(clothing_sizes)
    return result.scalars().first()


async def get_clothing_all(db: AsyncSession) -> [Clothing]:
    clothing = select(Clothing)
    result = await db.execute(clothing)
    return result.scalars().all()
