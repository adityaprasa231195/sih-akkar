from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, AuditLog
from app.schemas.schemas import UserOut, UserCreate, UserRoleUpdate, AuditLogOut
from app.core.security import get_password_hash
from app.api.auth import get_current_user_payload
from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/users", response_model=UserOut)
def create_user(
    new_user: UserCreate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    payload = get_current_user_payload(authorization)
    if payload.get("role") != "Administrator":
        raise HTTPException(status_code=403, detail="Administrator role required")

    existing = db.query(User).filter(
        (User.username == new_user.username) | (User.email == new_user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = User(
        username=new_user.username,
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
        role=new_user.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/users/{user_id}/role", response_model=UserOut)
def update_user_role(
    user_id: str,
    update: UserRoleUpdate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    payload = get_current_user_payload(authorization)
    if payload.get("role") != "Administrator":
        raise HTTPException(status_code=403, detail="Administrator role required")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = update.role
    db.commit()
    db.refresh(user)
    return user

@router.get("/audit-logs", response_model=List[AuditLogOut])
def get_audit_logs(
    action: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog).order_by(AuditLog.timestamp.desc())
    if action and action != "All":
        query = query.filter(AuditLog.action == action)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    return query.limit(100).all()

@router.get("/settings")
def get_system_settings():
    return {
        "manual_baseline_hours_per_ha": settings.MANUAL_BASELINE_HOURS_PER_HA,
        "high_confidence_threshold": 0.85,
        "medium_confidence_threshold": 0.50,
        "high_dispute_risk_threshold": 60,
        "default_state_code": settings.DEFAULT_STATE,
        "default_district_code": settings.DEFAULT_DISTRICT,
        "default_taluka_code": settings.DEFAULT_TALUKA,
        "default_village_code": settings.DEFAULT_VILLAGE
    }
