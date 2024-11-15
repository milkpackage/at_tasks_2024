import pytest
import httpx
import aiohttp
from api_data import api_key, api_token

@pytest.fixture
async def aiohttp_client():
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.fixture
def auth_params():
    return {
        "key": api_key,
        "token": api_token
    }

@pytest.fixture
def base_url():
    return "https://api.trello.com/1"

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client