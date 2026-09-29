from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Parcel, TopologyError, ParcelVersion, AuditLog
from app.schemas.schemas import ParcelOut, ParcelUpdate, ParcelApproveRequest, ParcelRejectRequest
from app.services.ulpin_service import generate_ulpin
from app.api.auth import get_current_user_payload

router = APIRouter(prefix="/parcels", tags=["parcels"])

@router.get("", response_model=List[ParcelOut])
def list_parcels(
    min_confidence: Optional[float] = Query(None),
    max_confidence: Optional[float] = Query(None),
    status: Optional[str] = Query(None),
    land_use: Optional[str] = Query(None),
    gt_status: Optional[str] = Query(None),
    coverage_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Parcel)
    if min_confidence is not None:
        query = query.filter(Parcel.confidence_score >= min_confidence)
    if max_confidence is not None:
        query = query.filter(Parcel.confidence_score <= max_confidence)
    if status is not None and status != "All":
        query = query.filter(Parcel.validation_status == status)
    if land_use is not None and land_use != "All":
        query = query.filter(Parcel.land_use_class == land_use)
    if gt_status is not None and gt_status != "All":
        query = query.filter(Parcel.gt_status == gt_status)
    if coverage_type is not None and coverage_type != "All":
        query = query.filter(Parcel.coverage_type == coverage_type)
    return query.all()

@router.get("/{parcel_id}", response_model=ParcelOut)
def get_parcel(parcel_id: str, db: Session = Depends(get_db)):
    parcel = db.query(Parcel).filter(Parcel.parcel_id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return parcel

@router.put("/{parcel_id}", response_model=ParcelOut)
def update_parcel(
    parcel_id: str,
    update_data: ParcelUpdate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    payload = get_current_user_payload(authorization)
    if payload.get("role") not in ["Editor", "Reviewer", "Administrator"]:
        raise HTTPException(status_code=403, detail="Editor role required to modify parcel")

    parcel = db.query(Parcel).filter(Parcel.parcel_id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    if update_data.geometry is not None:
        parcel.geometry = update_data.geometry
    if update_data.land_use_class is not None:
        parcel.land_use_class = update_data.land_use_class
    if update_data.coverage_type is not None:
        parcel.coverage_type = update_data.coverage_type
    parcel.updated_at = datetime.utcnow()

    # Track version history
    latest_version = db.query(ParcelVersion).filter(
        ParcelVersion.parcel_id == parcel_id
    ).order_by(ParcelVersion.version_number.desc()).first()
    next_ver = (latest_version.version_number + 1) if latest_version else 1

    new_ver = ParcelVersion(
        parcel_id=parcel_id,
        version_number=next_ver,
        geometry_snapshot=parcel.geometry,
        attributes_snapshot={
            "land_use": parcel.land_use_class,
            "coverage_type": parcel.coverage_type,
            "area_sqm": parcel.area_sqm
        },
        changed_by=payload.get("sub", "editor"),
        change_reason=update_data.change_reason or "Manual boundary adjustment"
    )
    db.add(new_ver)

    # Audit log
    audit = AuditLog(
        user_id=payload.get("sub", "editor"),
        user_name=payload.get("sub", "editor"),
        action="Edit",
        feature_id=parcel_id,
        details={"version": next_ver, "reason": update_data.change_reason}
    )
    db.add(audit)
    db.commit()
    db.refresh(parcel)
    return parcel

@router.post("/{parcel_id}/approve", response_model=ParcelOut)
def approve_parcel(
    parcel_id: str,
    req: ParcelApproveRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    payload = get_current_user_payload(authorization)
    if payload.get("role") not in ["Reviewer", "Administrator"]:
        raise HTTPException(status_code=403, detail="Reviewer or Administrator role required to approve parcels")

    parcel = db.query(Parcel).filter(Parcel.parcel_id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    # Gate 1: Check for open Critical topology errors
    critical_errors = db.query(TopologyError).filter(
        TopologyError.feature_id == parcel_id,
        TopologyError.severity == "Critical",
        TopologyError.status == "Open"
    ).all()
    if critical_errors:
        err_types = ", ".join({e.error_type for e in critical_errors})
        raise HTTPException(
            status_code=400,
            detail=f"Approval blocked: parcel has unresolved Critical topology errors ({err_types})."
        )

    # Gate 2: High Dispute Risk check (score >= 60)
    if parcel.dispute_risk_score >= 60:
        if not req.override_high_risk or not req.override_reason:
            raise HTTPException(
                status_code=400,
                detail=f"Approval blocked: High dispute risk score ({parcel.dispute_risk_score}/100). Reviewer override with documented justification required."
            )

    # Generate ULPIN if not already assigned
    if not parcel.ulpin:
        parcel.ulpin = generate_ulpin(db, parcel)

    parcel.validation_status = "Approved"
    parcel.approved_by = payload.get("sub", "reviewer")
    parcel.updated_at = datetime.utcnow()

    # Log in audit trail
    audit = AuditLog(
        user_id=payload.get("sub", "reviewer"),
        user_name=payload.get("sub", "reviewer"),
        action="Approve",
        feature_id=parcel_id,
        details={
            "ulpin_assigned": parcel.ulpin,
            "dispute_score": parcel.dispute_risk_score,
            "override_applied": bool(req.override_high_risk),
            "override_reason": req.override_reason
        }
    )
    db.add(audit)
    db.commit()
    db.refresh(parcel)
    return parcel

@router.post("/{parcel_id}/reject", response_model=ParcelOut)
def reject_parcel(
    parcel_id: str,
    req: ParcelRejectRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    payload = get_current_user_payload(authorization)
    parcel = db.query(Parcel).filter(Parcel.parcel_id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    parcel.validation_status = "Rejected"
    parcel.updated_at = datetime.utcnow()

    audit = AuditLog(
        user_id=payload.get("sub", "reviewer"),
        user_name=payload.get("sub", "reviewer"),
        action="Reject",
        feature_id=parcel_id,
        details={"rejection_reason": req.rejection_reason}
    )
    db.add(audit)
    db.commit()
    db.refresh(parcel)
    return parcel

@router.get("/{parcel_id}/history")
def get_parcel_history(parcel_id: str, db: Session = Depends(get_db)):
    versions = db.query(ParcelVersion).filter(
        ParcelVersion.parcel_id == parcel_id
    ).order_by(ParcelVersion.version_number.asc()).all()
    return versions

@router.post("/{parcel_id}/rollback/{version_id}", response_model=ParcelOut)
def rollback_parcel(
    parcel_id: str,
    version_id: str,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    payload = get_current_user_payload(authorization)
    if payload.get("role") not in ["Reviewer", "Administrator"]:
        raise HTTPException(status_code=403, detail="Reviewer role required for version rollback")

    parcel = db.query(Parcel).filter(Parcel.parcel_id == parcel_id).first()
    target_ver = db.query(ParcelVersion).filter(
        ParcelVersion.parcel_version_id == version_id,
        ParcelVersion.parcel_id == parcel_id
    ).first()
    if not parcel or not target_ver:
        raise HTTPException(status_code=404, detail="Target version or parcel not found")

    parcel.geometry = target_ver.geometry_snapshot
    if target_ver.attributes_snapshot.get("land_use"):
        parcel.land_use_class = target_ver.attributes_snapshot["land_use"]
    parcel.updated_at = datetime.utcnow()

    # Create new version representing the rollback state
    latest = db.query(ParcelVersion).filter(
        ParcelVersion.parcel_id == parcel_id
    ).order_by(ParcelVersion.version_number.desc()).first()
    next_num = latest.version_number + 1

    rolled_ver = ParcelVersion(
        parcel_id=parcel_id,
        version_number=next_num,
        geometry_snapshot=parcel.geometry,
        attributes_snapshot=target_ver.attributes_snapshot,
        changed_by=payload.get("sub", "reviewer"),
        change_reason=f"Rollback to snapshot version {target_ver.version_number}"
    )
    db.add(rolled_ver)

    audit = AuditLog(
        user_id=payload.get("sub", "reviewer"),
        user_name=payload.get("sub", "reviewer"),
        action="Rollback",
        feature_id=parcel_id,
        details={"rolled_back_to_version": target_ver.version_number, "new_version": next_num}
    )
    db.add(audit)
    db.commit()
    db.refresh(parcel)
    return parcel
