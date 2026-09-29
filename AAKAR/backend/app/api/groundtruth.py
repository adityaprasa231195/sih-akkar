from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Parcel, AuditLog
from app.schemas.schemas import ParcelOut, GTStatusUpdate

router = APIRouter(prefix="/groundtruth", tags=["groundtruth"])

@router.get("/priority-list")
def get_gt_priority_list(db: Session = Depends(get_db)):
    """
    Returns parcels prioritized for field ground-truthing (lowest confidence first).
    Also includes computed GT efficiency metrics.
    """
    parcels = db.query(Parcel).order_by(Parcel.confidence_score.asc()).all()
    
    total = len(parcels)
    low_conf_count = sum(1 for p in parcels if p.confidence_score < 0.50)
    med_conf_count = sum(1 for p in parcels if 0.50 <= p.confidence_score < 0.85)
    
    # Ground Truthing Effort Reduction: targeted field visits instead of 100% manual surveying
    # Only Low & Medium confidence require field checks
    targeted_visits = low_conf_count + int(med_conf_count * 0.4)
    effort_reduced_pct = round(((total - targeted_visits) / max(1, total)) * 100, 1)
    visits_saved = max(0, total - targeted_visits)

    return {
        "efficiency_metrics": {
            "gt_effort_reduced_pct": effort_reduced_pct,
            "estimated_visits_saved": visits_saved,
            "total_parcels": total,
            "priority_field_queue_count": low_conf_count
        },
        "parcels": [
            {
                "parcel_id": p.parcel_id,
                "ulpin": p.ulpin,
                "confidence_score": p.confidence_score,
                "gt_status": p.gt_status,
                "land_use_class": p.land_use_class,
                "area_sqm": p.area_sqm,
                "centroid_lat": p.centroid_lat,
                "centroid_lon": p.centroid_lon,
                "dispute_risk_score": p.dispute_risk_score
            }
            for p in parcels
        ]
    }

@router.post("/upload")
async def upload_gt_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    # Mocking geospatial vector matching
    matched = db.query(Parcel).filter(Parcel.confidence_score < 0.85).all()
    for p in matched:
        p.gt_status = "Completed"
        p.confidence_score = min(0.98, p.confidence_score + 0.18)
    
    audit = AuditLog(
        user_id="editor",
        user_name="editor",
        action="GTUpload",
        feature_id=file.filename,
        details={"file_name": file.filename, "file_size_bytes": len(content), "matched_parcels": len(matched)}
    )
    db.add(audit)
    db.commit()

    return {
        "status": "Success",
        "file_name": file.filename,
        "matched_parcels_count": len(matched),
        "unmatched_count": 0,
        "confidence_boost_applied": True
    }

@router.put("/{parcel_id}/status")
def update_gt_status(parcel_id: str, update: GTStatusUpdate, db: Session = Depends(get_db)):
    parcel = db.query(Parcel).filter(Parcel.parcel_id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    parcel.gt_status = update.gt_status
    if update.gt_status == "Verified":
        parcel.confidence_score = min(0.99, parcel.confidence_score + 0.15)

    db.commit()
    return {"message": "Ground truth status updated", "parcel_id": parcel_id, "new_status": parcel.gt_status}
