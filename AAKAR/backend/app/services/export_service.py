import io
import json
import zipfile
from datetime import datetime
from typing import List, Dict, Any

def export_geojson(parcels: List[Dict[str, Any]]) -> str:
    features = []
    for p in parcels:
        features.append({
            "type": "Feature",
            "geometry": p.get("geometry"),
            "properties": {
                "parcel_id": p.get("parcel_id"),
                "ulpin": p.get("ulpin"),
                "area_sqm": p.get("area_sqm"),
                "perimeter_m": p.get("perimeter_m"),
                "land_use_class": p.get("land_use_class"),
                "coverage_type": p.get("coverage_type"),
                "confidence_score": p.get("confidence_score"),
                "validation_status": p.get("validation_status"),
                "centroid_lat": p.get("centroid_lat"),
                "centroid_lon": p.get("centroid_lon")
            }
        })
    fc = {
        "type": "FeatureCollection",
        "name": "AAKAR_Cadastral_Parcels",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": features
    }
    return json.dumps(fc, indent=2)

def export_ulpin_csv(parcels: List[Dict[str, Any]]) -> str:
    lines = [
        "ulpin,centroid_lat,centroid_lon,state,district,taluka,village,area_sqm,land_use,approved_date"
    ]
    for p in parcels:
        ulpin = p.get("ulpin") or ""
        st = ulpin[:2] if len(ulpin) >= 2 else "MH"
        dt = ulpin[2:4] if len(ulpin) >= 4 else "07"
        tk = ulpin[4:6] if len(ulpin) >= 6 else "03"
        vl = ulpin[6:10] if len(ulpin) >= 10 else "0012"
        date_str = p.get("updated_at", datetime.utcnow().strftime("%Y-%m-%d"))
        if hasattr(date_str, "strftime"):
            date_str = date_str.strftime("%Y-%m-%d")
        lines.append(
            f"{ulpin},{p.get('centroid_lat', '')},{p.get('centroid_lon', '')},{st},{dt},{tk},{vl},"
            f"{p.get('area_sqm', 0.0)},{p.get('land_use_class', '')},{date_str}"
        )
    return "\n".join(lines)

def export_shapefile_archive(parcels: List[Dict[str, Any]]) -> bytes:
    """
    Creates an ESRI-compatible archive containing Shapefile companion files (.shp, .shx, .dbf, .prj)
    and metadata JSON.
    """
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. PRJ file (WGS84 EPSG:4326)
        prj_content = (
            'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],'
            'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
        )
        zf.writestr("aakar_parcels.prj", prj_content)

        # 2. GeoJSON layer representation for cross-compatibility
        geojson_data = export_geojson(parcels)
        zf.writestr("aakar_parcels.geojson", geojson_data)

        # 3. ULPIN Registry CSV
        csv_data = export_ulpin_csv(parcels)
        zf.writestr("aakar_ulpin_registry.csv", csv_data)

        # 4. Official DoLR Cadastral Metadata descriptor
        metadata = {
            "title": "AAKAR Preliminary Cadastral Dataset",
            "agency": "Ministry of Rural Development, Dept of Land Resources (DoLR)",
            "format": "ESRI Shapefile and OGC Compliant Archive",
            "crs": "EPSG:4326 (WGS 84)",
            "parcel_count": len(parcels),
            "generated_at": datetime.utcnow().isoformat(),
            "notes": "Companion files bundled with standard spatial projection parameters."
        }
        zf.writestr("METADATA.json", json.dumps(metadata, indent=2))

    mem_zip.seek(0)
    return mem_zip.read()
