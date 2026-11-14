import base64
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.core.security import (
    JwtConfigurationError,
    JwtIssuer,
    normalize_pem,
)
from tests.constants import AUDIENCE, ISSUER, SUBJECT


def decode(token: str, public_key_pem: str) -> dict:
    return jwt.decode(
        token,
        public_key_pem,
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER,
    )


def test_issue_access_token_has_the_expected_claims(client: TestClient) -> None:
    issuer: JwtIssuer = client.app.state.jwt_issuer
    issued_at = datetime.now(timezone.utc).replace(microsecond=0)

    token = issuer.issue_access_token(
        subject=SUBJECT,
        roles=["customer"],
        issued_at=issued_at,
        token_id="22222222-2222-4222-8222-222222222222",
    )

    header = jwt.get_unverified_header(token)
    claims = decode(token, issuer.public_key_pem)

    assert header == {"alg": "RS256", "kid": issuer.key_id, "typ": "JWT"}
    assert claims["sub"] == SUBJECT
    assert claims["iss"] == ISSUER
    assert claims["aud"] == AUDIENCE
    assert claims["roles"] == ["customer"]
    assert claims["jti"] == "22222222-2222-4222-8222-222222222222"
    assert claims["typ"] == "access"
    assert claims["iat"] == int(issued_at.timestamp())
    assert claims["exp"] == int((issued_at + timedelta(seconds=900)).timestamp())


def test_each_token_gets_a_unique_jti(client: TestClient) -> None:
    issuer: JwtIssuer = client.app.state.jwt_issuer

    first = decode(
        issuer.issue_access_token(subject=SUBJECT, roles=["admin"]),
        issuer.public_key_pem,
    )
    second = decode(
        issuer.issue_access_token(subject=SUBJECT, roles=["admin"]),
        issuer.public_key_pem,
    )

    assert first["jti"] != second["jti"]


def test_roles_are_deduplicated(client: TestClient) -> None:
    issuer: JwtIssuer = client.app.state.jwt_issuer

    token = issuer.issue_access_token(
        subject=SUBJECT,
        roles=["customer", "customer"],
    )

    assert decode(token, issuer.public_key_pem)["roles"] == ["customer"]


@pytest.mark.parametrize("subject", ["", "no-es-uuid", "123"])
def test_rejects_invalid_subject(client: TestClient, subject: str) -> None:
    issuer: JwtIssuer = client.app.state.jwt_issuer

    with pytest.raises(ValueError, match="UUID"):
        issuer.issue_access_token(subject=subject, roles=["customer"])


def test_rejects_empty_roles(client: TestClient) -> None:
    issuer: JwtIssuer = client.app.state.jwt_issuer

    with pytest.raises(ValueError, match="al menos un rol"):
        issuer.issue_access_token(subject=SUBJECT, roles=[])


def test_rejects_unknown_roles(client: TestClient) -> None:
    issuer: JwtIssuer = client.app.state.jwt_issuer

    with pytest.raises(ValueError, match="Roles no permitidos"):
        issuer.issue_access_token(subject=SUBJECT, roles=["superadmin"])  # type: ignore[list-item]


def test_rejects_a_public_key_that_does_not_match(
    rsa_key_pair: tuple[str, str],
) -> None:
    private_pem, _ = rsa_key_pair
    other_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    other_public_pem = other_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")

    with pytest.raises(JwtConfigurationError, match="no corresponde"):
        JwtIssuer(
            private_key=private_pem,
            public_key=other_public_pem,
            issuer=ISSUER,
            audience=AUDIENCE,
        )


def test_normalize_pem_accepts_base64(rsa_key_pair: tuple[str, str]) -> None:
    private_pem, _ = rsa_key_pair
    encoded = base64.b64encode(private_pem.encode("ascii")).decode("ascii")

    assert normalize_pem(encoded).startswith("-----BEGIN PRIVATE KEY-----")


def test_normalize_pem_accepts_escaped_newlines(rsa_key_pair: tuple[str, str]) -> None:
    private_pem, _ = rsa_key_pair

    assert normalize_pem(private_pem.replace("\n", "\\n")).strip() == private_pem.strip()


def test_normalize_pem_rejects_invalid_values() -> None:
    with pytest.raises(JwtConfigurationError, match="PEM válido"):
        normalize_pem("esto-no-es-una-clave")