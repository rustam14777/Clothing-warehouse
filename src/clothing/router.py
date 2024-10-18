from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import get_current_user
from src.clothing.dependencies import get_clothing_all, get_clothing_and_size
from src.clothing.schemas import ClothingResponse, SizeResponse
from src.database import get_async_session
from src.logger_error import logger

router = APIRouter(
    prefix='/clothing',
    tags=['Clothing'],
    dependencies=[Depends(get_current_user)]
)


@router.get('/', response_model=list[ClothingResponse])
async def get_all_clothing(db: Annotated[AsyncSession, Depends(get_async_session)]):
    """
    Returning all clothing.

        Returns:
            All clothing.
    """
    try:
        clothing = await get_clothing_all(db)
        return clothing
    except HTTPException as error:
        logger.error(error)
        raise error
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=500,
            detail=f'Server error: {error}'
        )


@router.get('/{name}/sizes/', response_model=list[SizeResponse])
async def get_clothing_sizes(
        name: Annotated[
        str,
        Path(
            title='Name clothing',
            description='The request parameter must be a string, first character capital, example: '
                        '"Shirt"',
            min_length=3,
            max_length=20,
            pattern='^[A-ZА-Я][a-zа-я]+$'
        )],
        db: Annotated[AsyncSession, Depends(get_async_session)]
):
    """
    Get clothing by name.

        Params:
            name (string): Name clothing must be a string and first character capital.

        Returns:
            Sizes for clothing.
    """
    try:
        clothing_size = await get_clothing_and_size(db, name)
        if not clothing_size:
            raise HTTPException(
                status_code=404,
                detail=f'Clothing with name {name} not found'
            )
        size = [o for o in clothing_size.sizes if o.quantity > 0]
        if not size:
            raise HTTPException(
                status_code=409,
                detail='There are no sizes for this clothing'
            )
        return size
    except HTTPException as error:
        logger.error(error)
        raise error
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=500,
            detail=f'Server error: {error}'
        )
