import jwt
from fastapi.testclient import TestClient

from tests.constants import AUDIENCE, ISSUER, SUBJECT


def test_jwks_exposes_only_the_public_key(client: TestClient) -> None:
    response = client.get("/.well-known/jwks.json")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "public, max-age=300"

    keys = response.json()["keys"]
    assert len(keys) == 1

    jwk = keys[0]
    assert jwk["kty"] == "RSA"
    assert jwk["alg"] == "RS256"
    assert jwk["use"] == "sig"
    assert jwk["kid"]
    assert set(jwk) == {"kty", "n", "e", "kid", "alg", "use"}


def test_jwks_key_verifies_an_issued_token(client: TestClient) -> None:
    issuer = client.app.state.jwt_issuer
    token = issuer.issue_access_token(subject=SUBJECT, roles=["customer"])

    jwk = client.get("/.well-known/jwks.json").json()["keys"][0]
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)

    claims = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER,
    )

    assert claims["sub"] == SUBJECT
    assert claims["roles"] == ["customer"]