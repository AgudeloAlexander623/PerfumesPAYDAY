from enum import StrEnum


class UserRole(StrEnum):
    """Roles permitidos tanto en la tabla users como en el access token."""

    CUSTOMER = "customer"
    ADMIN = "admin"


class UserStatus(StrEnum):
    """Estados posibles de una cuenta de usuario."""

    ACTIVE = "active"
    DISABLED = "disabled"
