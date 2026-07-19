from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.entities import AccountStatus, AuditLog, Role, User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    username = data.admin_username.strip().lower()
    if db.scalar(select(User).where(User.admin_username == username)):
        raise HTTPException(409, "Tên đăng nhập đã tồn tại")
    if data.requested_role == Role.SADMIN:
        raise HTTPException(403, "Không thể tự đăng ký SAdmin")
    email = data.email.strip().lower() if data.email else None
    user = User(
        admin_username=username,
        email=email,
        full_name=data.full_name,
        password_hash=hash_password(data.password),
        role=data.requested_role,
        status=AccountStatus.PENDING_APPROVAL,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    username = data.admin_username.strip().lower()
    user = db.scalar(select(User).where(User.admin_username == username))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Tên đăng nhập hoặc mật khẩu không đúng")
    if user.status != AccountStatus.ACTIVE:
        raise HTTPException(403, f"Tài khoản đang ở trạng thái {user.status.value}")
    db.add(AuditLog(actor_id=user.id, action="auth.login", entity_type="user", entity_id=str(user.id)))
    db.commit()
    return TokenResponse(access_token=create_access_token(str(user.id), user.role.value), user=user)

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user
