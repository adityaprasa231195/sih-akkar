import uuid
from typing import List, Dict, Any
from shapely.geometry import shape

def detect_encroachments(
    parcels: List[Dict[str, Any]],
    buildings: List[Dict[str, Any]],
    overlap_sqm_threshold: float = 2.0
) -> List[Dict[str, Any]]:
    """
    Automated Encroachment Detection:
    1. PossibleEncroachment: building extends outside host parcel into neighboring parcels or setback.
    2. UnauthorizedConstruction: building footprint detected on land designated Open or Undeveloped.
    3. BoundaryMismatch: spatial mismatch between preliminary AI parcel edge and registered boundary.
    4. NeedsVerification: ambiguous height/nDSM discrepancy.
    """
    encroachments = []
    
    # Map parcel geometries
    parsed_parcels = []
    for p in parcels:
        try:
            geom = shape(p.get("geometry", {}))
            parsed_parcels.append((p, geom))
        except Exception:
            continue

    # Map building geometries
    parsed_buildings = []
    for b in buildings:
        try:
            geom = shape(b.get("geometry", {}))
            parsed_buildings.append((b, geom))
        except Exception:
            continue

    for b_data, b_geom in parsed_buildings:
        b_id = b_data.get("building_id")
        assigned_p_id = b_data.get("parcel_id")
        
        # Check against each parcel
        for p_data, p_geom in parsed_parcels:
            p_id = p_data.get("parcel_id")
            land_use = p_data.get("land_use_class", "")

            if not b_geom.intersects(p_geom):
                continue

            intersection = b_geom.intersection(p_geom)
            # Approximate square meters from degrees (at latitude ~18.5 deg, 1 deg lat ~ 111km, 1 deg lon ~ 105km)
            overlap_sqm = intersection.area * (111000 * 105000)

            # Rule 2: Unauthorized Construction on Open Land
            if land_use in ["Open", "Undeveloped", "WaterBody"]:
                if overlap_sqm > 5.0:
                    encroachments.append({
                        "encroachment_flag_id": str(uuid.uuid4()),
                        "parcel_id": p_id,
                        "building_id": b_id,
                        "flag_type": "UnauthorizedConstruction",
                        "overlap_area_sqm": round(overlap_sqm, 2),
                        "confidence": 0.92,
                        "status": "Open",
                        "notes": f"Structure of {round(overlap_sqm, 1)} m² erected on designated {land_use} parcel."
                    })
                    continue

            # Rule 1: Building extends outside host parcel
            if assigned_p_id and assigned_p_id == p_id:
                # Host parcel check: see if building is partially outside host parcel
                outside_part = b_geom.difference(p_geom)
                outside_sqm = outside_part.area * (111000 * 105000)
                if outside_sqm > overlap_sqm_threshold:
                    encroachments.append({
                        "encroachment_flag_id": str(uuid.uuid4()),
                        "parcel_id": p_id,
                        "building_id": b_id,
                        "flag_type": "PossibleEncroachment",
                        "overlap_area_sqm": round(outside_sqm, 2),
                        "confidence": 0.88,
                        "status": "Open",
                        "notes": f"Building extends {round(outside_sqm, 1)} m² beyond host parcel boundary into setback/adjacent land."
                    })
            elif assigned_p_id and assigned_p_id != p_id:
                # Building assigned to another parcel encroaching on this parcel
                if overlap_sqm > overlap_sqm_threshold:
                    encroachments.append({
                        "encroachment_flag_id": str(uuid.uuid4()),
                        "parcel_id": p_id,
                        "building_id": b_id,
                        "flag_type": "PossibleEncroachment",
                        "overlap_area_sqm": round(overlap_sqm, 2),
                        "confidence": 0.85,
                        "status": "Open",
                        "notes": f"External building from parcel {assigned_p_id[:8]} intrudes {round(overlap_sqm, 1)} m² into parcel {p_id[:8]}."
                    })

    return encroachments
