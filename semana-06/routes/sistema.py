from fastapi import APIRouter

router = APIRouter(tags=["sistema"])


@router.get("/health")
def health():
    return {"status": "ok"}
