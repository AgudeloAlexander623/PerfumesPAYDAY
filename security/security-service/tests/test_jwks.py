from collections.abc import Callable
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.security import JwtConfigurationError, JwtIssuer
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


def test_jwks_keeps_previous_key_during_overlap(
    rsa_key_pair_factory: Callable[[], tuple[str, str]],
) -> None:
    new_private, _ = rsa_key_pair_factory()
    old_private, old_public = rsa_key_pair_factory()

    issuer = JwtIssuer(
        private_key=new_private,
        previous_private_key=old_private,
        previous_public_key=old_public,
        previous_key_rotated_at=datetime.now(timezone.utc),
        issuer=ISSUER,
        audience=AUDIENCE,
    )

    keys = issuer.public_jwks
    assert len(keys) == 2
    assert keys[0]["kid"] != keys[1]["kid"]


def test_jwks_drops_previous_key_after_overlap(
    rsa_key_pair_factory: Callable[[], tuple[str, str]],
) -> None:
    new_private, _ = rsa_key_pair_factory()
    old_private, _ = rsa_key_pair_factory()

    issuer = JwtIssuer(
        private_key=new_private,
        previous_private_key=old_private,
        previous_key_rotated_at=datetime.now(timezone.utc) - timedelta(hours=25),
        issuer=ISSUER,
        audience=AUDIENCE,
    )

    assert len(issuer.public_jwks) == 1


def test_token_from_previous_key_still_verifies_after_rotation(
    rsa_key_pair_factory: Callable[[], tuple[str, str]],
) -> None:
    old_private, _ = rsa_key_pair_factory()
    new_private, _ = rsa_key_pair_factory()
    old_issuer = JwtIssuer(
        private_key=old_private,
        issuer=ISSUER,
        audience=AUDIENCE,
    )
    token = old_issuer.issue_access_token(subject=SUBJECT, roles=["customer"])

    rotated_issuer = JwtIssuer(
        private_key=new_private,
        previous_private_key=old_private,
        previous_key_rotated_at=datetime.now(timezone.utc),
        issuer=ISSUER,
        audience=AUDIENCE,
    )
    token_kid = jwt.get_unverified_header(token)["kid"]
    jwk = next(key for key in rotated_issuer.public_jwks if key["kid"] == token_kid)

    claims = jwt.decode(
        token,
        jwt.algorithms.RSAAlgorithm.from_jwk(jwk),
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER,
    )

    assert claims["typ"] == "access"


def test_rotation_rejects_a_previous_public_key_that_does_not_match(
    rsa_key_pair_factory: Callable[[], tuple[str, str]],
) -> None:
    new_private, _ = rsa_key_pair_factory()
    old_private, _ = rsa_key_pair_factory()
    _, other_public = rsa_key_pair_factory()

    with pytest.raises(JwtConfigurationError, match="no corresponde"):
        JwtIssuer(
            private_key=new_private,
            previous_private_key=old_private,
            previous_public_key=other_public,
            issuer=ISSUER,
            audience=AUDIENCE,
        )