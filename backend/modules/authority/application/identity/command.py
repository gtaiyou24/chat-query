from __future__ import annotations

from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ProvisionTenantCommand:
    @dataclass(init=True, unsafe_hash=True, frozen=True)
    class Tenant:
        name: str

    @dataclass(init=True, unsafe_hash=True, frozen=True)
    class User:
        username: str
        email_address: str
        plain_password: str

    tenant: Tenant
    user: User


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateUserCommand:
    email_address: str
    password: str | None


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RefreshCommand:
    refresh_token: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RevokeCommand:
    token: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ForgotPasswordCommand:
    email_address: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ResetPasswordCommand:
    reset_token: str
    password: str
