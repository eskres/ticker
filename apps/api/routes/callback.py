import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from db import get_pkce, save_tokens

token_url = os.getenv('SAXO_TOKEN_URL')
client_id = os.getenv('SAXO_CLIENT_ID')
redirect_uri = os.getenv('SAXO_REDIRECT_URI')
base_url = os.getenv('TICKER_BASE_URL')

callback_router = APIRouter()


@callback_router.get("/callback")
async def callback(request: Request, code: str, state: str):
    code_verifier = get_pkce(state)
    if not code_verifier:
        raise HTTPException(status_code=400, detail='State not found')

    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier[0],
    }

    client = request.app.state.client
    token_raw = await client.post(token_url, data=data)

    try:
        token_data = token_raw.json()
    except Exception:
        token_raw.raise_for_status()
        raise HTTPException(status_code=502, detail="Token endpoint returned invalid response")
    if "error" in token_data:
        raise HTTPException(status_code=400, detail=token_data["error"])

    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    save_tokens(access_token, refresh_token)

    return RedirectResponse(base_url)