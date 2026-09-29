import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ChangeRecord, Parcel, BuildingFootprint
from app.services.change_detection_service import compute_cadastral_changes

router = APIRouter(prefix="/changedetection", tags=["changedetection"])

@router.post("/run")
def run_change_detection(db: Session = Depends(get_db)):
    parcels = db.query(Parcel).all()
    buildings = db.query(BuildingFootprint).all()
    
    # Run change detection service
    parcels_dicts = [{"parcel_id": p.parcel_id, "geometry": p.geometry, "area_sqm": p.area_sqm, "land_use_class": p.land_use_class} for p in parcels]
    buildings_dicts = [{"building_id": b.building_id, "parcel_id": b.parcel_id, "geometry": b.geometry, "height_m": b.height_m} for b in buildings]
    
    # Seed comparison against historical epoch
    result = compute_cadastral_changes(
        epoch_before_name="2024-Q1",
        epoch_after_name="2026-Q1",
        parcels_before=parcels_dicts[:6],
        parcels_after=parcels_dicts,
        buildings_before=buildings_dicts[:2],
        buildings_after=buildings_dicts
    )

    return {
        "job_id": f"chg-job-{uuid.uuid4().hex[:8]}",
        "status": "Completed",
        "epochs": {"before": "2024-Q1", "after": "2026-Q1"},
        "summary": result["summary"],
        "records": result["records"]
    }

@router.get("/results/{job_id}")
def get_change_detection_results(job_id: str, db: Session = Depends(get_db)):
    records = db.query(ChangeRecord).all()
    summary = {
        "NewParcel": sum(1 for r in records if r.change_type == "NewParcel"),
        "Deleted": sum(1 for r in records if r.change_type == "Deleted"),
        "BoundaryChanged": sum(1 for r in records if r.change_type == "BoundaryChanged"),
        "LandUseChanged": sum(1 for r in records if r.change_type == "LandUseChanged"),
        "BuildingAdded": sum(1 for r in records if r.change_type == "BuildingAdded"),
        "BuildingDemolished": sum(1 for r in records if r.change_type == "BuildingDemolished"),
        "total_changes": len(records)
    }
    return {
        "job_id": job_id,
        "summary": summary,
        "records": records
    }

@router.get("/report/{job_id}/download")
def download_change_report(job_id: str, db: Session = Depends(get_db)):
    records = db.query(ChangeRecord).all()
    report_lines = [
        "================================================================",
        "AAKAR CADASTRAL CHANGE DETECTION REPORT",
        "Ministry of Rural Development, Dept of Land Resources (DoLR)",
        f"Generated At: {datetime.utcnow().isoformat()}",
        f"Job ID: {job_id}",
        "================================================================",
        "",
        "RECORD ID | PARCEL ID | CHANGE TYPE | DETECTED DATE",
        "----------------------------------------------------------------"
    ]
    for r in records:
        report_lines.append(f"{r.change_record_id} | {r.parcel_id} | {r.change_type} | {r.detected_at}")

    content = "\n".join(report_lines)
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename=aakar_change_report_{job_id}.txt"}
    )
