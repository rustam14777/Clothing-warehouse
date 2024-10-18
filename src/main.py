from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy.exc import IntegrityError

from src.auth.auth import get_password_hash
from src.auth.dependencies import get_admin
from src.auth.models import User
from src.auth.router import router as router_auth
from src.clothing.router import router as router_clothing
from src.config import settings
from src.database import async_session
from src.logger_request import logger_request
from src.admin.router import router as router_admin
from src.order.router import router as router_order

DESCRIPTION = """
Clothing Orders API welcomes you.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create admin user in database.
    """
    async with async_session() as session:
        admin = await get_admin(session)
        if not admin:
            hashed_password = get_password_hash(settings.PASSWORD_ADMIN)
            user = User(
                name=settings.NAME_ADMIN,
                surname=settings.SURNAME_ADMIN,
                birthdate=settings.BIRTHDATE_ADMIN,
                email=settings.EMAIL_ADMIN,
                hashed_password=hashed_password,
                is_admin=True
            )
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                print("Admin user created")
            except IntegrityError:
                await session.rollback()
                print("Admin user already exists, skipping creation")
        else:
            print("Admin user already exists, skipping creation")
    yield


app = FastAPI(
    title='Clothing Orders',
    description=DESCRIPTION,
    version='0.0.1',
    lifespan=lifespan
)


app.include_router(router_auth)
app.include_router(router_admin)
app.include_router(router_clothing)
app.include_router(router_order)


@app.middleware('http')
async def dispatch(request: Request, call_next):
    name = request.url.path
    method = request.method
    url = request.url
    ip = request.client.host
    logger_request.info(f'Request from {name}: {method} - {url} ip - {ip}')
    response = await call_next(request)
    return response
