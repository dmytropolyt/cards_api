import pytest


@pytest.mark.asyncio
class TestCards:
    """Test cards routes."""

    data = {
        'card_name_url': '%23killallzombies',
        'card_name': '#killallzombies'
    }

    async def test_add_card_to_user(self, client_token):
        client_token = await client_token
        async with client_token as client:
            response = await client.post(
                f'/api/v1/users/me/add-card/{self.data["card_name_url"]}'
            )

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['username'] == 'test'
        assert self.data['card_name'] in response_data['cards'][0].values()

    async def test_get_my_cards(self, client_token):
        client_token = await client_token
        async with client_token as client:
            response = await client.get('/api/v1/users/me/cards')

        response_data = response.json()
        assert response.status_code == 200
        assert self.data['card_name'] in response_data[0].values()

    async def test_remove_card_form_user(self, client_token):
        client_token = await client_token
        async with client_token as client:
            await client.post(f'/api/v1/users/me/add-card/{self.data["card_name_url"]}')
            response_delete = await client.delete(
                f'/api/v1/users/me/remove-card/{self.data["card_name_url"]}'
            )
            response_cards = await client.get('/api/v1/users/me/cards')

        assert response_delete.status_code == 200
        assert response_cards.json() == []

    async def test_get_user_cards(self, client_token):
        client_token = await client_token
        async with client_token as client:
            await client.post(
                f'/api/v1/users/me/add-card/{self.data["card_name_url"]}'
            )
            response = await client.get('/api/v1/users/test/cards')

        response_data = response.json()
        assert response.status_code == 200
        assert self.data['card_name'] in response_data[0].values()
