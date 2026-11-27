from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Autenticación"])


@router.get("/.well-known/jwks.json")
async def jwks(request: Request) -> JSONResponse:
    """Publica la clave pública para que los servicios Node validen tokens.

    Solo expone `kty`, `n`, `e`, `kid`, `alg` y `use`; nunca material privado.
    """
    issuer = request.app.state.jwt_issuer
    response = JWKSResponse(issuer)
    return response


class JWKS:
    """Clase para exponer la clave publica en formato jwks."""

    def __init__(self, issuer):
        self.issuer = issuer

        if not self.issuer.public_jwks:
            raise ValueError("El issuer no tiene clave pública en formato jwks.")

    def get_jwks(self):
        """Devuelve la clave pública en formato jwks."""
        return {"keys": self.issuer.public_jwks}



class JWKSResponse(JSONResponse):
    """Respuesta HTTP que devuelve la clave pública en formato jwks."""

    def __init__(self, issuer):
        jwks = JWKS(issuer).get_jwks()
        super().__init__(content=jwks)
        self.headers["Cache-Control"] = "public, max-age=300"

        if not jwks["keys"]:
            raise ValueError("El issuer no tiene clave pública en formato jwks.")



            1