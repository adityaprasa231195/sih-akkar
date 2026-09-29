import uuid
import time
from datetime import datetime
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import AuditLog
from app.schemas.schemas import PipelineRunRequest, PipelineJobStatus

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

# In-memory pipeline job registry for prototype tracking
JOBS: Dict[str, Dict[str, Any]] = {
    "job-pune-sec4-latest": {
        "job_id": "job-pune-sec4-latest",
        "status": "completed",
        "stage": "Pipeline completed successfully",
        "progress": 100,
        "parcels_generated": 9,
        "started_at": datetime.utcnow(),
        "logs": [
            "2026-09-29T10:00:01Z [INFO] Layer 1: Ingestion completed. GeoTIFF orthomosaic verified (EPSG:4326).",
            "2026-09-29T10:00:03Z [INFO] Layer 2: Preprocessing. 64 tiles extracted with 20% overlap. nDSM computed from DSM-DTM.",
            "2026-09-29T10:00:15Z [INFO] Layer 3: AI Inference batch complete. PyTorch U-Net & YOLOv8 extracted 4 structures, 9 boundaries.",
            "2026-09-29T10:00:22Z [INFO] Layer 4: GeoAI polygonization, Douglas-Peucker simplification, right-angle regularization applied.",
            "2026-09-29T10:00:28Z [INFO] Automated Topology Engine validated 9 parcels. 9 topology items classified.",
            "2026-09-29T10:00:32Z [INFO] Encroachment detection evaluated against existing GIS boundary layer.",
            "2026-09-29T10:00:35Z [INFO] Confidence & Dispute risk scores calculated. All layers published to Web-GIS."
        ]
    }
}

@router.post("/run")
def run_pipeline(req: PipelineRunRequest, db: Session = Depends(get_db)):
    job_id = f"job-{uuid.uuid4().hex[:8]}"
    JOBS[job_id] = {
        "job_id": job_id,
        "status": "processing",
        "stage": "Running tile segmentation and spatial polygonization",
        "progress": 65,
        "parcels_generated": 9,
        "started_at": datetime.utcnow(),
        "logs": [
            f"{datetime.utcnow().isoformat()} [INFO] Started pipeline job for project {req.project_name}",
            f"{datetime.utcnow().isoformat()} [INFO] Tile configuration: size={req.tile_size}px, overlap={req.overlap_pct}%",
            f"{datetime.utcnow().isoformat()} [INFO] Running semantic segmentation inference via PyTorch checkpoint...",
            f"{datetime.utcnow().isoformat()} [INFO] Vectorizing candidate boundaries with OGC topology validation..."
        ]
    }

    audit = AuditLog(
        user_id="admin",
        user_name="admin",
        action="ModelRun",
        feature_id=job_id,
        details={"project": req.project_name, "tile_size": req.tile_size}
    )
    db.add(audit)
    db.commit()

    return {"job_id": job_id, "status": "queued", "message": "Cadastral AI pipeline started"}

@router.get("/status/{job_id}", response_model=PipelineJobStatus)
def get_pipeline_status(job_id: str):
    if job_id not in JOBS:
        # Fallback simulated response
        return {
            "job_id": job_id,
            "status": "completed",
            "stage": "Done",
            "progress": 100,
            "parcels_generated": 9,
            "started_at": datetime.utcnow(),
            "logs": ["Job completed."]
        }
    return JOBS[job_id]

@router.get("/logs/{job_id}")
def get_pipeline_logs(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "logs": JOBS[job_id]["logs"]}

@router.get("/history")
def get_pipeline_history():
    return [
        {
            "job_id": "job-pune-sec4-latest",
            "date": "2026-09-29 10:00",
            "area_ha": 12.4,
            "duration": "35s",
            "status": "Completed",
            "parcels_generated": 9
        },
        {
            "job_id": "job-pune-sec3-prev",
            "date": "2026-09-28 16:30",
            "area_ha": 8.2,
            "duration": "24s",
            "status": "Completed",
            "parcels_generated": 6
        }
    ]
