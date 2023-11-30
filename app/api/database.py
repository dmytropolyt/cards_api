import motor.motor_asyncio

from fastapi import Request


async def get_database(request: Request) -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return request.app.database
