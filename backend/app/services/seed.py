from sqlalchemy import select
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.entities import AccountStatus, Organization, Role, User

def seed() -> None:
    db = SessionLocal()
    try:
        org = db.scalar(select(Organization).where(Organization.code == "HUE"))
        if not org:
            org = Organization(name="Thành phố Huế", code="HUE", organization_type="CENTRAL_MUNICIPALITY")
            db.add(org)
            db.flush()
        username = settings.sadmin_username.strip().lower()
        user = db.scalar(select(User).where(User.admin_username == username))
        if not user:
            user = User(
                admin_username=username,
                email=None,
                full_name="Tổng Quản trị viên",
                password_hash=hash_password(settings.sadmin_password),
                role=Role.SADMIN,
                status=AccountStatus.ACTIVE,
                organization_id=org.id,
            )
            db.add(user)
        db.commit()
    finally:
        db.close()
