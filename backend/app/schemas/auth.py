import re
from pydantic import BaseModel, Field, field_validator
from app.models.entities import Role, AccountStatus

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.]+$")

class LoginRequest(BaseModel):
    admin_username: str = Field(min_length=3, max_length=80)
    password: str

    @field_validator("admin_username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        value = value.strip().lower()
        if not USERNAME_PATTERN.fullmatch(value):
            raise ValueError("Tên đăng nhập chỉ được gồm chữ, số, dấu chấm và gạch dưới")
        return value

class RegisterRequest(BaseModel):
    admin_username: str = Field(min_length=3, max_length=80)
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8)
    requested_role: Role = Role.USER
    email: str | None = None

    @field_validator("admin_username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        value = value.strip().lower()
        if not USERNAME_PATTERN.fullmatch(value):
            raise ValueError("Tên đăng nhập chỉ được gồm chữ, số, dấu chấm và gạch dưới")
        return value

class UserOut(BaseModel):
    id: int
    admin_username: str
    email: str | None
    full_name: str
    role: Role
    status: AccountStatus
    organization_id: int | None
    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
