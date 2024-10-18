from typing import Annotated

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.admin.dependencies import get_clothing, add_clothing, get_size, add_size, \
    update_size, delete_user, delete_clothing, get_users, get_orders_user, order_delete
from src.auth.auth import get_current_admin_user
from src.auth.dependencies import get_user_email
from src.auth.schemas import UserBase
from src.database import get_async_session
from src.logger_error import logger
from src.admin.schemas import CreateClothing, DeleteClothing, UserResponse, OrdersUser
from src.order.dependencies import get_order

router = APIRouter(
    prefix='/admin',
    tags=['Admin'],
    dependencies=[Depends(get_current_admin_user)]
)


@router.post('/clothing/', response_model=CreateClothing)
async def add_clothing_size(
        db: Annotated[AsyncSession, Depends(get_async_session)],
        create_clothing: CreateClothing
):
    """
    Add clothing and size.

        Params:
            name (string): Only letters, characters > 3 and < 20.
            size (string): Size xxs, xs, s, m, l, xl, xxl, xxxl.
            quantity (integer): Quantity clothing more 0.

        Returns:
            Clothing, size and quantity.
    """
    try:
        clothing = await get_clothing(db, create_clothing.name)
        if clothing is None:
            new_clothing = await add_clothing(db, create_clothing.name)
        else:
            new_clothing = clothing
        size = await get_size(db, create_clothing.size, new_clothing.id)
        if size is not None:
            increment_quantity = size.quantity + create_clothing.quantity
            await update_size(db, size.clothing_id, increment_quantity)
            return JSONResponse(content={
                'status': 'success',
                'message': f'Added {create_clothing.quantity} units'
                f' {create_clothing.name} '
                f'size {create_clothing.size}'
            })
        await add_size(db, new_clothing.id, create_clothing.size, create_clothing.quantity)
        return create_clothing
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f'Database error: {error}'
        )
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=500,
            detail=f'Server error: {error}'
        )


@router.get('/users/', response_model=list[UserResponse])
async def get_all_user(
        db: Annotated[AsyncSession, Depends(get_async_session)],
):
    """
    Get users all.

        Returns:
            All users.
    """
    try:
        user = await get_users(db)
        return user
    except HTTPException as error:
        logger.error(error)
        raise error
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=500,
            detail=f'Server error: {error}'
        )


@router.delete('/users/', response_model=UserBase)
async def delete_user_by_email(
        db: Annotated[AsyncSession, Depends(get_async_session)],
        email: EmailStr
):
    """
    Delete user by email.

        Params:
            email (email): Email must be between 9 and 40 characters.

        Returns:
            User.
    """
    try:
        user = await get_user_email(db, email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f'User with email {email} not found'
            )
        await delete_user(db, user)
        return user
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


@router.delete('/clothing/', response_model=DeleteClothing)
async def delete_clothing_by_name(
        name: Annotated[
            str,
            Query(
                title='Name clothing',
                description='The request parameter must be a string,'
                            ' first character capital, example: "Shirt"',
                min_length=3,
                max_length=20,
                pattern='^[A-ZА-Я][a-zа-я]+$'
            )],
        db: Annotated[AsyncSession, Depends(get_async_session)],
):
    """
    Delete clothing by name.

        Params:
            name (string): Only letters, characters > 3 and < 20.

        Returns:
            Clothing.
    """
    try:
        clothing = await get_clothing(db, name)
        if not clothing:
            raise HTTPException(
                status_code=404,
                detail=f'Clothing with name {name} not found'
            )
        await delete_clothing(db, clothing)
        return clothing
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


@router.get('/orders/{email}/', response_model=list[OrdersUser])
async def get_orders_by_email(
        db: Annotated[AsyncSession, Depends(get_async_session)], email: EmailStr
):
    """
    Get orders users by email.

        Params:
            email (email): Email must be between 9 and 40 characters.

        Returns:
            Order user.
    """
    try:
        orders = await get_orders_user(db, email)
        if not orders:
            raise HTTPException(
                status_code=404,
                detail=f'The user with email {email} has no orders'
            )
        return orders
    except HTTPException as error:
        logger.error(error)
        raise error

    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=500,
            detail=f'Server error: {error}'
        )


@router.delete('/orders/', response_model=OrdersUser)
async def delete_orders_user(
        email: EmailStr,
        name: Annotated[
            str,
            Query(
                title='Name clothing',
                description='The request parameter must be a string,'
                            ' first character capital, example: "Shirt"',
                min_length=3,
                max_length=20,
                pattern='^[A-ZА-Я][a-zа-я]+$'
            )],
        db: Annotated[AsyncSession, Depends(get_async_session)]
):
    """
    Delete orders by email user and name clothing.

        Params:
            email (email): User email must be between 9 and 40 characters.
            name (string): Name clothing should contain only letters and first character capital.

        Returns:
            Order.
    """
    try:
        order = await get_order(db, email, name)
        if not order:
            raise HTTPException(
                status_code=409,
                detail=f'The user with email address {email} does not have an '
                       f'order for the {name}'
            )
        await order_delete(db, order)
        return order
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
