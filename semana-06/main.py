"""Punto de entrada de la API REST de Natural Power."""

from fastapi import FastAPI

from config.db import lifespan
from routes.items import router as items_router
from routes.sistema import router as sistema_router

app = FastAPI(
    title="Natural Power - API REST de items",
    description="Semana 06: CRUD con FastAPI y persistencia en MongoDB.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(sistema_router)
app.include_router(items_router)
