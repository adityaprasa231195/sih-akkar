export type Role = 'Viewer' | 'Editor' | 'Reviewer' | 'Administrator';

export interface User {
  user_id: string;
  username: string;
  email: string;
  role: Role;
  created_at: string;
}

export interface Parcel {
  parcel_id: string;
  ulpin?: string | null;
  geometry: any;
  area_sqm: number;
  perimeter_m: number;
  centroid_lat?: number;
  centroid_lon?: number;
  coverage_type: 'Urban' | 'Rural' | 'PeriUrban' | 'Mixed';
  land_use_class: 'Residential' | 'Commercial' | 'Institutional' | 'Industrial' | 'Open' | 'Transportation' | 'WaterBody' | 'Rural Residential (Abadi)' | 'Agricultural (Irrigated)' | 'Agricultural (Dry)' | 'Gram Panchayat Common Land' | 'Water Body';
  confidence_score: number;
  topology_status: 'Valid' | 'HasWarnings' | 'HasErrors';
  validation_status: 'Pending' | 'InReview' | 'Approved' | 'Rejected';
  gt_status: 'Pending' | 'InProgress' | 'Completed' | 'Verified';
  dispute_risk_score: number;
  dispute_risk_factors: {
    confidence_tier?: string;
    dispute_tier?: string;
    dispute_factors?: Array<{ factor: string; points: number }>;
  };
  created_at: string;
  updated_at: string;
  created_by: string;
  approved_by?: string | null;
}

export interface BuildingFootprint {
  building_id: string;
  parcel_id?: string | null;
  geometry: any;
  height_m: number;
  confidence_score: number;
  is_flagged: boolean;
}

export interface EncroachmentFlag {
  encroachment_flag_id: string;
  parcel_id: string;
  building_id?: string | null;
  flag_type: 'PossibleEncroachment' | 'UnauthorizedConstruction' | 'BoundaryMismatch' | 'NeedsVerification';
  overlap_area_sqm: number;
  confidence: number;
  status: 'Open' | 'UnderReview' | 'Resolved' | 'Dismissed';
  resolved_by?: string | null;
  resolved_at?: string | null;
  notes?: string | null;
}

export interface TopologyError {
  error_id: string;
  feature_id: string;
  error_type: 'Overlap' | 'Gap' | 'Sliver' | 'SelfIntersection' | 'Duplicate' | 'InvalidPolygon' | 'UnclosedBoundary' | 'Misalignment' | 'InconsistentRelationship';
  severity: 'Critical' | 'Warning' | 'Info';
  description: string;
  suggested_correction?: string | null;
  status: 'Open' | 'AutoCorrected' | 'HumanCorrected' | 'Dismissed';
}

export interface ChangeRecord {
  change_record_id: string;
  parcel_id: string;
  change_type: 'NewParcel' | 'Deleted' | 'BoundaryChanged' | 'LandUseChanged' | 'BuildingAdded' | 'BuildingDemolished';
  epoch_before: string;
  epoch_after: string;
  geometry_before?: any;
  geometry_after?: any;
  attribute_diff: Record<string, any>;
  detected_at: string;
}

export interface ParcelVersion {
  parcel_version_id: string;
  parcel_id: string;
  version_number: number;
  geometry_snapshot: any;
  attributes_snapshot: Record<string, any>;
  changed_by: string;
  changed_at: string;
  change_reason: string;
  approved_by?: string | null;
}

export interface DashboardKPIs {
  hectares_processed: number;
  time_saved_pct: number;
  gt_effort_reduced_pct: number;
  topology_health_pct: number;
  open_encroachments: number;
  high_dispute_risk_count: number;
  ulpin_ready_count: number;
  changes_detected_count: number;
}
