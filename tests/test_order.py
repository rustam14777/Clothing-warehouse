from httpx import AsyncClient


async def test_create_order_success(async_client: AsyncClient, authorize_user):
    order_data = {"name": "Shirt", "size": "M"}
    response = await async_client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {authorize_user}"},
        json=order_data
    )

    assert response.status_code == 200
    assert response.json() == order_data


async def test_create_order_clothing_not_found(async_client: AsyncClient, authorize_user):
    order_data = {"name": "Boots", "size": "M"}
    response = await async_client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {authorize_user}"},
        json=order_data
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Clothing with name Boots not found"}


async def test_create_order_size_out_of_stock(async_client: AsyncClient, authorize_user):
    order_data = {"name": "Shirt", "size": "XXL"}
    response = await async_client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {authorize_user}"},
        json=order_data
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "The Shirt size XXL are out of stock"}


async def test_create_order_already_ordered(async_client: AsyncClient, authorize_user):
    order_data = {"name": "Shirt", "size": "M"}
    await async_client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {authorize_user}"},
        json=order_data
    )

    response = await async_client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {authorize_user}"},
        json=order_data
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "You have already ordered Shirt"}
