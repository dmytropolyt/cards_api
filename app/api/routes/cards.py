from fastapi import APIRouter, Depends, HTTPException, Request

from ..models import Card, User
from ..utils import get_current_user

router = APIRouter()


@router.post('/users/me/add-card/{card_name}', response_model=User)
async def add_card_to_user(
        request: Request,
        card_name: str,
        current_user: User = Depends(get_current_user)
):
    print(card_name)
    print('some')
    card = await request.app.database['cards'].find_one({'name': card_name})
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    current_user['cards'].append(card)
    await request.app.database['users'].update_one(
        {"_id": current_user["_id"]},
        {"$set": {"cards": current_user["cards"]}}
    )
    return current_user


@router.delete('/users/me/remove-card/{card_name}', response_model=User)
async def remove_card_from_user(
        request: Request,
        card_name: str,
        current_user: User = Depends(get_current_user)
):
    await request.app.database['users'].update_one(
        {'_id': current_user['_id']},
        {'$pull': {'cards': {'name': card_name}}}
    )
    return current_user


@router.get('/users/me/cards')
async def get_my_cards(
        current_user: User = Depends(get_current_user)
) -> list[Card]:
    return current_user.get('cards', [])


@router.get('/users/{username}/cards')
async def get_user_cards(
        request: Request,
        username: str, current_user: User = Depends(get_current_user)
) -> list[Card]:
    user = await request.app.database['users'].find_one({'username': username})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.get('cards', [])
