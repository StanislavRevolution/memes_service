import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.database import async_session_maker_nullpool, engine_nullpool
from app.memes.models import Memes

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="module")
async def test_app():
    async with async_session_maker_nullpool() as session:
        async with engine_nullpool.begin() as conn:
            await conn.run_sync(Memes.metadata.create_all)
        yield app
        async with engine_nullpool.begin() as conn:
            await conn.run_sync(Memes.metadata.drop_all)


@pytest.fixture(scope="module")
async def client(test_app: FastAPI):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
async def test_db():
    async with async_session_maker_nullpool() as session:
        yield session


@pytest.mark.asyncio
async def test_create_meme(client: AsyncClient, test_db: AsyncSession):
    response = await client.post("/memes", data={"title": "Test Meme"}, files={"upload_file": ("filename", b"filecontent")})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Meme"


@pytest.mark.asyncio
async def test_get_memes(client: AsyncClient, test_db: AsyncSession):
    response = await client.get("/memes")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_get_meme_by_id(client: AsyncClient, test_db: AsyncSession):
    response = await client.post("/memes", data={"title": "Another Meme"}, files={"upload_file": ("filename", b"filecontent")})
    assert response.status_code == 200
    meme_id = response.json()["id"]

    response = await client.get(f"/memes/{meme_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Another Meme"


@pytest.mark.asyncio
async def test_update_meme(client: AsyncClient, test_db: AsyncSession):
    response = await client.post("/memes", data={"title": "Update Meme"}, files={"upload_file": ("filename", b"filecontent")})
    assert response.status_code == 200
    meme_id = response.json()["id"]

    response = await client.put(f"/memes/{meme_id}", json={"title": "Updated Meme"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Meme"


@pytest.mark.asyncio
async def test_delete_meme(client: AsyncClient, test_db: AsyncSession):
    response = await client.post("/memes", data={"title": "Delete Meme"}, files={"upload_file": ("filename", b"filecontent")})
    assert response.status_code == 200
    meme_id = response.json()["id"]

    response = await client.delete(f"/memes/{meme_id}")
    assert response.status_code == 200

    response = await client.get(f"/memes/{meme_id}")
    assert response.status_code == 404
