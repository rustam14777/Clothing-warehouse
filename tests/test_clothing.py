from httpx import AsyncClient


async def test_get_all_clothing(async_client: AsyncClient, authorize_user):
    response = await async_client.get(
        '/clothing/',
        headers={'Authorization': f'Bearer {authorize_user}'}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [{
        'name': 'Shirt'
    }]


async def test_get_clothing_sizes_success(async_client: AsyncClient, authorize_user):
    response = await async_client.get(
        '/clothing/Shirt/sizes/',
        headers={'Authorization': f'Bearer {authorize_user}'}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [{
        'size': 'M',
        'quantity': 10
    }]


async def test_get_clothing_sizes_not_found(async_client: AsyncClient, authorize_user):
    response = await async_client.get(
        '/clothing/Gloves/sizes/',
        headers={'Authorization': f'Bearer {authorize_user}'}
    )

    assert response.status_code == 404
    assert response.json() == {
        'detail': 'Clothing with name Gloves not found'
    }


async def test_get_clothing_sizes_no_sizes(async_client: AsyncClient, authorize_user, add_clothing):
    response = await async_client.get(
        '/clothing/Cap/sizes/',
        headers={'Authorization': f'Bearer {authorize_user}'}
    )

    assert response.status_code == 409
    assert response.json() == {
        'detail': 'There are no sizes for this clothing'
    }
