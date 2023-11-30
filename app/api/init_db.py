import motor.motor_asyncio

from scrapper.scrapper import Scrapper

from .models import Card
from .config import settings


async def populate_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.MONGO_INITDB_DATABASE]
    cards_collection = db["cards"]

    scrapper = Scrapper()
    all_games = scrapper.get_all_games()

    for game in all_games:
        game['id'] = str(game['id'])

        card_data = Card(**game)
        await cards_collection.insert_one(card_data.model_dump())


if __name__ == '__main__':
    import asyncio

    asyncio.run(populate_db())
