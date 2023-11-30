import pytest

import motor.motor_asyncio
from httpx import AsyncClient

from api.main import app
from api.config import settings
from api.models import Card


@pytest.fixture
def test_db_app():
    def test_start_db_client():
        app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(settings.TEST_DATABASE_URL)
        app.database = app.mongodb_client['test']

    def test_drop_db():
        app.mongodb_client.drop_database('test')
        app.mongodb_client.close()

    app.on_event('startup')(test_start_db_client)
    app.on_event('shutdown')(test_drop_db)

    test_start_db_client()
    return app


@pytest.fixture
def async_client(test_db_app):
    return AsyncClient(app=test_db_app, base_url="http://test")


@pytest.fixture
async def client_token(async_client, test_db_app):
    data = {
        'username': 'test',
        'password': 'testpass12'
    }

    card = {
        "id": '1', "name": "#killallzombies",
        "genre": ["Shooter"],
        "developers": ["Beatshapers"],
        "publishers": ["Beatshapers"],
        "releaseDates": {
            "Japan": "Unreleased", "NorthAmerica": "Nov 12, 2014",
            "Europe": "Oct 28, 2014",
            "Australia": "Oct 28, 2014"
        }
    }
    card = Card(**card)
    await test_db_app.database['cards'].insert_one(card.model_dump())

    async with async_client as client:
        await client.post('/api/v1/users/', json=data)
        token_response = await client.post('/api/v1/token', data=data)

    access_token = token_response.json()['access_token']

    return AsyncClient(
        app=test_db_app,
        base_url="http://test", headers={'Authorization': f'Bearer {access_token}'}
    )
