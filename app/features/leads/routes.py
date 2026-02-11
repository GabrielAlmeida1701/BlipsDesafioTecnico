from fastapi import APIRouter, HTTPException
from .schemas import LeadCreate, LeadResponse
from . import repository
from app.shared.services import fetch_birth_date

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(payload: LeadCreate):
    birth = await fetch_birth_date()

    doc = payload.dict()
    doc["birth_date"] = birth
    created = await repository.create_lead(doc)

    if not created:
        raise HTTPException(status_code=500, detail="Failed to create lead")
    
    created["id"] = str(created["_id"]) if "_id" in created else created.get("id")
    if "_id" in created:
        del created["_id"]
    return created


@router.get("", response_model=list[LeadResponse])
async def list_all():
    return await repository.list_leads()


@router.get("/{id}", response_model=LeadResponse)
async def get_one(id: str):
    lead = await repository.get_lead(id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
