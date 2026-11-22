from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Autenticación"])


@router.get("/.well-known/jwks.json")
async def jwks(request: Request) -> JSONResponse:
    """Publica la clave pública para que los servicios Node validen tokens.

    Solo expone `kty`, `n`, `e`, `kid`, `alg` y `use`; nunca material privado.
    """
    issuer = request.app.state.jwt_issuer
    response = JSONResponse({"keys": [issuer.public_jwk]})
    response.headers["Cache-Control"] = "public, max-age=300"
    return response