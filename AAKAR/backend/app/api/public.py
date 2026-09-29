from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Parcel
from app.schemas.schemas import PublicParcelLookupResult
from app.core.config import settings

router = APIRouter(prefix="/public", tags=["public"])

@router.get("/parcel/{ulpin}", response_model=PublicParcelLookupResult)
def lookup_parcel_by_ulpin(ulpin: str, db: Session = Depends(get_db)):
    parcel = db.query(Parcel).filter(Parcel.ulpin == ulpin.upper()).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="No registered parcel found with this ULPIN ID")

    # Safe public response omitting sensitive ownership or dispute indicators
    date_str = parcel.updated_at.strftime("%Y-%m-%d") if parcel.updated_at else "2026-09-29"
    return {
        "ulpin": parcel.ulpin,
        "geometry": parcel.geometry,
        "land_use_class": parcel.land_use_class,
        "area_sqm": parcel.area_sqm,
        "validation_status": parcel.validation_status,
        "last_approved_date": date_str,
        "state": "Maharashtra",
        "district": "Pune",
        "taluka": "Haveli",
        "village": "Wagholi"
    }

@router.get("/parcel/search", response_model=List[PublicParcelLookupResult])
def search_parcels(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    query_str = f"%{q.upper()}%"
    parcels = db.query(Parcel).filter(
        (Parcel.ulpin.like(query_str)) |
        (Parcel.parcel_id.like(f"%{q}%"))
    ).filter(Parcel.validation_status == "Approved").all()

    results = []
    for p in parcels:
        if p.ulpin:
            date_str = p.updated_at.strftime("%Y-%m-%d") if p.updated_at else "2026-09-29"
            results.append({
                "ulpin": p.ulpin,
                "geometry": p.geometry,
                "land_use_class": p.land_use_class,
                "area_sqm": p.area_sqm,
                "validation_status": p.validation_status,
                "last_approved_date": date_str,
                "state": "Maharashtra",
                "district": "Pune",
                "taluka": "Haveli",
                "village": "Wagholi"
            })
    return results
