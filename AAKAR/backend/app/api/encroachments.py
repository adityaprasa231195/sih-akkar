from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import EncroachmentFlag, AuditLog
from app.schemas.schemas import EncroachmentFlagOut, EncroachmentResolveRequest
from app.api.auth import get_current_user_payload

router = APIRouter(prefix="/encroachments", tags=["encroachments"])

@router.get("", response_model=List[EncroachmentFlagOut])
def list_encroachments(
    status: Optional[str] = Query(None),
    flag_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(EncroachmentFlag)
    if status and status != "All":
        query = query.filter(EncroachmentFlag.status == status)
    if flag_type and flag_type != "All":
        query = query.filter(EncroachmentFlag.flag_type == flag_type)
    return query.all()

@router.put("/{flag_id}/resolve", response_model=EncroachmentFlagOut)
def resolve_encroachment(
    flag_id: str,
    req: EncroachmentResolveRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    payload = get_current_user_payload(authorization)
    flag = db.query(EncroachmentFlag).filter(EncroachmentFlag.encroachment_flag_id == flag_id).first()
    if not flag:
        raise HTTPException(status_code=404, detail="Encroachment flag not found")

    flag.status = "Dismissed" if req.action == "dismiss" else "Resolved"
    flag.resolved_by = payload.get("sub", "reviewer")
    flag.resolved_at = datetime.utcnow()
    flag.notes = req.notes or f"Action {req.action} applied by {flag.resolved_by}"

    audit = AuditLog(
        user_id=payload.get("sub", "reviewer"),
        user_name=payload.get("sub", "reviewer"),
        action="EncroachmentResolved",
        feature_id=flag.parcel_id,
        details={"flag_id": flag_id, "action": req.action, "notes": flag.notes}
    )
    db.add(audit)
    db.commit()
    db.refresh(flag)
    return flag
