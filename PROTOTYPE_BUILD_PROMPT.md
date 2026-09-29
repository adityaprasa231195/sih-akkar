# AAKAR — AI-Based Automated Urban Parcel Mapping & Cadastral Feature Extraction
## AI IDE Build Prompt

---

## Project Identity

- **App Name:** AAKAR
- **Tagline:** "Mapping Every Corner of India"
- **Domain:** GeoAI / Cadastral Mapping / Urban & Rural Land Records
- **Organization:** Ministry of Rural Development, Dept of Land Resources (DoLR), Government of India
- **Category:** Software — Smart Automation
- **Purpose:** Automate extraction of cadastral features (parcel boundaries, building footprints, road networks, land-use) from high-resolution drone imagery using AI/ML, generate topology-validated preliminary parcel maps, and provide a Web-GIS dashboard for human-in-the-loop expert review — making AAKAR the single unified platform that replaces fragmented systems like NAKSHA (urban-only), SVAMITVA (rural-only), and Bhu-Aadhaar (IDs only).

---

## Build Philosophy

This is a **prototype that must look and feel like a production system**. Every screen, API, and feature should appear complete and real. No placeholder UI, no "coming soon" text, no skeleton pages. If a feature is in this prompt, build it fully — even if the underlying AI model uses a pre-trained checkpoint instead of a fine-tuned one. The prototype should be demonstrable end-to-end without apology.

---

## Design System — AAKAR UI/UX

Apply this design system to every screen, component, and page. No exceptions.

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--bg-primary` | `#FFFFFF` | Page background, card background |
| `--bg-secondary` | `#F7F8FA` | Sidebar, panel backgrounds |
| `--bg-subtle` | `#EFF1F5` | Table rows (alt), input backgrounds |
| `--border` | `#E4E7EC` | All borders, dividers |
| `--text-primary` | `#111827` | Headings, labels |
| `--text-secondary` | `#6B7280` | Subtext, descriptions |
| `--text-muted` | `#9CA3AF` | Placeholders, inactive states |
| `--accent` | `#2563EB` | Primary buttons, active links, map highlights |
| `--accent-hover` | `#1D4ED8` | Hover state for accent |
| `--success` | `#16A34A` | High confidence badges, approved status |
| `--warning` | `#D97706` | Medium confidence, warning badges |
| `--danger` | `#DC2626` | Low confidence, error badges, encroachment flags |
| `--info` | `#0891B2` | Info badges, neutral notifications |
| `--map-parcel` | `#2563EB` | Parcel boundary stroke on map |
| `--map-building` | `#7C3AED` | Building footprint stroke on map |
| `--map-road` | `#374151` | Road network stroke on map |
| `--map-encroach` | `#DC2626` | Encroachment flag overlay |
| `--map-high-conf` | `#16A34A` | High confidence parcel fill (20% opacity) |
| `--map-mid-conf` | `#D97706` | Medium confidence parcel fill (20% opacity) |
| `--map-low-conf` | `#DC2626` | Low confidence parcel fill (20% opacity) |

### Typography

- **Font:** Inter (Google Fonts) — load via CDN
- **Headings:** `font-weight: 600`, `letter-spacing: -0.02em`
- **Body:** `font-weight: 400`, `line-height: 1.6`
- **Mono/code:** `font-family: 'JetBrains Mono', monospace` — for parcel IDs, coordinates, ULPIN codes

### Spacing & Layout

- Base unit: `4px`. All spacing in multiples of 4 (8, 12, 16, 24, 32, 48)
- Page max-width: `1440px`, centered
- Sidebar width: `260px` fixed
- Card border-radius: `12px`
- Button border-radius: `8px`
- Input border-radius: `8px`
- Box shadow (cards): `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)`

### Component Patterns

- **Buttons:** Flat, no gradient. Primary = `--accent` fill, white text. Secondary = white fill, `--border` border, `--text-primary` text. Danger = `--danger` fill, white text.
- **Badges/Pills:** Small, rounded-full. Color-coded by confidence/status. No borders, use background + text color only.
- **Tables:** White background, `--border` row dividers, `--bg-subtle` for alt rows. Sticky header.
- **Modals:** Centered overlay, white card, `--bg-primary` backdrop at 60% opacity. Close button top-right.
- **Toasts/Notifications:** Slide in from top-right. Auto-dismiss in 4s. Variants: success, warning, danger, info.
- **Sidebar nav items:** `--text-secondary` default, `--accent` when active, `--bg-subtle` active background.
- **Map panels:** Dark map tiles (Carto Dark Matter or OpenStreetMap) with white overlay panels. Map controls (zoom, layer toggle) in white cards with `--border` border.
- **Empty states:** Centered illustration (SVG), short description, one action button. No lorem ipsum.
- **Loading states:** Skeleton shimmer using `--bg-subtle` animated gradient. No spinning wheels.
- **Forms:** Labels above inputs. Helper text below in `--text-muted`. Error text in `--danger`. Inline validation.

### Icons

- Use **Lucide React** icon set throughout. No mixing icon sets.

### Responsive

- Desktop-first (1280px+). The map view does not need to be mobile-responsive. All other pages (login, dashboard, data upload, export, admin) must work at 768px+.

---

## System Architecture — Six Layers

### Layer 1 — Data Acquisition
- Accept: drone imagery (GeoTIFF, JPEG2000), ORI, DSM rasters, DTM rasters, GIS parcel vectors (Shapefile, GeoPackage, GeoJSON), Ground Truth datasets (vector + tabular), GNSS/CORS survey points
- Validate on upload: data completeness, CRS presence, format compliance
- Reject bad inputs with descriptive error messages before pipeline entry
- Store in PostGIS with spatial indexing

### Layer 2 — Preprocessing
- Image quality check: blur detection, exposure/contrast check
- Image tiling: divide orthomosaics into overlapping tiles (tile size + overlap configurable)
- Radiometric normalization and noise reduction
- Spatial alignment: co-register all inputs to a single target CRS (EPSG configurable, default: EPSG:4326)
- CRS transformation via pyproj/GDAL
- nDSM computation: `nDSM = DSM − DTM`
- Prepare tile batches for AI inference

### Layer 3 — AI/ML Engine
- **Semantic Segmentation** (U-Net or DeepLabV3+, PyTorch): pixel-level classes — building surface, road, pathway, vegetation, water body, open land, boundary indicator
- **Instance Segmentation** (Mask R-CNN): individual building footprint delineation in dense clusters
- **Object Detection** (YOLOv8): fast initial structure detection
- **Boundary Prediction**: edge detection + segmentation outputs → parcel boundary candidates
- **Land-Use Classification**: Residential / Commercial / Institutional / Industrial / Open-Undeveloped / Transportation / Water Bodies
- DSM/nDSM-assisted disambiguation: separate rooftops from ground surfaces
- Tile-based inference with stitch post-processing
- Per-feature confidence score (0.0–1.0)

### Layer 4 — GeoAI / Spatial Processing
- Raster-to-vector conversion (GDAL/Rasterio polygonization)
- Polygon simplification (Douglas-Peucker), regularization (right-angle correction for buildings)
- Minimum-area noise filtering (configurable threshold)
- Boundary network construction from building edges + road edges + DSM height discontinuities + existing GIS layers
- Polygonization: close boundary candidates into non-overlapping parcel polygons with full spatial coverage
- **Automated Topology Validation** — detect all 9 error types:
  1. Polygon Overlap (intersection analysis)
  2. Gap (coverage analysis)
  3. Sliver (area-perimeter ratio)
  4. Self-intersection (geometry validation)
  5. Duplicate geometry (hash comparison)
  6. Invalid polygon (OGC validity check)
  7. Unclosed boundary (ring closure check)
  8. Misalignment (snap tolerance analysis)
  9. Inconsistent relationships (spatial relationship rules)
- Classify each error: Critical / Warning / Info
- Auto-suggest corrections for simple errors; require human approval before applying
- Flag ambiguous errors for expert review only — no auto-correction of Critical errors

### Layer 5 — Application Layer (Web-GIS)
Full browser-based GIS. No desktop GIS software required. See Frontend section for full UI spec.

### Layer 6 — Outputs
- Topology-validated parcel polygons (PostGIS + export files)
- Building footprint layer
- Road and pathway network layer (width-based classification)
- Land-use classification layer
- Confidence heatmap raster
- Topology validation report
- Verification and audit report per parcel
- Encroachment detection report
- Change detection report
- Export formats: Shapefile, GeoPackage, GeoJSON, PDF, ULPIN-compatible CSV

---

## Technology Stack

| Category | Technology |
|---|---|
| AI Language | Python 3.10+ |
| AI Framework | PyTorch |
| Vision | OpenCV |
| Segmentation | U-Net / DeepLabV3+ / Mask R-CNN |
| Object Detection | YOLOv8 |
| Metrics | scikit-learn, torchmetrics |
| Raster | GDAL, Rasterio |
| Vector | GeoPandas, Shapely |
| Coordinate Transform | pyproj, Fiona |
| Spatial Database | PostgreSQL 15+ + PostGIS 3+ |
| Backend API | FastAPI |
| Async Tasks | Celery + Redis |
| Frontend | React + TypeScript |
| Web Mapping | MapLibre GL JS |
| UI Components | Tailwind CSS + Lucide React |
| Containerization | Docker + Docker Compose |

---

## AI Models — Pre-Trained Weights (No Training Required)

**Do not train any model from scratch.** Use the following pre-trained weights directly. They work on drone/satellite imagery out of the box and are sufficient for the prototype to demonstrate a complete end-to-end pipeline.

| Model | Library / Source | Pre-trained On | How to Load |
|---|---|---|---|
| U-Net (semantic segmentation) | `segmentation-models-pytorch` — `smp.Unet(encoder_name="resnet34", encoder_weights="imagenet")` | ImageNet | `pip install segmentation-models-pytorch` |
| DeepLabV3+ (semantic segmentation) | `smp.DeepLabV3Plus(encoder_name="resnet50", encoder_weights="imagenet")` | ImageNet | same library |
| Mask R-CNN (instance segmentation) | `torchvision.models.detection.maskrcnn_resnet50_fpn(weights="DEFAULT")` | COCO | built into torchvision |
| YOLOv8 (object detection) | `ultralytics` — `YOLO("yolov8n.pt")` or `YOLO("yolov8s.pt")` | COCO | `pip install ultralytics` |

**Key point:** The pre-trained encoders already understand edges, textures, and shapes well enough to segment buildings and roads from drone imagery without fine-tuning. Results won't be perfect — that is expected for a prototype. The confidence scoring system accounts for model uncertainty.

**Ground Truth feedback loop** (future, not in prototype): once field-verified parcel data accumulates in the platform, those verified geometries become training examples to fine-tune the models. This is a post-prototype concern — do not implement automated retraining in the prototype.
| GPU | NVIDIA CUDA / cuDNN |
| Auth | JWT (python-jose) |

---

## Data Models

### Parcel
```
parcel_id: UUID
ulpin: varchar(14)           -- auto-generated ULPIN-format ID
geometry: MultiPolygon       -- PostGIS, target CRS
area_sqm: float
perimeter_m: float
coverage_type: enum (Urban, Rural, PeriUrban, Mixed)
land_use_class: enum (Residential, Commercial, Institutional, Industrial, Open, Transportation, WaterBody)
confidence_score: float      -- 0.0 to 1.0
topology_status: enum (Valid, HasWarnings, HasErrors)
validation_status: enum (Pending, InReview, Approved, Rejected)
gt_status: enum (Pending, InProgress, Completed, Verified)
dispute_risk_score: int       -- 0 to 100
dispute_risk_factors: jsonb
created_at: timestamp
updated_at: timestamp
created_by: user_id
approved_by: user_id (nullable)
```

### Building Footprint
```
building_id: UUID
geometry: Polygon
parcel_id: UUID (FK, nullable)
height_m: float (from nDSM, nullable)
confidence_score: float
is_flagged: boolean           -- true if roof != ground footprint suspected
```

### Encroachment Flag
```
encroachment_flag_id: UUID
parcel_id: UUID (FK)
building_id: UUID (FK, nullable)
flag_type: enum (PossibleEncroachment, UnauthorizedConstruction, BoundaryMismatch, NeedsVerification)
overlap_area_sqm: float
confidence: float
status: enum (Open, UnderReview, Resolved, Dismissed)
resolved_by: user_id (nullable)
resolved_at: timestamp (nullable)
notes: text (nullable)
```

### Topology Error
```
error_id: UUID
feature_id: UUID
error_type: enum (Overlap, Gap, Sliver, SelfIntersection, Duplicate, InvalidPolygon, UnclosedBoundary, Misalignment, InconsistentRelationship)
severity: enum (Critical, Warning, Info)
description: text
suggested_correction: text (nullable)
status: enum (Open, AutoCorrected, HumanCorrected, Dismissed)
```

### Change Record
```
change_record_id: UUID
parcel_id: UUID
change_type: enum (NewParcel, Deleted, BoundaryChanged, LandUseChanged, BuildingAdded, BuildingDemolished)
epoch_before: timestamp
epoch_after: timestamp
geometry_before: MultiPolygon (nullable)
geometry_after: MultiPolygon (nullable)
attribute_diff: jsonb
detected_at: timestamp
```

### Parcel Version
```
parcel_version_id: UUID
parcel_id: UUID (FK)
version_number: int
geometry_snapshot: MultiPolygon
attributes_snapshot: jsonb
changed_by: user_id
changed_at: timestamp
change_reason: text
approved_by: user_id (nullable)
```

### User
```
user_id: UUID
username: string
email: string
role: enum (Viewer, Editor, Reviewer, Administrator)
```

### Audit Log
```
log_id: UUID
user_id: UUID
action: enum (Edit, Approve, Reject, Export, ModelRun, GTUpload, Rollback, EncroachmentResolved)
feature_id: UUID (nullable)
timestamp: timestamp
details: jsonb
```

---

## API Endpoints (FastAPI)

### Auth
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

### Data Ingestion
- `POST /api/v1/data/upload`
- `GET /api/v1/data/jobs/{job_id}`

### Pipeline
- `POST /api/v1/pipeline/run`
- `GET /api/v1/pipeline/status/{job_id}`
- `GET /api/v1/pipeline/logs/{job_id}`

### Parcels
- `GET /api/v1/parcels` — filters: bbox, confidence range, status, land-use, gt_status, coverage_type
- `GET /api/v1/parcels/{parcel_id}`
- `PUT /api/v1/parcels/{parcel_id}` — Editor+ role
- `POST /api/v1/parcels/{parcel_id}/approve` — Reviewer+ role
- `POST /api/v1/parcels/{parcel_id}/reject`
- `GET /api/v1/parcels/{parcel_id}/history`
- `POST /api/v1/parcels/{parcel_id}/rollback/{version_id}` — Reviewer+ role

### Topology
- `GET /api/v1/topology/errors`
- `POST /api/v1/topology/run`
- `PUT /api/v1/topology/errors/{error_id}/resolve`

### Encroachments
- `GET /api/v1/encroachments`
- `PUT /api/v1/encroachments/{flag_id}/resolve`

### Ground Truthing
- `POST /api/v1/groundtruth/upload`
- `GET /api/v1/groundtruth/priority-list`
- `PUT /api/v1/groundtruth/{parcel_id}/status`

### Change Detection
- `POST /api/v1/changedetection/run`
- `GET /api/v1/changedetection/results/{job_id}`
- `GET /api/v1/changedetection/report/{job_id}/download`

### Map Tiles
- `GET /api/v1/tiles/imagery/{z}/{x}/{y}`
- `GET /api/v1/tiles/parcels/{z}/{x}/{y}`
- `GET /api/v1/tiles/confidence/{z}/{x}/{y}`

### Export
- `POST /api/v1/export`
- `GET /api/v1/export/{export_id}/download`

### Public (no auth)
- `GET /api/v1/public/parcel/{ulpin}` — citizen lookup by ULPIN ID
- `GET /api/v1/public/parcel/search?q=` — search by address or village name

---

## Frontend Pages & UI Spec

All pages use the AAKAR Design System defined above. White background, Inter font, Lucide icons, Tailwind CSS.

---

### 1. Login Page
- Centered card (max-width 400px) on white background
- AAKAR logo top-center (simple wordmark: "AAKAR" in `--accent`, subtitle "Ministry of Rural Development · DoLR" in `--text-muted`)
- Email + password fields, "Sign in" primary button
- No register link (admin creates users)
- Error state: red border on field + toast notification

---

### 2. Dashboard (Home)
Top bar: AAKAR logo left, username + role badge right, logout icon.
Left sidebar (260px): navigation links with Lucide icons.

**8 KPI Cards (2×4 grid):**
Each card: white background, `--border` border, 12px radius, icon top-left in accent color, large number, label below.
1. **Hectares Processed** — total area run through AI pipeline
2. **Time Saved vs Manual** — `Y%` computed from `(manual_baseline - AI_time) / manual_baseline * 100`
3. **GT Effort Reduced** — `Z%` fewer field visits via confidence prioritization
4. **Topology Health** — `N% parcels topology-valid`
5. **Encroachment Flags** — `N open` in danger color if > 0
6. **Dispute Risk Parcels** — `N high-risk` awaiting mandatory review
7. **ULPIN-Ready Parcels** — `N approved parcels with ULPIN IDs`
8. **Changes Detected** — `N` since last epoch

**System Comparison Table** (below KPI cards):
Full-width white card. Table header in `--bg-subtle`. Feature column left-aligned, system columns centered.
Columns: Feature | NAKSHA | SVAMITVA | Bhu-Aadhaar | AAKAR
AAKAR column cells: green checkmark badge "Yes" for all rows.
Other columns: gray "No" or amber "Partial" badges.

**Recent Activity Feed** (right side panel):
Last 10 audit log entries. Each row: action icon, description, user name, time ago.

---

### 3. Map View (Main Web-GIS)
Full-screen layout. MapLibre GL JS base map (Carto Positron light tiles for background clarity).

**Left Sidebar (260px):**
- Layer toggles (each with eye icon): Drone Imagery | Parcel Boundaries | Building Footprints | Road Network | Land-Use Classification | Confidence Heatmap | Existing GIS Overlay | Encroachment Flags
- Layer opacity slider per layer
- Filter panel: confidence range slider, validation status checkboxes, land-use class multi-select, GT status checkboxes, coverage type radio

**Right Panel (360px, slides in on parcel click):**
Parcel Inspector:
- Parcel ID (monospace, copyable) + ULPIN (monospace, copyable)
- Confidence score: large number + colored progress bar
- Dispute risk score: colored badge (green/amber/red)
- Land-use class badge
- Coverage type badge (Urban/Rural/Peri-Urban/Mixed)
- Area (sqm), Perimeter (m)
- GT status badge + GT action button
- Topology status badge + "View errors" link
- Encroachment flag count (if any) + "View flags" link
- Validation status badge
- Action buttons: Edit Geometry | Approve | Reject | View History
- Approval requires Reviewer role; button is disabled + tooltip shown for lower roles

**Map Controls (top-right, white card):**
- Zoom in/out
- Fit to area
- Toggle satellite/light base map
- Draw mode (for manual boundary edits)

**Confidence heatmap** rendered as a semi-transparent raster overlay using `--map-high-conf`, `--map-mid-conf`, `--map-low-conf` fills at 20% opacity.

**Encroachment flag layer**: red fill at 30% opacity on flagged parcels, red stroke 2px.

---

### 4. Parcel Timeline View (modal or dedicated page)
Opens from "View History" in the Parcel Inspector.
- Vertical timeline: each version is a node (version number, changed by, changed at, change reason)
- Click a version: show attribute diff as a two-column table (before | after), highlight changed cells in amber
- Geometry diff: mini map showing before (gray outline) vs after (blue outline)
- "Rollback to this version" button (Reviewer+ only) — shows confirmation modal

---

### 5. Topology Errors Page
Full-page table.
- Columns: Severity badge | Error Type | Affected Parcel ID | Description | Suggested Fix | Status | Actions
- Filters top bar: severity multi-select, error type multi-select, status filter
- Click a row: zoom to parcel on map in a mini map preview on the right
- "Resolve" button per row: opens modal to accept suggestion or enter custom fix note

---

### 6. Encroachments Page
Full-page table.
- Columns: Flag Type badge | Parcel ID | Building ID | Overlap Area (sqm) | Confidence | Status | Actions
- Summary cards at top: total open flags, by type (4 mini cards)
- Click row: opens side panel with mini map showing parcel boundary vs building footprint overlap
- "Resolve" / "Dismiss" actions

---

### 7. Ground Truthing Page
Two panels:

**Left — Priority Queue:**
Sorted list of parcels by confidence ascending (lowest first).
Each row: parcel ID, confidence badge, GT status badge, land-use, area, GPS coordinates (centroid lat/lon for field navigation), "Mark In Progress" button.

**Right — GT Upload:**
Drag-and-drop zone for GT field data (GeoJSON or Shapefile).
After upload: show matched vs unmatched parcel count, confidence score updates preview.

**GT Efficiency Widget (top):**
Shows `GT_reduction_%` + estimated field visits saved vs uniform approach.

---

### 8. Pipeline Control Page
- "Run AI Pipeline" button (admin/reviewer only) — opens modal to select area/project and configure parameters (tile size, overlap, confidence threshold)
- Active pipeline jobs: progress bar per job, stage name, ETA
- Past runs: table with date, area, duration, status, parcels generated, "View logs" link
- Log viewer: scrollable monospace text panel, auto-scroll toggle

---

### 9. Data Upload Page
Stepper UI (3 steps):
1. **Select Data Type** — card grid: Drone Imagery | ORI | DSM | DTM | GIS Parcel Layer | Ground Truth Data | GNSS Points
2. **Upload File** — drag-and-drop zone, show file name + size, validate format and CRS client-side before upload
3. **Confirm & Ingest** — show summary table (file, type, CRS detected, size), "Start Ingestion" button, progress indicator

---

### 10. Change Detection Page
- Two dataset selectors (dropdown: available processed datasets by date)
- "Run Change Detection" button
- Results: color-coded map overlay (green = new, red = deleted, orange = modified)
- Summary panel: count by change type (6 mini cards)
- Change records table: Change Type | Parcel ID | Before Date | After Date | Details
- "Download Change Report" button (PDF + GeoJSON)

---

### 11. Export Page
- Area selector (draw on mini map or enter parcel ID range)
- Format checkboxes: Shapefile | GeoPackage | GeoJSON | ULPIN CSV | PDF Report
- Status filter: export only Approved parcels (default) or include Pending
- "Request Export" button — shows progress, then "Download" button when ready
- Export history table: date, format, area, parcels count, download link

---

### 12. Admin Page (Administrator role only)
- User table: name, email, role badge, created date, actions (Edit Role, Deactivate)
- "Invite User" button: opens modal with email + role selector
- System settings: manual baseline hours/hectare (used for KPI calculations), confidence threshold presets
- Audit log full view: all actions, all users, filterable by action type, user, date range

---

### 13. Citizen Parcel Lookup (Public — no login)
Separate public route `/lookup`. No sidebar, no nav.
- AAKAR logo top-center, tagline below
- Search bar: "Enter ULPIN ID or village/address" — large, centered, rounded
- Results: parcel boundary on MapLibre map (read-only), attribute card below:
  - ULPIN ID (monospace), land-use class, area (sqm), validation status, last approved date
- "Download Parcel Summary PDF" button
- Intentionally NOT shown: owner name, financial data, dispute risk, internal confidence, encroachment flags

---

## ULPIN ID Generation Logic

For every parcel that reaches Approved status, auto-generate a 14-character ULPIN:

```
Format: [ST][DT][TK][VL][SEQN]
ST   = 2-char state code      (e.g., "MH" for Maharashtra)
DT   = 2-char district code   (numeric, e.g., "07")
TK   = 2-char taluka code     (numeric, e.g., "03")
VL   = 4-char village code    (numeric, e.g., "0012")
SEQN = 4-char sequential      (numeric, zero-padded, e.g., "0001")

Example: MH070300120001
```

- Store state/district/taluka/village as project-level metadata (admin sets on project creation)
- Sequential number auto-increments per village scope
- Centroid lat/lon of the approved parcel geometry stored as ULPIN geo-anchor
- ULPIN-CSV export columns: `ulpin, centroid_lat, centroid_lon, state, district, taluka, village, area_sqm, land_use, approved_date`

---

## Confidence Scoring Logic

Compute per parcel, store contributing factors in `dispute_risk_factors` jsonb:

1. **Base** = AI model softmax probability for predicted class
2. **Downward adjustments:**
   - Ambiguous model predictions (multiple overlapping outputs): −0.15
   - nDSM indicates roof-ground mismatch: −0.10
   - Existing GIS boundary offset > 2m: −0.10
   - Image quality flag (blur/shadow/occlusion) on tile: −0.10
   - Topology error detected: −0.15
3. **Upward adjustments:**
   - AI prediction aligns with existing GIS boundary (< 0.5m offset): +0.10
   - Multiple data sources agree: +0.05
   - GT data confirms boundary: +0.20
4. Final score clamped to [0.0, 1.0]

**Confidence tiers:**
- High ≥ 0.85: green badge "High Confidence", desktop review only
- Medium 0.50–0.84: amber badge "Verify", targeted field check recommended
- Low < 0.50: red badge "Field Required", priority field verification required

---

## Dispute Risk Scoring Logic

Compute per parcel on every update, store in `dispute_risk_score` (0–100) and `dispute_risk_factors` jsonb:

| Condition | Score Added |
|---|---|
| Encroachment flag present | +40 |
| Topology error on this parcel | +15 |
| Confidence score < 0.50 | +20 |
| Boundary offset vs. existing GIS record > 2m average | +15 |
| Multiple owner records linked to same geometry in GT data | +10 |

**Risk tiers:**
- High ≥ 60: red badge "High Risk", mandatory human review before approval allowed
- Medium 30–59: amber badge "Review Suggested"
- Low < 30: green badge "Low Risk"

---

## Encroachment Detection Logic

Run automatically after AI pipeline completes, if existing GIS parcel layer is present:

1. For each AI-extracted building footprint:
   - Intersect with existing registered parcel boundary
   - If building extends outside the parcel boundary AND overlap_area > threshold (configurable, default 2 sqm): flag as `PossibleEncroachment`
2. For each existing registered parcel with land_use = Open or Undeveloped:
   - Check if any building footprint exists within it
   - If yes: flag as `UnauthorizedConstruction`
3. For each parcel where AI boundary differs from GIS boundary by > configurable threshold:
   - Flag as `BoundaryMismatch`
4. Unresolved ambiguous cases: flag as `NeedsVerification`

---

## Pipeline Execution Order

```
[Files Uploaded via Data Upload Page]
         ↓
[Layer 1: Validation & Ingestion → PostGIS]
         ↓
[Layer 2: Preprocessing → Tiles prepared, nDSM computed]
         ↓
[Layer 3: AI Inference — Celery workers, GPU-accelerated]
    ├── Semantic segmentation (buildings, roads, land-use)
    ├── Instance segmentation (individual building footprints)
    ├── Object detection (YOLOv8 initial scan)
    └── Boundary candidate prediction
         ↓
[Layer 4: GeoAI Spatial Processing]
    ├── Raster → Vector conversion
    ├── Polygon simplification + regularization
    ├── Boundary network construction
    ├── Polygonization (closed parcel polygons)
    ├── Topology validation (all 9 error types)
    ├── Encroachment detection (if existing GIS layer present)
    ├── Confidence scoring per feature
    └── Dispute risk scoring per parcel
         ↓
[All results stored in PostGIS]
         ↓
[Layer 5: Web-GIS — Map View available immediately]
    ├── Expert reviews, edits, validates
    ├── GT data uploaded and integrated
    ├── ULPIN auto-generated on Approve
    └── Parcel version history saved on every edit
         ↓
[Layer 6: Export / Change Detection / Public Lookup]
```

---

## Project Structure

```
aakar/
├── backend/
│   ├── app/
│   │   ├── api/           -- FastAPI routers (parcels, topology, encroachments, etc.)
│   │   ├── models/        -- SQLAlchemy ORM + PostGIS column types
│   │   ├── schemas/       -- Pydantic request/response schemas
│   │   ├── services/      -- Business logic (pipeline, topology, encroachment, ULPIN, export)
│   │   ├── tasks/         -- Celery tasks (inference, preprocessing, change detection)
│   │   └── core/          -- Config, auth (JWT), DB session, middleware
│   ├── ai_pipeline/
│   │   ├── preprocessing/ -- Tiling, normalization, CRS alignment, nDSM
│   │   ├── models/        -- U-Net, Mask R-CNN, YOLOv8 wrappers
│   │   ├── inference/     -- Tile inference, stitching, prediction merge
│   │   ├── postprocessing/ -- Polygonization, simplification, regularization
│   │   ├── topology/      -- 9-error topology validation engine
│   │   ├── confidence/    -- Confidence scoring + dispute risk scoring
│   │   └── encroachment/  -- Encroachment detection logic
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/         -- All 13 pages
│   │   ├── components/    -- MapView, ParcelInspector, KPICard, ComparisonTable, etc.
│   │   ├── hooks/         -- useParcel, usePipeline, useAuth, useMapLayers
│   │   ├── api/           -- Typed API client (axios + react-query)
│   │   ├── store/         -- Zustand global state
│   │   └── types/         -- TypeScript interfaces for all data models
│   ├── public/
│   │   └── aakar-logo.svg
│   ├── Dockerfile
│   ├── tailwind.config.ts -- Configure all --token colors as Tailwind custom colors
│   └── package.json
├── nginx/
│   └── nginx.conf         -- Reverse proxy: / → frontend, /api → backend
├── docker-compose.yml
└── README.md
```

---

## docker-compose.yml Services

- `db` — PostgreSQL 15 + PostGIS 3 — port 5432
- `redis` — Redis 7 — port 6379
- `backend` — FastAPI — port 8000
- `worker` — Celery worker (GPU-enabled if CUDA available, falls back to CPU)
- `frontend` — React (Vite build) served via Nginx — port 80
- `nginx` — Reverse proxy — port 80 exposed externally

All services connected via internal Docker network. No service ports exposed except nginx port 80.

---

## Constraints

- Every AI output is a **preliminary result only**. No AI-generated feature becomes a final cadastral record without Reviewer-role human approval.
- Critical-severity topology errors block parcel approval until resolved. Implement an approval gate that checks for open Critical errors before allowing the approve action.
- High Dispute Risk (score ≥ 60) blocks parcel approval until a Reviewer explicitly overrides and documents a reason.
- Every edit, approval, rejection, and export is logged in the audit trail.
- All spatial data in a consistent CRS. Default: EPSG:4326. Support reprojection to state CRS on export.
- Tile-based processing — single tiles that fail are logged and skipped, other tiles continue.
- No proprietary software dependency (no ArcGIS, ERDAS, QGIS Server required).
- Exported Shapefiles include all companion files (.shp, .shx, .dbf, .prj).
- Role gates: Viewers read only, Editors cannot approve, Reviewers cannot manage users, Admins have full access.

---

## Competitive Positioning — AAKAR vs Existing Systems

| Feature | NAKSHA | SVAMITVA | Bhu-Aadhaar | **AAKAR** |
|---|---|---|---|---|
| Urban coverage | Yes | No | Yes (ID only) | **Yes** |
| Rural coverage | No | Yes | Yes (ID only) | **Yes** |
| AI auto-extraction | No | No | No | **Yes** |
| Automated topology validation | No | No | No | **Yes** |
| Confidence scoring | No | No | No | **Yes** |
| Encroachment detection | No | No | No | **Yes** |
| Change detection between epochs | No | No | No | **Yes** |
| Dispute risk scoring | No | No | No | **Yes** |
| Parcel version history | No | No | No | **Yes** |
| ULPIN-compatible ID generation | Partial | No | Yes | **Yes** |
| Citizen parcel lookup portal | No | No | No | **Yes** |
| Confidence-based GT prioritization | No | No | No | **Yes** |
| Open-source, no proprietary GIS | Partial | Partial | Partial | **Yes** |

Build this table as a live interactive component on the Dashboard. It is a core part of the AAKAR pitch.

---

## Success Criteria

The prototype is complete when all pass:

1. A GeoTIFF drone image uploads, processes through the AI pipeline, and produces parcel polygon GeoJSON
2. All 9 topology error types are detected and shown on the Topology Errors page
3. Every parcel has a confidence score and dispute risk score
4. The Map View renders parcel boundaries, confidence heatmap, building footprints, and encroachment flag layer
5. A Reviewer-role user can approve a parcel — ULPIN is auto-generated on approval
6. Encroachment detection runs automatically when existing GIS parcel layer is present
7. High-risk parcels (score ≥ 60) block approval until explicitly overridden with a documented reason
8. Parcel version history is viewable via Parcel Timeline View
9. Change detection produces a downloadable change report for two dataset versions
10. Citizen Parcel Lookup returns parcel boundary + attributes by ULPIN ID — no login required
11. The System Comparison table and all 8 KPI widgets are live on the Dashboard
12. Approved parcels export as GeoPackage with ULPIN-compatible IDs
13. All actions appear in the Audit Log on the Admin page
14. The full system starts via `docker-compose up` with no manual configuration
15. Every page follows the AAKAR Design System: white background, Inter font, accent `#2563EB`, Lucide icons, no placeholder text
