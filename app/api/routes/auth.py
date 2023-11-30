from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from ..config import settings
from ..models import Token, User, UserCreate
from ..utils import pwd_context, get_current_user

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


@router.post("/users/", response_model=User)
async def create_user(request: Request, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    user_data = user.model_dump()
    user_data["password"] = hashed_password
    user_data['cards'] = []

    await request.app.database["users"].insert_one(user_data)

    return user


@router.post('/token', response_model=Token)
async def login_for_access_token(
        request: Request,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await request.app.database["users"].find_one(
        {"username": form_data.username}
    )
    if user is None or not pwd_context.verify(
            form_data.password, user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
    access_token = create_access_token(
        data={"sub": user.get('username')}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
