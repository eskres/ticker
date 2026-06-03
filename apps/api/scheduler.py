import os
from db import get_tokens, save_tokens
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

token_url = os.getenv('SAXO_TOKEN_URL')

async def refresh_tokens():
    tokens = get_tokens()
    if not tokens:
        return

    access_token, refresh_token, code_verifier = tokens

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "code_verifier": code_verifier,
    }

    async with httpx.AsyncClient() as client:
        token_raw = await client.post(token_url, data=data)
        try:
            token_data = token_raw.json()
        except Exception:
            token_raw.raise_for_status()
            raise Exception("Token endpoint returned invalid response")
        if "error" in token_data:
            raise Exception(token_data["error"])

        access_token = token_data["access_token"]
        refresh_token = token_data["refresh_token"]
        save_tokens(access_token, refresh_token)

scheduler = AsyncIOScheduler()
scheduler.add_job(refresh_tokens, 'interval', minutes=55)
