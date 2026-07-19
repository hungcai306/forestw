from pydantic import BaseModel, EmailStr, Field
from app.models.entities import Role, AccountStatus

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8)
    requested_role: Role = Role.USER

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role
    status: AccountStatus
    organization_id: int | None
    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
