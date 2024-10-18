from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_user_email, add_user
from src.auth.auth import get_password_hash, authenticate_user, create_access_token, \
    get_current_user
from src.config import settings
from src.database import get_async_session
from src.auth.schemas import User, CreateUser, Token
from src.logger_error import logger

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register/',  response_model=User)
async def create_user(user: CreateUser, db: AsyncSession = Depends(get_async_session)):
    """
    Register user.

        Params:
            name (string): Only letters, characters > 4 and < 40.
            surname (string): Only letters, characters > 4 and < 40.
            email (email): Email address.
            birthdate (date): Format 2000-01-30.
            password (string): Min length 6 characters.

        Returns:
            User created.
    """
    try:
        db_user = await get_user_email(db, user.email)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail='Email already registered'
            )
        hashed_password = get_password_hash(user.password)
        db_add_user = await add_user(
            db, user.name, user.surname, user.birthdate, user.email,
            hashed_password
        )
        return db_add_user
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


@router.post('/token/', response_model=Token)
async def login_for_access_token(
        db: Annotated[AsyncSession, Depends(get_async_session)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Login and get token, enter params for username and password, where name your email address and
    password your password.

        Params:
            username (email): Your email.
            password (string): Your password.

        Returns:
            Token.
    """
    try:
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': user.email}, expires_delta=access_token_expires
        )
        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }
    except HTTPException as error:
        logger.error(error)
        raise error
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=500,
            detail=f'Server error: {error}'
        )


@router.get('/users/me/', response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user.

        Returns:
            Current user.
    """
    return current_user
