from pydantic import BaseModel


class Card(BaseModel):
    id: str
    name: str
    genre: list[str]
    developers: list[str]
    publishers: list[str]
    releaseDates: dict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str


class User(UserCreate):
    cards: list[Card] = []
