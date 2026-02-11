from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.features.leads.routes import router as leads_router
from app.shared.db import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title="Leads API", lifespan=lifespan)
app.include_router(leads_router)
