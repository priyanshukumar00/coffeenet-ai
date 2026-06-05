from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum
from typing import Optional
import re


class UserRole(str, Enum):
    Admin = "Admin"
    Manager = "Manager"
    Cashier = "Cashier"
    Kitchen = "Kitchen"


def validate_password_strength(value: str):

    if not re.search(r"[A-Z]", value):
        raise ValueError(
            "Password must contain at least one uppercase letter"
        )

    if not re.search(r"[a-z]", value):
        raise ValueError(
            "Password must contain at least one lowercase letter"
        )

    if not re.search(r"\d", value):
        raise ValueError(
            "Password must contain at least one number"
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        raise ValueError(
            "Password must contain at least one special character"
        )

    return value


class UserCreate(BaseModel):

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=50
    )

    role: UserRole

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):

        if not value.strip():
            raise ValueError(
                "Full name cannot be empty"
            )

        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        return validate_password_strength(
            value
        )


class UserUpdate(BaseModel):

    full_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )

    email: Optional[EmailStr] = None

    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=50
    )

    role: Optional[UserRole] = None

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):

        if value is None:
            return value

        if not value.strip():
            raise ValueError(
                "Full name cannot be empty"
            )

        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if value is None:
            return value

        return validate_password_strength(
            value
        )

class UserLogin(BaseModel):

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=50
    )

