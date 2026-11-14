import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_private_key_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("JWT_PRIVATE_KEY", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_production_flag() -> None:
    settings = Settings(
        _env_file=None,
        environment="production",
        jwt_private_key="clave-de-prueba",
    )

    assert settings.is_production is True


def test_defaults_match_the_node_contract() -> None:
    settings = Settings(
        _env_file=None,
        jwt_private_key="clave-de-prueba",
    )

    assert settings.jwt_issuer == "perfumespayday-security"
    assert settings.jwt_audience == "perfumespayday-api"
    assert settings.jwt_access_ttl_seconds == 900
    assert settings.is_production is False