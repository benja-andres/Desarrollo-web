import os

from fastapi import FastAPI
import httpx

app = FastAPI(title="Local API Gateway")

# En el laboratorio con dos hosts: http://192.168.1.20:9000 (HOST B)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:9000")


@app.get("/api/products")
async def products():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/products"
        )
        return response.json()


@app.get("/api/orders")
async def orders():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/orders"
        )
        return response.json()
