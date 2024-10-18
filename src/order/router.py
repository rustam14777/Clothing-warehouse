from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import get_current_user
from src.auth.models import User
from src.clothing.dependencies import get_clothing_and_size
from src.database import get_async_session
from src.logger_error import logger
from src.order.dependencies import get_order, add_order, update_quantity_size
from src.order.schemas import CreateOrder

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.post('/', response_model=CreateOrder)
async def create_order_for_user(
        db: Annotated[AsyncSession, Depends(get_async_session)],
        current_user: Annotated[User, Depends(get_current_user)],
        create_order: CreateOrder
):
    """
    Add orders for get a clothing.

        Params:
            name (string): Name clothing.
            size (string): Size clothing.

        Returns:
            Order for user.
    """
    try:
        clothing_sizes = await get_clothing_and_size(db, create_order.name)
        if not clothing_sizes:
            raise HTTPException(
                status_code=404,
                detail=f'Clothing with name {create_order.name} not found'
            )
        if create_order.size not in {o.size for o in clothing_sizes.sizes if o.quantity > 0}:
            raise HTTPException(
                status_code=404,
                detail=f'The {create_order.name} size {create_order.size} are out of '
                       f'stock'
            )
        order = await get_order(db, current_user.email, create_order.name)
        if order:
            raise HTTPException(
                status_code=409,
                detail=f'You have already ordered {create_order.name}'
            )
        await add_order(db, current_user.name, current_user.birthdate, current_user.email,
                        create_order.name, create_order.size)
        await update_quantity_size(db, clothing_sizes, create_order.size)
        return create_order
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f'Database error: {error}'
        )
    except HTTPException as error:
        logger.error(error)
        raise error
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=500,
            detail=f'Server error: {error}'
        )
