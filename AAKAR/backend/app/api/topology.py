from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import TopologyError, Parcel
from app.schemas.schemas import TopologyErrorOut, TopologyResolveRequest
from app.services.topology_service import validate_topology

router = APIRouter(prefix="/topology", tags=["topology"])

@router.get("/errors", response_model=List[TopologyErrorOut])
def list_topology_errors(
    severity: Optional[str] = Query(None),
    error_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(TopologyError)
    if severity and severity != "All":
        query = query.filter(TopologyError.severity == severity)
    if error_type and error_type != "All":
        query = query.filter(TopologyError.error_type == error_type)
    if status and status != "All":
        query = query.filter(TopologyError.status == status)
    return query.all()

@router.post("/run")
def run_topology_validation(db: Session = Depends(get_db)):
    parcels = db.query(Parcel).all()
    parcels_data = [
        {"parcel_id": p.parcel_id, "geometry": p.geometry}
        for p in parcels
    ]
    detected = validate_topology(parcels_data)
    
    # Store newly detected errors
    added_count = 0
    for err in detected:
        existing = db.query(TopologyError).filter(
            TopologyError.feature_id == err["feature_id"],
            TopologyError.error_type == err["error_type"],
            TopologyError.status == "Open"
        ).first()
        if not existing:
            new_err = TopologyError(**err)
            db.add(new_err)
            added_count += 1
            
    db.commit()
    return {
        "status": "Completed",
        "total_errors_detected": len(detected),
        "new_errors_logged": added_count
    }

@router.put("/errors/{error_id}/resolve", response_model=TopologyErrorOut)
def resolve_topology_error(
    error_id: str,
    req: TopologyResolveRequest,
    db: Session = Depends(get_db)
):
    err = db.query(TopologyError).filter(TopologyError.error_id == error_id).first()
    if not err:
        raise HTTPException(status_code=404, detail="Topology error not found")

    if req.action == "dismiss":
        err.status = "Dismissed"
    elif req.action == "accept_suggested":
        err.status = "AutoCorrected"
    else:
        err.status = "HumanCorrected"

    db.commit()
    db.refresh(err)
    return err
