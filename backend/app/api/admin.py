from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import require_roles
from app.core.database import get_db
from app.models.entities import AccountStatus, AuditLog, Role, User, UserScope
from app.schemas.auth import UserOut

router = APIRouter(prefix="/admin", tags=["administration"])

class ApprovalBody(BaseModel):
    organization_id: int | None = None

class ScopeBody(BaseModel):
    group_id: int | None = None
    station_id: int | None = None
    ward_codes: list[str] = []
    forest_types: list[str] = ["NATURAL_FOREST", "PLANTED_FOREST"]
    permissions: list[str] = []

@router.get("/users/pending", response_model=list[UserOut])
def pending_users(db: Session = Depends(get_db), actor: User = Depends(require_roles(Role.SADMIN, Role.ADMIN))):
    query = select(User).where(User.status == AccountStatus.PENDING_APPROVAL)
    if actor.role == Role.ADMIN:
        query = query.where(User.role.in_([Role.MODERATOR, Role.SUSER, Role.USER]))
    return list(db.scalars(query.order_by(User.created_at.desc())).all())

@router.post("/users/{user_id}/approve", response_model=UserOut)
def approve_user(user_id: int, body: ApprovalBody, db: Session = Depends(get_db), actor: User = Depends(require_roles(Role.SADMIN, Role.ADMIN))):
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(404, "Không tìm thấy tài khoản")
    if target.role == Role.ADMIN and actor.role != Role.SADMIN:
        raise HTTPException(403, "Chỉ SAdmin được phê duyệt Admin")
    if target.role == Role.SADMIN:
        raise HTTPException(403, "Không hỗ trợ phê duyệt SAdmin qua API này")
    target.status = AccountStatus.ACTIVE
    target.approved_by_id = actor.id
    target.organization_id = body.organization_id or actor.organization_id
    db.add(AuditLog(actor_id=actor.id, action="user.approve", entity_type="user", entity_id=str(target.id), payload={"role": target.role.value}))
    db.commit(); db.refresh(target)
    return target

@router.post("/users/{user_id}/scope")
def assign_scope(user_id: int, body: ScopeBody, db: Session = Depends(get_db), actor: User = Depends(require_roles(Role.SADMIN, Role.ADMIN, Role.MODERATOR))):
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(404, "Không tìm thấy tài khoản")
    scope = UserScope(user_id=user_id, group_id=body.group_id, station_id=body.station_id, ward_codes=body.ward_codes, forest_types=body.forest_types, permissions=body.permissions, granted_by_id=actor.id)
    db.add(scope)
    db.add(AuditLog(actor_id=actor.id, action="scope.assign", entity_type="user", entity_id=str(user_id), payload=body.model_dump()))
    db.commit()
    return {"ok": True, "scope_id": scope.id}
