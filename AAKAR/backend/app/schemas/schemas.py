from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "Viewer"

class UserOut(BaseModel):
    user_id: str
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    role: str

# Parcel Schemas
class ParcelOut(BaseModel):
    parcel_id: str
    ulpin: Optional[str] = None
    geometry: Dict[str, Any]
    area_sqm: float
    perimeter_m: float
    centroid_lat: Optional[float] = None
    centroid_lon: Optional[float] = None
    coverage_type: str
    land_use_class: str
    confidence_score: float
    topology_status: str
    validation_status: str
    gt_status: str
    dispute_risk_score: int
    dispute_risk_factors: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    created_by: str
    approved_by: Optional[str] = None

    class Config:
        from_attributes = True

class ParcelUpdate(BaseModel):
    geometry: Optional[Dict[str, Any]] = None
    land_use_class: Optional[str] = None
    coverage_type: Optional[str] = None
    change_reason: Optional[str] = "Manual boundary adjustment"

class ParcelApproveRequest(BaseModel):
    override_high_risk: Optional[bool] = False
    override_reason: Optional[str] = None

class ParcelRejectRequest(BaseModel):
    rejection_reason: str

# Building Schemas
class BuildingFootprintOut(BaseModel):
    building_id: str
    geometry: Dict[str, Any]
    parcel_id: Optional[str] = None
    height_m: float
    confidence_score: float
    is_flagged: bool

    class Config:
        from_attributes = True

# Encroachment Schemas
class EncroachmentFlagOut(BaseModel):
    encroachment_flag_id: str
    parcel_id: str
    building_id: Optional[str] = None
    flag_type: str
    overlap_area_sqm: float
    confidence: float
    status: str
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class EncroachmentResolveRequest(BaseModel):
    action: str = "resolve"  # resolve, dismiss
    notes: Optional[str] = None

# Topology Schemas
class TopologyErrorOut(BaseModel):
    error_id: str
    feature_id: str
    error_type: str
    severity: str
    description: str
    suggested_correction: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class TopologyResolveRequest(BaseModel):
    action: str = "accept_suggested"  # accept_suggested, custom, dismiss
    resolution_notes: Optional[str] = None

# Ground Truth Schemas
class GTStatusUpdate(BaseModel):
    gt_status: str  # Pending, InProgress, Completed, Verified
    field_notes: Optional[str] = None

# Pipeline Schemas
class PipelineRunRequest(BaseModel):
    project_name: str = "Pune_Sector_4_Drone_Survey"
    tile_size: int = 512
    overlap_pct: int = 20
    confidence_threshold: float = 0.50
    enable_encroachment_detection: bool = True

class PipelineJobStatus(BaseModel):
    job_id: str
    status: str  # queued, processing, completed, failed
    stage: str
    progress: int
    parcels_generated: int
    started_at: datetime
    logs: List[str]

# Change Detection Schemas
class ChangeDetectionRequest(BaseModel):
    dataset_epoch_before: str = "2024-Q1"
    dataset_epoch_after: str = "2026-Q1"

class ChangeRecordOut(BaseModel):
    change_record_id: str
    parcel_id: str
    change_type: str
    epoch_before: datetime
    epoch_after: datetime
    geometry_before: Optional[Dict[str, Any]] = None
    geometry_after: Optional[Dict[str, Any]] = None
    attribute_diff: Dict[str, Any]
    detected_at: datetime

    class Config:
        from_attributes = True

# Export Schemas
class ExportRequest(BaseModel):
    formats: List[str]  # GeoJSON, Shapefile, GeoPackage, ULPIN_CSV, PDF
    status_filter: str = "Approved"  # Approved, All
    target_crs: str = "EPSG:4326"

class ExportResponse(BaseModel):
    export_id: str
    status: str
    download_url: str
    parcel_count: int
    created_at: datetime

# Audit Log Schemas
class AuditLogOut(BaseModel):
    log_id: str
    user_id: str
    user_name: str
    action: str
    feature_id: Optional[str] = None
    timestamp: datetime
    details: Dict[str, Any]

    class Config:
        from_attributes = True

# Public Lookup Schemas
class PublicParcelLookupResult(BaseModel):
    ulpin: str
    geometry: Dict[str, Any]
    land_use_class: str
    area_sqm: float
    validation_status: str
    last_approved_date: Optional[str] = None
    state: str
    district: str
    taluka: str
    village: str
