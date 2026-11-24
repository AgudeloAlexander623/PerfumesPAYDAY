import json
import subprocess
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Callable
from uuid import uuid4

import jwt
import pytest

from app.core.security import JwtIssuer

ISSUER = "perfumesgold-security"
AUDIENCE = "perfumesgold-api"
ACCESS_TTL_SECONDS = 900
JWKS_PATH = "/.well-known/jwks.json"
BACKEND_DIR = Path(__file__).resolve().parents[3] / "Backend"
TSX = BACKEND_DIR / "node_modules/.bin/tsx"
VERIFIER = BACKEND_DIR / "tests/contract/verify_jwt.ts"

VerifyResult = tuple[int, dict[str, object]]


class JwksHandler(BaseHTTPRequestHandler):
    """Sirve el JWKS del emisor Python sin exponer material privado."""

    payload = b""

    def do_GET(self) -> None:  # noqa: N802
        if self.path != JWKS_PATH:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "public, max-age=300")
        self.send_header("Content-Length", str(len(self.payload)))
        self.end_headers()
        self.wfile.write(self.payload)

    def log_message(self, _format: str, *_args: object) -> None:
        """Evita que el servidor ensucie la salida de pytest."""


def verify_with_node(token: str, jwks_url: str) -> VerifyResult:
    """Ejecuta el verificador Node y devuelve su código de salida y su JSON."""
    if not TSX.is_file() or not VERIFIER.is_file():
        pytest.skip("El contrato Node requiere `npm install` en Backend.")

    result = subprocess.run(
        [str(TSX), str(VERIFIER), token, jwks_url, ISSUER, AUDIENCE],
        cwd=BACKEND_DIR,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    try:
        payload: dict[str, object] = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(
            "El verificador Node no devolvió JSON. "
            f"stdout={result.stdout!r} stderr={result.stderr!r}; {exc}"
        )

    return result.returncode, payload


def refresh_token(private_pem: str, valid_token: str) -> str:
    """Deriva un refresh del access real; solo cambia el claim `typ`."""
    payload = jwt.decode(valid_token, options={"verify_signature": False})
    payload["typ"] = "refresh"
    kid = jwt.get_unverified_header(valid_token)["kid"]

    return jwt.encode(
        payload,
        private_pem,
        algorithm="RS256",
        headers={"kid": kid},
    )


@pytest.fixture
def identity() -> tuple[str, str]:
    """Identificadores únicos por prueba, sin valores mágicos compartidos."""
    return str(uuid4()), str(uuid4())


@pytest.fixture
def issuer(rsa_key_pair: tuple[str, str]) -> JwtIssuer:
    """Emisor Python efímero con el mismo contrato que consumen los Node."""
    private_pem, public_pem = rsa_key_pair
    return JwtIssuer(
        private_key=private_pem,
        public_key=public_pem,
        issuer=ISSUER,
        audience=AUDIENCE,
        ttl_seconds=ACCESS_TTL_SECONDS,
    )


@pytest.fixture
def jwks_server(
    issuer: JwtIssuer,
) -> Iterator[tuple[str, Callable[[], None]]]:
    """Publica el JWKS en localhost y permite simular su caída."""
    payload = json.dumps({"keys": issuer.public_jwks}).encode()
    handler = type("ConfiguredJwksHandler", (JwksHandler,), {"payload": payload})
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[0], server.server_address[1]
    stopped = False

    def stop() -> None:
        nonlocal stopped
        if stopped:
            return
        stopped = True
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    try:
        yield f"http://{host}:{port}{JWKS_PATH}", stop
    finally:
        stop()


def test_python_access_token_is_accepted_by_node(
    issuer: JwtIssuer,
    identity: tuple[str, str],
    jwks_server: tuple[str, Callable[[], None]],
) -> None:
    url, _ = jwks_server
    subject, token_id = identity
    issued_at = datetime.now(timezone.utc).replace(microsecond=0)
    token = issuer.issue_access_token(
        subject=subject,
        roles=["customer"],
        issued_at=issued_at,
        token_id=token_id,
    )

    code, payload = verify_with_node(token, url)

    assert code == 0
    assert payload == {
        "ok": True,
        "claims": {
            "sub": subject,
            "iss": ISSUER,
            "aud": AUDIENCE,
            "iat": int(issued_at.timestamp()),
            "exp": int(
                (issued_at + timedelta(seconds=ACCESS_TTL_SECONDS)).timestamp()
            ),
            "jti": token_id,
            "roles": ["customer"],
            "typ": "access",
        },
    }


def test_node_rejects_a_refresh_typ(
    issuer: JwtIssuer,
    identity: tuple[str, str],
    rsa_key_pair: tuple[str, str],
    jwks_server: tuple[str, Callable[[], None]],
) -> None:
    url, _ = jwks_server
    subject, token_id = identity
    valid = issuer.issue_access_token(
        subject=subject,
        roles=["customer"],
        token_id=token_id,
    )
    token = refresh_token(rsa_key_pair[0], valid)

    code, payload = verify_with_node(token, url)

    assert code == 2
    assert payload == {
        "ok": False,
        "error": {"code": "UNAUTHORIZED", "statusCode": 401},
    }


def test_node_rejects_a_tampered_signature(
    issuer: JwtIssuer,
    identity: tuple[str, str],
    jwks_server: tuple[str, Callable[[], None]],
) -> None:
    url, _ = jwks_server
    subject, token_id = identity
    token = issuer.issue_access_token(
        subject=subject,
        roles=["customer"],
        token_id=token_id,
    )
    header, claims, signature = token.split(".")
    replacement = "A" if signature[0] != "A" else "B"
    tampered = f"{header}.{claims}.{replacement}{signature[1:]}"

    code, payload = verify_with_node(tampered, url)

    assert code == 2
    assert payload == {
        "ok": False,
        "error": {"code": "UNAUTHORIZED", "statusCode": 401},
    }


def test_node_maps_jwks_outage_to_503(
    issuer: JwtIssuer,
    identity: tuple[str, str],
    jwks_server: tuple[str, Callable[[], None]],
) -> None:
    url, stop = jwks_server
    subject, token_id = identity
    token = issuer.issue_access_token(
        subject=subject,
        roles=["customer"],
        token_id=token_id,
    )
    stop()

    code, payload = verify_with_node(token, url)

    assert code == 2
    assert payload == {
        "ok": False,
        "error": {"code": "UPSTREAM_UNAVAILABLE", "statusCode": 503},
    }
