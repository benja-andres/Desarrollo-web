from secrets import token_urlsafe

from fastapi import HTTPException, Request, Response, status

USERS = {
    "ana": {"user_id": "USR-001", "password": "1234", "roles": ["user"]},
    "ernesto": {
        "user_id": "USR-003",
        "password": "admin123",
        "roles": ["user", "admin"],
    },
}
SESSIONS: dict[str, dict[str, object]] = {}
COOKIE_NAME = "session_token"


def login(username: str, password: str, response: Response) -> dict[str, str]:
    user = USERS.get(username)
    if user is None or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    token = token_urlsafe(32)
    SESSIONS[token] = {
        "user_id": user["user_id"],
        "username": username,
        "roles": user["roles"],
    }
    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        max_age=900,
    )
    return {"message": "Sesión iniciada"}


def current_user(request: Request) -> dict[str, object]:
    token = request.cookies.get(COOKIE_NAME)
    user = SESSIONS.get(token or "")
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere una sesión válida",
        )
    return user


def logout(request: Request, response: Response) -> dict[str, str]:
    token = request.cookies.get(COOKIE_NAME)
    if token:
        SESSIONS.pop(token, None)
    response.delete_cookie(COOKIE_NAME, httponly=True, samesite="lax")
    return {"message": "Sesión cerrada"}
