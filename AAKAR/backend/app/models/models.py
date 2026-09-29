import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Float, Integer, Boolean, DateTime, Text, JSON, ForeignKey
)
from app.core.database import Base

def gen_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=gen_uuid)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="Viewer", nullable=False)  # Viewer, Editor, Reviewer, Administrator
    created_at = Column(DateTime, default=utc_now)

class Parcel(Base):
    __tablename__ = "parcels"

    parcel_id = Column(String, primary_key=True, default=gen_uuid)
    ulpin = Column(String(14), unique=True, nullable=True, index=True)
    geometry = Column(JSON, nullable=False)  # GeoJSON Polygon or MultiPolygon
    area_sqm = Column(Float, nullable=False, default=0.0)
    perimeter_m = Column(Float, nullable=False, default=0.0)
    centroid_lat = Column(Float, nullable=True)
    centroid_lon = Column(Float, nullable=True)
    coverage_type = Column(String(50), default="Urban")  # Urban, Rural, PeriUrban, Mixed
    land_use_class = Column(String(50), default="Residential")  # Residential, Commercial, Institutional, Industrial, Open, Transportation, WaterBody
    confidence_score = Column(Float, default=0.85)  # 0.0 to 1.0
    topology_status = Column(String(50), default="Valid")  # Valid, HasWarnings, HasErrors
    validation_status = Column(String(50), default="Pending")  # Pending, InReview, Approved, Rejected
    gt_status = Column(String(50), default="Pending")  # Pending, InProgress, Completed, Verified
    dispute_risk_score = Column(Integer, default=15)  # 0 to 100
    dispute_risk_factors = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    created_by = Column(String, default="system")
    approved_by = Column(String, nullable=True)

class BuildingFootprint(Base):
    __tablename__ = "building_footprints"

    building_id = Column(String, primary_key=True, default=gen_uuid)
    geometry = Column(JSON, nullable=False)
    parcel_id = Column(String, ForeignKey("parcels.parcel_id"), nullable=True)
    height_m = Column(Float, default=3.5)
    confidence_score = Column(Float, default=0.90)
    is_flagged = Column(Boolean, default=False)

class EncroachmentFlag(Base):
    __tablename__ = "encroachment_flags"

    encroachment_flag_id = Column(String, primary_key=True, default=gen_uuid)
    parcel_id = Column(String, ForeignKey("parcels.parcel_id"), nullable=False)
    building_id = Column(String, ForeignKey("building_footprints.building_id"), nullable=True)
    flag_type = Column(String(50), default="PossibleEncroachment")  # PossibleEncroachment, UnauthorizedConstruction, BoundaryMismatch, NeedsVerification
    overlap_area_sqm = Column(Float, default=0.0)
    confidence = Column(Float, default=0.85)
    status = Column(String(50), default="Open")  # Open, UnderReview, Resolved, Dismissed
    resolved_by = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

class TopologyError(Base):
    __tablename__ = "topology_errors"

    error_id = Column(String, primary_key=True, default=gen_uuid)
    feature_id = Column(String, nullable=False)
    error_type = Column(String(50), nullable=False)  # Overlap, Gap, Sliver, SelfIntersection, Duplicate, InvalidPolygon, UnclosedBoundary, Misalignment, InconsistentRelationship
    severity = Column(String(20), default="Warning")  # Critical, Warning, Info
    description = Column(Text, nullable=False)
    suggested_correction = Column(Text, nullable=True)
    status = Column(String(50), default="Open")  # Open, AutoCorrected, HumanCorrected, Dismissed

class ChangeRecord(Base):
    __tablename__ = "change_records"

    change_record_id = Column(String, primary_key=True, default=gen_uuid)
    parcel_id = Column(String, ForeignKey("parcels.parcel_id"), nullable=False)
    change_type = Column(String(50), nullable=False)  # NewParcel, Deleted, BoundaryChanged, LandUseChanged, BuildingAdded, BuildingDemolished
    epoch_before = Column(DateTime, default=utc_now)
    epoch_after = Column(DateTime, default=utc_now)
    geometry_before = Column(JSON, nullable=True)
    geometry_after = Column(JSON, nullable=True)
    attribute_diff = Column(JSON, default=dict)
    detected_at = Column(DateTime, default=utc_now)

class ParcelVersion(Base):
    __tablename__ = "parcel_versions"

    parcel_version_id = Column(String, primary_key=True, default=gen_uuid)
    parcel_id = Column(String, ForeignKey("parcels.parcel_id"), nullable=False)
    version_number = Column(Integer, default=1)
    geometry_snapshot = Column(JSON, nullable=False)
    attributes_snapshot = Column(JSON, default=dict)
    changed_by = Column(String, default="system")
    changed_at = Column(DateTime, default=utc_now)
    change_reason = Column(Text, default="Initial cadastral generation")
    approved_by = Column(String, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, nullable=False)
    user_name = Column(String, nullable=False, default="Admin")
    action = Column(String(50), nullable=False)  # Edit, Approve, Reject, Export, ModelRun, GTUpload, Rollback, EncroachmentResolved
    feature_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=utc_now)
    details = Column(JSON, default=dict)
