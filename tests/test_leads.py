import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_lead(monkeypatch):
    async def fake_fetch_birth_date():
        return "1998-02-05"

    async def fake_create_lead(data):
        return {"_id": "507f1f77bcf86cd799439011", **data}

    monkeypatch.setattr("app.features.leads.routes.fetch_birth_date", fake_fetch_birth_date)
    monkeypatch.setattr("app.features.leads.repository.create_lead", fake_create_lead)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/leads", json={"name": "João", "email": "joao@example.com", "phone": "+5511999"})

    assert resp.status_code == 201
    body = resp.json()
    
    assert body["name"] == "João"
    assert body["birth_date"] == "1998-02-05"
    assert "id" in body


@pytest.mark.asyncio
async def test_list_and_get(monkeypatch):
    sample = [{"id": "1", "name": "A", "email": "a@a.com", "phone": "p", "birth_date": None}]

    async def fake_list_leads():
        return sample

    async def fake_get_lead(id: str):
        return sample[0] if id == "1" else None

    monkeypatch.setattr("app.features.leads.repository.list_leads", fake_list_leads)
    monkeypatch.setattr("app.features.leads.repository.get_lead", fake_get_lead)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        rlist = await ac.get("/leads")
        rget = await ac.get("/leads/1")

    assert rlist.status_code == 200
    assert rget.status_code == 200
    assert rlist.json() == sample
    assert rget.json()["id"] == "1"
