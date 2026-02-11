from bson.objectid import ObjectId
from app.shared.db import get_db


async def create_lead(data: dict) -> dict:
    res = await get_db().leads.insert_one(data)
    doc = await get_db().leads.find_one({"_id": res.inserted_id})
    return doc


async def list_leads() -> list:
    docs = []
    cursor = get_db().leads.find()
    async for d in cursor:
        d["id"] = str(d["_id"])
        del d["_id"]
        docs.append(d)
    return docs


async def get_lead(id: str) -> dict | None:
    try:
        obj = ObjectId(id)
    except Exception:
        return None

    doc = await get_db().leads.find_one({"_id": obj})
    if not doc:
        return None

    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc
