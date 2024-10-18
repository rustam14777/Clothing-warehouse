from datetime import date
from typing import AsyncGenerator

import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.auth.auth import pwd_context
from src.auth.models import User
from src.clothing.models import Clothing, Size
from src.config import settings
from src.database import Base, get_async_session
from src.main import app
from src.order.models import Order

URL_TEST_DB = settings.async_database_url_test

engine_test = create_async_engine(URL_TEST_DB, poolclass=NullPool)
async_session_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

Base.bind = engine_test


async def override_get_async_session() -> AsyncSession:
    async with async_session_test() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url='http://test', transport=ASGITransport(app=app)) as ac:
        yield ac


@pytest.fixture(scope='session')
async def registered_user_fixture():
    async with async_session_test() as session:
        password_hash = pwd_context.hash('testpassword')
        new_user = User(
            name='TestUser',
            surname='TestSurname',
            email='user@mail.ru',
            birthdate=date(2000, 1, 1),
            hashed_password=password_hash,
        )
        session.add(new_user)
        await session.commit()
        return new_user


@pytest.fixture(scope='session')
async def registered_admin_fixture():
    async with async_session_test() as session:
        password_hash = pwd_context.hash('testpassword')
        new_admin = User(
            name='TestAdmin',
            surname='TestSurname',
            email='admin@mail.ru',
            birthdate=date(2000, 1, 1),
            hashed_password=password_hash,
            is_admin=True
        )
        session.add(new_admin)
        await session.commit()
        return new_admin


@pytest.fixture(scope='session')
async def authorize_user(async_client: AsyncClient, registered_user_fixture):
    response = await async_client.post(
        '/auth/token/',
        data={
            'username': registered_user_fixture.email,
            'password': 'testpassword'
        }
    )

    assert response.status_code == 200
    return response.json()['access_token']


@pytest.fixture(scope='session')
async def authorize_admin(async_client: AsyncClient, registered_admin_fixture):
    response = await async_client.post(
        '/auth/token/',
        data={
            'username': registered_admin_fixture.email,
            'password': 'testpassword'
        }
    )

    assert response.status_code == 200
    return response.json()['access_token']


@pytest.fixture(scope='session')
async def add_order():
    async with async_session_test() as session:
        new_order = Order(
            name_user='Usertest',
            birthdate=date(2000, 1, 1),
            email_user='usertest@mail.ru',
            name_clothing='Shirt',
            size='M'
        )
        session.add(new_order)
        await session.commit()
        return new_order


@pytest.fixture(scope='session')
async def add_clothing():
    async with async_session_test() as session:
        new_clothing = Clothing(
            name='Cap'
        )
        session.add(new_clothing)
        await session.commit()
        new_size = Size(clothing_id=new_clothing.id, size='S', quantity=0)
        session.add(new_size)
        await session.commit()
        return new_size
