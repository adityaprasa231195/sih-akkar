import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

router = APIRouter(prefix="/data", tags=["data"])

INGESTION_JOBS = {}

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    data_type: str = Form("Drone Imagery"),
    crs: str = Form("EPSG:4326")
):
    valid_types = [
        "Drone Imagery", "ORI", "DSM", "DTM", "GIS Parcel Layer", "Ground Truth Data", "GNSS Points"
    ]
    if data_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid data type. Allowed: {valid_types}")

    content = await file.read()
    job_id = f"ingest-{uuid.uuid4().hex[:8]}"

    INGESTION_JOBS[job_id] = {
        "job_id": job_id,
        "file_name": file.filename,
        "data_type": data_type,
        "crs_detected": crs,
        "file_size_bytes": len(content),
        "status": "Ready for Pipeline",
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "status": "Uploaded",
        "job_id": job_id,
        "summary": INGESTION_JOBS[job_id]
    }

@router.get("/jobs/{job_id}")
def get_ingestion_job(job_id: str):
    if job_id not in INGESTION_JOBS:
        raise HTTPException(status_code=404, detail="Ingestion job not found")
    return INGESTION_JOBS[job_id]
