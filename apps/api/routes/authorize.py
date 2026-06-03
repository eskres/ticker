import os
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import secrets
import base64
import hashlib
from db import save_pkce, get_pkce
import urllib.parse

saxo_auth_url = os.getenv("SAXO_AUTH_URL")
client_id = os.getenv("SAXO_CLIENT_ID")
redirect_uri = os.getenv("SAXO_REDIRECT_URI")

authorize_router = APIRouter()

@authorize_router.get("/authorize")
async def authorize():

    state = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode()

    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode()

    sha256 = hashlib.sha256()
    sha256.update(code_verifier.encode())

    code_challenge = base64.urlsafe_b64encode(sha256.digest()).rstrip(b'=').decode()

    save_pkce(state, code_verifier)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
    }

    url = saxo_auth_url + '?' + urllib.parse.urlencode(params)

    return RedirectResponse(url)
