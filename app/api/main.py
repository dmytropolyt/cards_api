from fastapi import FastAPI
import motor.motor_asyncio

from .routes.auth import router as auth_router
from .routes.cards import router as cards_router
from .config import settings


app = FastAPI()


@app.on_event('startup')
def start_db_client():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    app.database = app.mongodb_client[settings.MONGO_INITDB_DATABASE]


@app.on_event('shutdown')
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/api/v1/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}


app.include_router(auth_router, prefix='/api/v1', tags=['auth'])
app.include_router(cards_router, prefix='/api/v1', tags=['cards'])
