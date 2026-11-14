import base64
import hashlib
import json
from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from typing import Literal
from uuid import UUID, uuid4

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.config import Settings

Role = Literal["customer", "admin"]
ALLOWED_ROLES: frozenset[str] = frozenset({"customer", "admin"})


class JwtConfigurationError(ValueError):
    """La configuración de claves o claims no es utilizable."""


def normalize_pem(value: str) -> str:
    """Acepta PEM, PEM con `\\n` escapados o el PEM codificado en base64."""
    normalized = value.replace("\\n", "\n").strip()

    if "-----BEGIN" in normalized:
        return normalized

    try:
        decoded = base64.b64decode(normalized).decode("utf-8").strip()
    except (ValueError, UnicodeDecodeError) as exc:
        raise JwtConfigurationError("La clave JWT no es un PEM válido.") from exc

    if "-----BEGIN" not in decoded:
        raise JwtConfigurationError("La clave JWT no es un PEM válido.")

    return decoded


def load_private_key(value: str) -> rsa.RSAPrivateKey:
    try:
        key = serialization.load_pem_private_key(
            normalize_pem(value).encode(),
            password=None,
        )
    except (TypeError, ValueError) as exc:
        raise JwtConfigurationError(
            "No se pudo cargar la clave privada JWT."
        ) from exc

    if not isinstance(key, rsa.RSAPrivateKey):
        raise JwtConfigurationError("La clave privada JWT debe ser RSA.")

    return key


def load_public_key(value: str) -> rsa.RSAPublicKey:
    try:
        key = serialization.load_pem_public_key(normalize_pem(value).encode())
    except (TypeError, ValueError) as exc:
        raise JwtConfigurationError(
            "No se pudo cargar la clave pública JWT."
        ) from exc

    if not isinstance(key, rsa.RSAPublicKey):
        raise JwtConfigurationError("La clave pública JWT debe ser RSA.")

    return key


def _base64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _int_to_base64url(value: int) -> str:
    length = (value.bit_length() + 7) // 8
    return _base64url(value.to_bytes(length, "big"))


def _thumbprint(jwk: dict[str, str]) -> str:
    """Huella JWK (RFC 7638) usada como `kid` estable."""
    canonical = json.dumps(
        {"e": jwk["e"], "kty": jwk["kty"], "n": jwk["n"]},
        separators=(",", ":"),
        sort_keys=True,
    )
    return _base64url(hashlib.sha256(canonical.encode("ascii")).digest())


class JwtIssuer:
    """Firma access tokens RS256 y publica la clave pública en formato JWK."""

    def __init__(
        self,
        *,
        private_key: str,
        issuer: str,
        audience: str,
        public_key: str | None = None,
        ttl_seconds: int = 900,
        key_id: str | None = None,
    ) -> None:
        self._private_key = load_private_key(private_key)
        derived_public_key = self._private_key.public_key()

        if public_key is not None:
            provided_public_key = load_public_key(public_key)
            if (
                provided_public_key.public_numbers()
                != derived_public_key.public_numbers()
            ):
                raise JwtConfigurationError(
                    "JWT_PUBLIC_KEY no corresponde a JWT_PRIVATE_KEY."
                )

        self._public_key = derived_public_key
        self.issuer = issuer
        self.audience = audience
        self.ttl_seconds = ttl_seconds

        numbers = derived_public_key.public_numbers()
        jwk = {
            "kty": "RSA",
            "n": _int_to_base64url(numbers.n),
            "e": _int_to_base64url(numbers.e),
        }
        self.key_id = key_id or _thumbprint(jwk)
        jwk.update({"kid": self.key_id, "alg": "RS256", "use": "sig"})
        self._jwk = jwk

    @classmethod
    def from_settings(cls, settings: Settings) -> "JwtIssuer":
        return cls(
            private_key=settings.jwt_private_key,
            public_key=settings.jwt_public_key,
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            ttl_seconds=settings.jwt_access_ttl_seconds,
            key_id=settings.jwt_key_id,
        )

    @property
    def public_jwk(self) -> dict[str, str]:
        """Copia del JWK público; nunca incluye material privado."""
        return dict(self._jwk)

    @property
    def public_key_pem(self) -> str:
        return self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("ascii")

    def issue_access_token(
        self,
        *,
        subject: str | UUID,
        roles: Sequence[Role],
        issued_at: datetime | None = None,
        token_id: str | None = None,
    ) -> str:
        """Emite un access token con los claims que valida el backend Node."""
        subject_value = str(subject)

        try:
            UUID(subject_value)
        except ValueError as exc:
            raise ValueError("El claim `sub` debe ser un UUID.") from exc

        if not roles:
            raise ValueError("El token debe incluir al menos un rol.")

        invalid_roles = set(roles) - ALLOWED_ROLES
        if invalid_roles:
            raise ValueError(
                f"Roles no permitidos: {', '.join(sorted(invalid_roles))}."
            )

        now = issued_at or datetime.now(timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)

        payload = {
            "sub": subject_value,
            "iss": self.issuer,
            "aud": self.audience,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=self.ttl_seconds)).timestamp()),
            "jti": token_id or str(uuid4()),
            "roles": list(dict.fromkeys(roles)),
            "typ": "access",
        }

        return jwt.encode(
            payload,
            self._private_key,
            algorithm="RS256",
            headers={"kid": self.key_id, "typ": "JWT"},
        )