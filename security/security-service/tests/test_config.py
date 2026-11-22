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

    assert settings.jwt_issuer == "perfumesgold-security"
    assert settings.jwt_audience == "perfumesgold-api"
    assert settings.jwt_access_ttl_seconds == 900
    assert settings.is_production is False


def test_session_defaults_match_adr_0009() -> None:
    settings = Settings(
        _env_file=None,
        jwt_private_key="clave-de-prueba",
    )

    assert settings.refresh_ttl_days == 7
    assert settings.session_absolute_ttl_days == 30
    assert settings.login_max_failed_attempts == 5
    assert settings.login_lockout_minutes == 15
    assert "security_db" in settings.database_url


def test_absolute_ttl_cannot_be_shorter_than_refresh_ttl() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            jwt_private_key="clave-de-prueba",
            refresh_ttl_days=30,
            session_absolute_ttl_days=7,
        )