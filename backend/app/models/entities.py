import enum
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Role(str, enum.Enum):
    SADMIN = "SADMIN"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    SUSER = "SUSER"
    USER = "USER"

class AccountStatus(str, enum.Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REJECTED = "REJECTED"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.PENDING_APPROVAL)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"))
    approved_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    code: Mapped[str] = mapped_column(String(100), unique=True)
    organization_type: Mapped[str] = mapped_column(String(80), default="AGENCY")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    __table_args__ = (UniqueConstraint("organization_id", "name"),)

class Station(Base):
    __tablename__ = "stations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    code: Mapped[str] = mapped_column(String(100), unique=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    ward_codes: Mapped[list] = mapped_column(JSON, default=list)

class UserScope(Base):
    __tablename__ = "user_scopes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"))
    station_id: Mapped[int | None] = mapped_column(ForeignKey("stations.id"))
    ward_codes: Mapped[list] = mapped_column(JSON, default=list)
    forest_types: Mapped[list] = mapped_column(JSON, default=lambda: ["NATURAL_FOREST", "PLANTED_FOREST"])
    permissions: Mapped[list] = mapped_column(JSON, default=list)
    granted_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(120), index=True)
    entity_type: Mapped[str | None] = mapped_column(String(120))
    entity_id: Mapped[str | None] = mapped_column(String(120))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class AdministrativeUnit(Base):
    __tablename__ = "administrative_units"
    id: Mapped[int] = mapped_column(primary_key=True)
    province_code: Mapped[str] = mapped_column(String(20), index=True)
    ward_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    ward_name: Mapped[str] = mapped_column(String(255))
    unit_type: Mapped[str] = mapped_column(String(30))
    source_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
