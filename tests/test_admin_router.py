
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient


async def test_add_clothing_size(async_client: AsyncClient, authorize_admin):
    clothing_data = {
        'name': 'Shirt',
        'size': 'M',
        'quantity': 10
    }

    response = await async_client.post(
        '/admin/clothing/',
        json=jsonable_encoder(clothing_data),
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 200
    assert response.json() == {
        'name': clothing_data['name'],
        'size': clothing_data['size'],
        'quantity': clothing_data['quantity']
    }


async def test_add_clothing_invalid_name(async_client: AsyncClient, authorize_admin):
    invalid_name = 'T-Short@'
    response = await async_client.post(
        '/admin/clothing/',
        headers={'Authorization': f'Bearer {authorize_admin}'},
        json={
            'name': invalid_name,
            'size': 'M',
            'quantity': 10
        }
    )

    assert response.status_code == 422


async def test_get_all_user(async_client: AsyncClient, authorize_admin):
    response = await async_client.get(
        '/admin/users/',
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_delete_user_by_email(async_client: AsyncClient, authorize_admin):
    user = {
        'name': 'userdel',
        'surname': 'test',
        'email': 'userdel@mail.ru',
        'birthdate': '2012-12-12',
        'password': 'testuser'
    }
    response_repeated = await async_client.post('/auth/register/', json=user)

    assert response_repeated.status_code == 200

    response = await async_client.delete(
        f'/admin/users/?email={user['email']}',
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 200
    assert response.json()['email'] == 'userdel@mail.ru'


async def test_delete_user_not_found(async_client: AsyncClient, authorize_admin):
    email = 'nonuser@mail.ru'
    response = await async_client.delete(
        f'/admin/users/?email={email}',
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 404
    assert response.json() == {'detail': f'User with email {email} not found'}


async def test_delete_clothing_by_name(async_client: AsyncClient, authorize_admin):
    cloth = {
        'name': 'Coat',
        'size': 'L',
        'quantity': 12
    }
    response_add_cloth = await async_client.post(
        '/admin/clothing/',
        json=cloth,
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response_add_cloth.status_code == 200

    response = await async_client.delete(
        f'/admin/clothing/?name={cloth['name']}',
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'Coat'


async def test_delete_clothing_not_found(async_client: AsyncClient, authorize_admin):
    name = 'Boots'
    response = await async_client.delete(
        f'/admin/clothing/?name={name}',
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 404
    assert response.json() == {'detail': f'Clothing with name {name} not found'}


async def test_get_orders_by_email(async_client: AsyncClient, authorize_admin, add_order):
    response = await async_client.get(
        '/admin/orders/usertest@mail.ru/',
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            'name_user': 'Usertest',
            'birthdate': '2000-01-01',
            'email_user': 'usertest@mail.ru',
            'name_clothing': 'Shirt',
            'size': 'M'
        }
    ]


async def test_get_orders_by_email_if_not_order(async_client: AsyncClient, authorize_admin):
    response = await async_client.get(
        '/admin/orders/user@example.com/',
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 404
    assert not isinstance(response.json(), list)


async def test_delete_orders_user(async_client: AsyncClient, authorize_admin):
    name = 'Shirt'
    email = 'usertest@mail.ru'
    response = await async_client.delete(
        f'/admin/orders/?email={email}&name={name}',
        headers={'Authorization': f'Bearer {authorize_admin}'}
    )

    assert response.status_code == 200
    assert response.json() == {
        'name_user': 'Usertest',
        'birthdate': '2000-01-01',
        'email_user': 'usertest@mail.ru',
        'name_clothing': 'Shirt',
        'size': 'M'
    }


async def test_delete_orders_user_if_not_order(async_client: AsyncClient, authorize_admin):
    email = 'testorder@mail.ru'
    name = 'Shirt'
    response = await async_client.delete(
            f'/admin/orders/?email={email}&name={name}',
            headers={'Authorization': f'Bearer {authorize_admin}'}
        )

    assert response.status_code == 409
    assert response.json() == {
        'detail': f'The user with email address {email} does not have an order for the {name}'
    }
