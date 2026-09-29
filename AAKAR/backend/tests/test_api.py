import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.database import SessionLocal
from app.seed_data import seed_database

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    db = SessionLocal()
    seed_database(db)
    db.close()

client = TestClient(app)

def test_root_health():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["app"] == "AAKAR"

def test_dashboard_kpis():
    res = client.get("/api/v1/dashboard/kpis")
    assert res.status_code == 200
    data = res.json()
    assert "time_saved_pct" in data
    assert "gt_effort_reduced_pct" in data
    assert "topology_health_pct" in data
    assert "open_encroachments" in data
    assert "high_dispute_risk_count" in data
    assert "ulpin_ready_count" in data

def test_parcels_list_and_filters():
    res = client.get("/api/v1/parcels")
    assert res.status_code == 200
    parcels = res.json()
    assert len(parcels) >= 9

    # Filter by confidence
    res_high = client.get("/api/v1/parcels?min_confidence=0.85")
    assert res_high.status_code == 200
    for p in res_high.json():
        assert p["confidence_score"] >= 0.85

def test_approval_gates():
    # Attempt approval on parcel with Critical topology errors
    res_fail = client.post("/api/v1/parcels/p-saswad-004/approve", json={"override_high_risk": False})
    assert res_fail.status_code == 400
    assert "unresolved Critical topology errors" in res_fail.json()["detail"]

    # Attempt approval on parcel with high dispute risk without override
    res_risk = client.post("/api/v1/parcels/p-saswad-007/approve", json={"override_high_risk": False})
    assert res_risk.status_code == 400

def test_topology_errors_all_nine_types():
    res = client.get("/api/v1/topology/errors")
    assert res.status_code == 200
    errors = res.json()
    error_types = {e["error_type"] for e in errors}
    expected = {
        "Overlap", "Gap", "Sliver", "SelfIntersection", "Duplicate",
        "InvalidPolygon", "UnclosedBoundary", "Misalignment", "InconsistentRelationship"
    }
    assert expected.issubset(error_types)

def test_encroachments_detection():
    res = client.get("/api/v1/encroachments")
    assert res.status_code == 200
    flags = res.json()
    assert len(flags) >= 4
    types = {f["flag_type"] for f in flags}
    assert "PossibleEncroachment" in types
    assert "UnauthorizedConstruction" in types

def test_ground_truth_prioritization():
    res = client.get("/api/v1/groundtruth/priority-list")
    assert res.status_code == 200
    data = res.json()
    assert "efficiency_metrics" in data
    assert data["efficiency_metrics"]["gt_effort_reduced_pct"] > 50.0
    parcels = data["parcels"]
    # Check lowest confidence is first
    assert parcels[0]["confidence_score"] <= parcels[-1]["confidence_score"]

def test_change_detection():
    res = client.post("/api/v1/changedetection/run")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Completed"
    assert "summary" in data

def test_export_shapefile_and_geojson():
    res = client.post("/api/v1/export", json={"formats": ["Shapefile", "GeoJSON"], "status_filter": "Approved"})
    assert res.status_code == 200
    data = res.json()
    assert "download_url" in data
    download_res = client.get(data["download_url"])
    assert download_res.status_code == 200
    assert download_res.headers["content-type"] == "application/zip"

def test_public_citizen_lookup():
    # Lookup by ULPIN without authentication
    res = client.get("/api/v1/public/parcel/MH251200104001")
    assert res.status_code == 200
    data = res.json()
    assert data["ulpin"] == "MH251200104001"
    assert "dispute_risk_score" not in data  # Privacy preserved
    assert "confidence_score" not in data    # Internal AI score hidden
