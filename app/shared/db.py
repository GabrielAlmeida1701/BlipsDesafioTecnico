import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", 'mongodb://mongo:27017')

client: Optional[AsyncIOMotorClient] = None
conn = None

async def connect_to_mongo():
    global client, conn
    client = AsyncIOMotorClient(MONGO_URL)
    conn = client.leadsdb

async def close_mongo_connection():
    print('Closing MongoDB connection')
    global client
    if client:
        client.close()

def get_db():
    global conn
    return conn