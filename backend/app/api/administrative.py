from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
import httpx
from app.api.deps import require_roles
from app.core.config import settings
from app.core.database import get_db
from app.models.entities import AdministrativeUnit, Role, User

router = APIRouter(prefix="/administrative", tags=["administrative"])

@router.get("/wards")
def list_wards(province_code: str = "46", db: Session = Depends(get_db)):
    rows = db.scalars(select(AdministrativeUnit).where(AdministrativeUnit.province_code == province_code, AdministrativeUnit.active.is_(True)).order_by(AdministrativeUnit.ward_name)).all()
    return [{"ward_code": r.ward_code, "ward_name": r.ward_name, "unit_type": r.unit_type, "province_code": r.province_code} for r in rows]

@router.post("/sync")
def sync_wards(province_code: str = Query(default="46"), db: Session = Depends(get_db), actor: User = Depends(require_roles(Role.SADMIN))):
    url = f"{settings.admin_api_base}/wards"
    try:
        response = httpx.get(url, params={"province_code": province_code}, timeout=20)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        raise HTTPException(502, f"Không đồng bộ được nguồn hành chính: {exc}")
    items = payload.get("data", payload) if isinstance(payload, dict) else payload
    count = 0
    for item in items:
        code = str(item.get("ward_code") or item.get("code") or "").strip()
        name = item.get("ward_name") or item.get("name")
        if not code or not name:
            continue
        row = db.scalar(select(AdministrativeUnit).where(AdministrativeUnit.ward_code == code))
        if not row:
            row = AdministrativeUnit(ward_code=code, province_code=province_code, ward_name=name, unit_type="WARD" if str(name).lower().startswith("phường") else "COMMUNE")
            db.add(row)
        row.ward_name = name
        row.source_payload = item
        row.active = True
        count += 1
    db.commit()
    return {"synced": count, "province_code": province_code}
