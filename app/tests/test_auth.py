import pytest


@pytest.mark.asyncio
class TestAuth:
    """Test auth routes."""

    data = {
        'username': 'test',
        'password': 'testpass12'
    }

    async def test_create_user(self, async_client):

        async with async_client as client:
            response = await client.post('/api/v1/users/', json=self.data)

        assert response.status_code == 200
        assert response.json()['username'] == self.data['username']

    async def test_login_for_access_token(self, async_client):

        async with async_client as client:
            await client.post('/api/v1/users/', json=self.data)
            response = await client.post('/api/v1/token', data=self.data)

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['token_type'] == 'bearer'
        assert len(response_data['access_token']) > 0

    async def test_get_user_me(self, client_token):
        client_token = await client_token
        async with client_token as client:
            response = await client.get('/api/v1/users/me/')

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['username'] == self.data['username']
        assert 'password' in response_data
        assert 'cards' in response_data
