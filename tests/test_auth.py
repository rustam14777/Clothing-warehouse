from unittest.mock import patch

from httpx import AsyncClient

from fastapi.security import OAuth2PasswordRequestForm


async def test_register(async_client: AsyncClient):
    user = {
        'name': 'Roma',
        'surname': 'Dava',
        'email': 'roma@mail.ru',
        'birthdate': '2012-12-12',
        'password': 'roma2012'
    }
    response = await async_client.post('/auth/register/', json=user)

    assert response.status_code == 200
    assert response.json() == {
        'name': 'Roma',
        'surname': 'Dava',
        'email': 'roma@mail.ru',
        'birthdate': '2012-12-12',
        'id': 3,
        'is_active': True,
        'is_admin': False,
        'is_user': True
    }


async def test_get_token_for_admin_and_access_rights(
        async_client: AsyncClient, registered_admin_fixture
):
    response = await async_client.post(
        '/auth/token/',
        data={
            'username': 'admin@mail.ru',
            'password': 'testpassword'
        }
    )
    access_token = response.json()['access_token']

    assert response.status_code == 200
    assert len(access_token) > 0
    assert isinstance(access_token, str)
    assert registered_admin_fixture.is_admin is True


async def test_get_token_for_user_and_access_rights(
        async_client: AsyncClient, registered_user_fixture
):
    response = await async_client.post(
        '/auth/token/',
        data={
            'username': 'user@mail.ru',
            'password': 'testpassword'
        }
    )
    access_token = response.json()['access_token']

    assert response.status_code == 200
    assert len(access_token) > 0
    assert isinstance(access_token, str)
    assert registered_user_fixture.is_admin is False


async def test_get_token_unauthorized(async_client: AsyncClient):
    response = await async_client.post(
        '/auth/token/',
        data={
            'username': 'falsuser@mail.ru',
            'password': 'testpassword'
        }
    )

    assert response.status_code == 401


async def test_register_and_login(async_client: AsyncClient):
    user_data = {
        'name': 'Test',
        'surname': 'User',
        'birthdate': '2000-02-12',
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = await async_client.post('/auth/register/', json=user_data)

    assert response.status_code == 200

    form_data = OAuth2PasswordRequestForm(
        username=user_data['email'],
        password=user_data['password']
    )
    response = await async_client.post(
        '/auth/token/',
        data={
            'username': form_data.username,
            'password': form_data.password
        }
    )

    assert response.status_code == 200

    access_token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    response = await async_client.get('/auth/users/me/', headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        'name': 'Test',
        'surname': 'User',
        'email': 'test@example.com',
        'birthdate': '2000-02-12',
        'id': 5,
        'is_active': True,
        'is_admin': False,
        'is_user': True
    }


async def test_create_user_email_already_exists(async_client: AsyncClient):
    user_data = {
        'name': 'Test',
        'surname': 'User',
        'birthdate': '2000-01-01',
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = await async_client.post('/auth/register/', json=user_data)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Email already registered'


async def test_login_for_access_token_invalid_credentials(async_client: AsyncClient):
    form_data = OAuth2PasswordRequestForm(username='test@example.com', password='wrong_password')
    response = await async_client.post(
        'auth/token/',
        data={
            'username': form_data.username,
            'password': form_data.password
        }
    )

    assert response.status_code == 401
    assert response.json()['detail'] == 'Incorrect email or password'


async def test_internal_server_error_500(async_client: AsyncClient):
    with patch('src.auth.router.add_user', side_effect=Exception('Server error')):
        response = await async_client.post(
            '/auth/register/',
            json={
                'name': 'John',
                'surname': 'Damir',
                'email': 'johndamir@mail.ru',
                'birthdate': '2000-01-01',
                'password': 'johnpassword'
            }
        )

        assert response.status_code == 500
        assert 'Server error: Server error' in response.json().get('detail')


async def test_error_handling(async_client: AsyncClient):
    response = await async_client.get('/NonExistingPathError')

    assert response.status_code == 404
    assert 'Not Found' in response.json().get('detail')
