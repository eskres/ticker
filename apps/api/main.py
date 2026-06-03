from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from routes import authorize_router, callback_router, token_router
from contextlib import asynccontextmanager
import httpx
from scheduler import scheduler
from db import init_db

saxo_client_id = os.getenv("SAXO_CLIENT_ID")
saxo_auth_url = os.getenv("SAXO_AUTH_URL")
saxo_token_url = os.getenv("SAXO_TOKEN_URL")
saxo_redirect_uri = os.getenv("SAXO_REDIRECT_URI")
ticker_base_url = os.getenv("TICKER_BASE_URL")

env = (saxo_client_id, saxo_auth_url, saxo_token_url, saxo_redirect_uri, ticker_base_url)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    if not all(env):
        raise ValueError("Environment variables missing")
    init_db()
    async with httpx.AsyncClient() as client:
        _app.state.client = client
        scheduler.start()
        yield
        scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(authorize_router)
app.include_router(callback_router)
app.include_router(token_router)
