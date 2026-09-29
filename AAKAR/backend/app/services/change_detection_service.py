import uuid
from datetime import datetime
from typing import List, Dict, Any
from shapely.geometry import shape

def compute_cadastral_changes(
    epoch_before_name: str,
    epoch_after_name: str,
    parcels_before: List[Dict[str, Any]],
    parcels_after: List[Dict[str, Any]],
    buildings_before: List[Dict[str, Any]],
    buildings_after: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Compares two survey epochs and classifies cadastral changes:
    - NewParcel
    - Deleted
    - BoundaryChanged
    - LandUseChanged
    - BuildingAdded
    - BuildingDemolished
    """
    records = []
    before_map = {p["parcel_id"]: p for p in parcels_before}
    after_map = {p["parcel_id"]: p for p in parcels_after}

    # Check modified and deleted parcels
    for p_id, p_before in before_map.items():
        if p_id not in after_map:
            records.append({
                "change_record_id": str(uuid.uuid4()),
                "parcel_id": p_id,
                "change_type": "Deleted",
                "epoch_before": datetime.utcnow(),
                "epoch_after": datetime.utcnow(),
                "geometry_before": p_before.get("geometry"),
                "geometry_after": None,
                "attribute_diff": {"status": "Parcel retired or merged in latest epoch"},
                "detected_at": datetime.utcnow()
            })
        else:
            p_after = after_map[p_id]
            # Check land use change
            if p_before.get("land_use_class") != p_after.get("land_use_class"):
                records.append({
                    "change_record_id": str(uuid.uuid4()),
                    "parcel_id": p_id,
                    "change_type": "LandUseChanged",
                    "epoch_before": datetime.utcnow(),
                    "epoch_after": datetime.utcnow(),
                    "geometry_before": p_before.get("geometry"),
                    "geometry_after": p_after.get("geometry"),
                    "attribute_diff": {
                        "before_land_use": p_before.get("land_use_class"),
                        "after_land_use": p_after.get("land_use_class")
                    },
                    "detected_at": datetime.utcnow()
                })

            # Check boundary change using area / geometry comparison
            if abs(p_before.get("area_sqm", 0) - p_after.get("area_sqm", 0)) > 5.0:
                records.append({
                    "change_record_id": str(uuid.uuid4()),
                    "parcel_id": p_id,
                    "change_type": "BoundaryChanged",
                    "epoch_before": datetime.utcnow(),
                    "epoch_after": datetime.utcnow(),
                    "geometry_before": p_before.get("geometry"),
                    "geometry_after": p_after.get("geometry"),
                    "attribute_diff": {
                        "area_delta_sqm": round(p_after.get("area_sqm", 0) - p_before.get("area_sqm", 0), 2)
                    },
                    "detected_at": datetime.utcnow()
                })

    # Check newly created parcels
    for p_id, p_after in after_map.items():
        if p_id not in before_map:
            records.append({
                "change_record_id": str(uuid.uuid4()),
                "parcel_id": p_id,
                "change_type": "NewParcel",
                "epoch_before": datetime.utcnow(),
                "epoch_after": datetime.utcnow(),
                "geometry_before": None,
                "geometry_after": p_after.get("geometry"),
                "attribute_diff": {
                    "area_sqm": p_after.get("area_sqm"),
                    "land_use": p_after.get("land_use_class")
                },
                "detected_at": datetime.utcnow()
            })

    # Check building additions / demolitions
    b_before_ids = {b.get("building_id") for b in buildings_before}
    b_after_ids = {b.get("building_id") for b in buildings_after}

    for b in buildings_after:
        if b.get("building_id") not in b_before_ids:
            records.append({
                "change_record_id": str(uuid.uuid4()),
                "parcel_id": b.get("parcel_id") or "unassigned",
                "change_type": "BuildingAdded",
                "epoch_before": datetime.utcnow(),
                "epoch_after": datetime.utcnow(),
                "geometry_before": None,
                "geometry_after": b.get("geometry"),
                "attribute_diff": {"building_id": b.get("building_id"), "height_m": b.get("height_m")},
                "detected_at": datetime.utcnow()
            })

    for b in buildings_before:
        if b.get("building_id") not in b_after_ids:
            records.append({
                "change_record_id": str(uuid.uuid4()),
                "parcel_id": b.get("parcel_id") or "unassigned",
                "change_type": "BuildingDemolished",
                "epoch_before": datetime.utcnow(),
                "epoch_after": datetime.utcnow(),
                "geometry_before": b.get("geometry"),
                "geometry_after": None,
                "attribute_diff": {"building_id": b.get("building_id")},
                "detected_at": datetime.utcnow()
            })

    # Aggregate metrics
    summary = {
        "NewParcel": sum(1 for r in records if r["change_type"] == "NewParcel"),
        "Deleted": sum(1 for r in records if r["change_type"] == "Deleted"),
        "BoundaryChanged": sum(1 for r in records if r["change_type"] == "BoundaryChanged"),
        "LandUseChanged": sum(1 for r in records if r["change_type"] == "LandUseChanged"),
        "BuildingAdded": sum(1 for r in records if r["change_type"] == "BuildingAdded"),
        "BuildingDemolished": sum(1 for r in records if r["change_type"] == "BuildingDemolished"),
        "total_changes": len(records)
    }

    return {"summary": summary, "records": records}
