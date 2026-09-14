import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "bdunab2")
COLL_NAME = os.getenv("COLL_NAME", "items")


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    try:
        # Comprobar la conexión antes de aceptar solicitudes.
        await client.admin.command("ping")
        app.state.collection = client[DB_NAME][COLL_NAME]
        yield
    finally:
        client.close()


def get_collection(request: Request) -> AsyncIOMotorCollection:
    return request.app.state.collection


Collection = Annotated[AsyncIOMotorCollection, Depends(get_collection)]
