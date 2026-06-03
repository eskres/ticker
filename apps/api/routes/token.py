from fastapi import APIRouter, HTTPException
from db import get_tokens

token_router = APIRouter()

@token_router.get("/token")
async def token():
    tokens = get_tokens()
    if not tokens:
        raise HTTPException(status_code=401, detail='Token not found')

    access_token, _, _ = tokens

    return {"access_token": access_token}