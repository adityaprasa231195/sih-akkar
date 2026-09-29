import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Parcel, AuditLog
from app.schemas.schemas import ExportRequest, ExportResponse
from app.services.export_service import export_shapefile_archive, export_geojson, export_ulpin_csv

router = APIRouter(prefix="/export", tags=["export"])

EXPORTS = {}

@router.post("", response_model=ExportResponse)
def request_export(req: ExportRequest, db: Session = Depends(get_db)):
    query = db.query(Parcel)
    if req.status_filter == "Approved":
        query = query.filter(Parcel.validation_status == "Approved")
    parcels = query.all()

    export_id = f"exp-{uuid.uuid4().hex[:8]}"
    parcels_dicts = [
        {
            "parcel_id": p.parcel_id,
            "ulpin": p.ulpin,
            "geometry": p.geometry,
            "area_sqm": p.area_sqm,
            "perimeter_m": p.perimeter_m,
            "land_use_class": p.land_use_class,
            "coverage_type": p.coverage_type,
            "confidence_score": p.confidence_score,
            "validation_status": p.validation_status,
            "centroid_lat": p.centroid_lat,
            "centroid_lon": p.centroid_lon
        }
        for p in parcels
    ]

    # Generate companion shapefile zip
    archive_bytes = export_shapefile_archive(parcels_dicts)

    EXPORTS[export_id] = {
        "export_id": export_id,
        "archive_bytes": archive_bytes,
        "parcel_count": len(parcels),
        "formats": req.formats,
        "created_at": datetime.utcnow()
    }

    audit = AuditLog(
        user_id="admin",
        user_name="admin",
        action="Export",
        feature_id=export_id,
        details={"formats": req.formats, "parcel_count": len(parcels)}
    )
    db.add(audit)
    db.commit()

    return {
        "export_id": export_id,
        "status": "Ready",
        "download_url": f"/api/v1/export/{export_id}/download",
        "parcel_count": len(parcels),
        "created_at": datetime.utcnow()
    }

@router.get("/{export_id}/download")
def download_export(export_id: str):
    if export_id not in EXPORTS:
        raise HTTPException(status_code=404, detail="Export not found")

    item = EXPORTS[export_id]
    return Response(
        content=item["archive_bytes"],
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=aakar_cadastral_{export_id}.zip"}
    )
