#!/usr/bin/env python3
"""Genera un par RS256 de desarrollo y lo imprime en base64."""

import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def to_base64(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def main() -> None:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    print("# Par de claves RS256 para desarrollo. No lo uses en producción.")
    print("# Pega JWT_PRIVATE_KEY en security/security-service/.env.")
    print("# Los servicios Node pueden usar JWT_PUBLIC_KEY o el JWKS del servicio.")
    print(f"JWT_PRIVATE_KEY={to_base64(private_pem)}")
    print(f"JWT_PUBLIC_KEY={to_base64(public_pem)}")


if __name__ == "__main__":
    main()