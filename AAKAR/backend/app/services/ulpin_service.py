from typing import Tuple
from shapely.geometry import shape
from sqlalchemy.orm import Session
from app.models.models import Parcel
from app.core.config import settings

def calculate_centroid(geojson_geom: dict) -> Tuple[float, float]:
    try:
        geom = shape(geojson_geom)
        return float(geom.centroid.y), float(geom.centroid.x)
    except Exception:
        # Fallback approximate center
        coords = []
        if geojson_geom.get("type") == "Polygon":
            coords = geojson_geom.get("coordinates", [[]])[0]
        elif geojson_geom.get("type") == "MultiPolygon":
            coords = geojson_geom.get("coordinates", [[[]]])[0][0]
        if coords:
            lats = [c[1] for c in coords]
            lons = [c[0] for c in coords]
            return sum(lats)/len(lats), sum(lons)/len(lons)
        return 18.5204, 73.8567

def generate_ulpin(
    db: Session,
    parcel: Parcel,
    state: str = settings.DEFAULT_STATE,
    district: str = settings.DEFAULT_DISTRICT,
    taluka: str = settings.DEFAULT_TALUKA,
    village: str = settings.DEFAULT_VILLAGE
) -> str:
    """
    Format: [ST][DT][TK][VL][SEQN]
    ST: 2-char state (e.g. MH)
    DT: 2-char district (e.g. 07)
    TK: 2-char taluka (e.g. 03)
    VL: 4-char village (e.g. 0012)
    SEQN: 4-char sequential zero-padded (e.g. 0001)
    Total 14 characters.
    """
    prefix = f"{state[:2].upper()}{district[:2]}{taluka[:2]}{village[:4]}"
    
    # Count existing approved parcels with this prefix to assign sequence
    existing_count = db.query(Parcel).filter(
        Parcel.ulpin.like(f"{prefix}%")
    ).count()
    
    seqn = f"{existing_count + 1:04d}"
    ulpin = f"{prefix}{seqn}"
    
    # Ensure centroid is calculated for geo-anchor
    if parcel.geometry:
        lat, lon = calculate_centroid(parcel.geometry)
        parcel.centroid_lat = round(lat, 6)
        parcel.centroid_lon = round(lon, 6)
        
    return ulpin
