import hmac
import os

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI(
    title="Secure API Gateway",
    description="API Gateway con autenticación Bearer y HashiCorp Vault",
)
security = HTTPBearer(auto_error=False)

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200").rstrip("/")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://192.168.1.20:9000").rstrip("/")

if not VAULT_TOKEN:
    raise RuntimeError("VAULT_TOKEN no configurado")


async def get_gateway_secrets() -> dict[str, str]:
    url = f"{VAULT_ADDR}/v1/secret/data/gateway"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                url,
                headers={"X-Vault-Token": VAULT_TOKEN},
            )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible acceder a Vault",
        ) from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="No fue posible acceder a los secretos de Vault",
        )

    try:
        return response.json()["data"]["data"]
    except (KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=500,
            detail="La respuesta de Vault no contiene los secretos esperados",
        ) from exc


async def authenticate_client(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, str]:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Bearer token requerido")

    vault_secrets = await get_gateway_secrets()
    expected_token = vault_secrets.get("client_token", "")
    received_token = credentials.credentials

    if not expected_token or not hmac.compare_digest(received_token, expected_token):
        raise HTTPException(status_code=401, detail="Token invalido")

    backend_secret = vault_secrets.get("backend_shared_secret")
    if not backend_secret:
        raise HTTPException(status_code=500, detail="Secreto del backend no configurado")

    return {
        "client_id": "student-client",
        "backend_secret": backend_secret,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "OK", "service": "API Gateway"}


@app.api_route(
    "/api/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def proxy(
    path: str,
    request: Request,
    auth: dict[str, str] = Depends(authenticate_client),
) -> Response:
    target_url = f"{BACKEND_URL}/{path}"
    gateway_headers = {
        "X-Gateway-Secret": auth["backend_secret"],
        "X-Authenticated-Client": auth["client_id"],
    }
    content_type = request.headers.get("content-type")
    if content_type:
        gateway_headers["content-type"] = content_type

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                content=await request.body(),
                headers=gateway_headers,
            )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Backend no disponible",
        ) from exc

    response_headers = {}
    if "content-type" in upstream.headers:
        response_headers["content-type"] = upstream.headers["content-type"]

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers,
    )
