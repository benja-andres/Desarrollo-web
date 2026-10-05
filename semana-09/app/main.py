from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse

from persona1.app.auth import current_user, login, logout
from persona1.app.products import PRODUCTS, delete_product

app = FastAPI(title="Autenticación y autorización - Semana 09")
FRONTEND_FILE = Path(__file__).parents[2] / "persona2" / "frontend" / "index.html"


class LoginData(BaseModel):
    username: str
    password: str


@app.get("/")
def home() -> FileResponse:
    return FileResponse(FRONTEND_FILE)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "OK"}


@app.post("/auth/login")
def auth_login(data: LoginData, response: Response) -> dict[str, str]:
    return login(data.username, data.password, response)


@app.get("/auth/me")
def me(user: dict[str, object] = Depends(current_user)) -> dict[str, object]:
    return user


@app.post("/auth/logout")
def auth_logout(request: Request, response: Response) -> dict[str, str]:
    return logout(request, response)


@app.get("/api/products")
def list_products(_: dict[str, object] = Depends(current_user)) -> list[dict[str, object]]:
    return PRODUCTS


@app.delete("/api/products/{product_id}")
def remove_product(
    product_id: int,
    user: dict[str, object] = Depends(current_user),
) -> dict[str, str]:
    if "admin" not in user["roles"]:
        raise HTTPException(status_code=403, detail="Se requiere el rol admin")
    if not delete_product(product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": f"Producto {product_id} eliminado"}
