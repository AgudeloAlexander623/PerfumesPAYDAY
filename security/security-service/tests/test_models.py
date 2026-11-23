from app.db.models import User, UserSession


def test_users_table_contract() -> None:
    """La tabla users debe reflejar el modelo de ADR-0009."""
    table = User.__table__

    assert table.name == "users"
    assert set(table.columns.keys()) >= {
        "id",
        "name",
        "email",
        "password_hash",
        "role",
        "status",
        "created_at",
        "updated_at",
        "last_login_at",
    }

    constraint_names = {constraint.name for constraint in table.constraints}
    assert "uq_users_email" in constraint_names
    assert {"ck_users_role", "ck_users_status"} <= constraint_names


def test_sessions_table_contract() -> None:
    """La tabla sessions debe permitir rotación y detección de reutilización."""
    table = UserSession.__table__

    assert table.name == "sessions"
    assert set(table.columns.keys()) >= {
        "id",
        "user_id",
        "family_id",
        "refresh_token_hash",
        "expires_at",
        "absolute_expires_at",
        "revoked_at",
        "replaced_by",
        "user_agent",
        "ip",
        "created_at",
        "updated_at",
        "last_used_at",
    }

    index_names = {index.name for index in table.indexes}
    assert {"ix_sessions_user_id", "ix_sessions_family_id", "ix_sessions_expires_at"} <= index_names

    constraint_names = {constraint.name for constraint in table.constraints}
    assert "uq_sessions_refresh_token_hash" in constraint_names

    foreign_keys = {foreign_key.target_fullname for foreign_key in table.foreign_keys}
    assert {"users.id", "sessions.id"} <= foreign_keys
