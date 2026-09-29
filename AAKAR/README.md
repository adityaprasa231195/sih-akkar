# AAKAR — AI-Based Automated Urban Parcel Mapping & Cadastral Feature Extraction
**"Mapping Every Corner of India"**

Ministry of Rural Development, Department of Land Resources (DoLR), Government of India.

---

## Overview

AAKAR automates the extraction of preliminary cadastral features (parcel boundaries, building footprints, road networks, land-use) from high-resolution drone imagery and elevation models (DSM/DTM). It generates topology-validated preliminary parcel maps and provides a Web-GIS dashboard for human-in-the-loop expert review, creating a unified platform that connects urban and rural land record workflows.

---

## System Architecture

1. **Layer 1 — Data Acquisition & Ingestion**: Validates GeoTIFF, ORI, DSM/DTM rasters, GIS vectors, and GNSS RTK checkpoints.
2. **Layer 2 — Preprocessing**: Tiling with configurable overlap, radiometric normalization, spatial co-registration to EPSG:4326, and nDSM computation (`nDSM = DSM - DTM`).
3. **Layer 3 — AI/ML Engine**: Semantic segmentation (PyTorch U-Net / DeepLabV3+), object detection (YOLOv8), and preliminary boundary prediction.
4. **Layer 4 — GeoAI Spatial Processing**:
   - Raster-to-vector polygonization, Douglas-Peucker simplification, and right-angle building regularization.
   - **Automated 9-Error Topology Validation Engine**:
     1. Polygon Overlap (intersection analysis)
     2. Gap (coverage analysis)
     3. Sliver (compactness / isoperimetric quotient)
     4. Self-intersection (ring self-crossings)
     5. Duplicate geometry (area coincidence)
     6. Invalid polygon (OGC checks)
     7. Unclosed boundary (ring closure)
     8. Misalignment (snap tolerance analysis < 0.3m)
     9. Inconsistent relationships (spatial containment rules)
   - **Confidence Scoring Engine**: Multi-factor adjustments clamped to [0.0, 1.0].
   - **Dispute Risk Engine**: Aggregates risk points (0–100) with approval gates for High Risk (≥ 60).
   - **Encroachment Detection**: Building intrusion detection and unauthorized construction flags on open land.
5. **Layer 5 — Application Layer (Web-GIS)**: Interactive map viewer, layer toggles, parcel inspection, version timeline rollback, and citizen lookup.
6. **Layer 6 — Dissemination & Outputs**: Shapefiles with companion files (.shp, .shx, .dbf, .prj), OGC GeoPackage, GeoJSON, and official 14-character ULPIN CSV registries.

---

## Quickstart

### Option 1: Docker Compose (Production Setup)

```bash
cd AAKAR
docker-compose up --build
```

Access services:
- **Web-GIS Application**: `http://localhost/`
- **Citizen Parcel Lookup**: `http://localhost/lookup`
- **FastAPI Documentation**: `http://localhost/docs`

### Option 2: Local Development Run

#### Backend (FastAPI):
```bash
cd AAKAR/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend (React + Vite):
```bash
cd AAKAR/frontend
npm install
npm run dev
```

---

## Test Credentials

| Role | Username | Password | Permissions |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full system access, invite users, system tuning |
| **Reviewer** | `reviewer` | `reviewer123` | Human-in-the-loop parcel approvals, ULPIN generation, rollback |
| **Editor** | `editor` | `editor123` | Geometry edits, attribute updates, GT data uploads |
| **Viewer** | `viewer` | `viewer123` | Read-only inspection of cadastral layers |

---

## Automated Verification Tests

To run the automated verification suite:

```bash
cd AAKAR/backend
pytest tests/test_api.py -v
```

All 10 test suites evaluate the 15 prototype success criteria including approval gates, topology validation, and ULPIN generation.
