from fastapi import APIRouter

router = APIRouter(tags=["Sistema"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Estado mínimo que consultan Docker Compose y el gateway."""
    return {"status": "ok", "service": "security-service"}