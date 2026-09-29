from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Parcel, BuildingFootprint, EncroachmentFlag

router = APIRouter(prefix="/tiles", tags=["tiles"])

@router.get("/layers")
def get_map_layers(db: Session = Depends(get_db)):
    parcels = db.query(Parcel).all()
    buildings = db.query(BuildingFootprint).all()
    encroachments = db.query(EncroachmentFlag).all()

    # Rural road network vectors for Gram Panchayat Dive, Purandar
    roads_fc = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Pune-Saswad Dive Main Village Road",
        "width_m": 7.5,
        "surface": "Bituminous Paved Rural Highway"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            74.02176,
            18.38452
          ],
          [
            74.02219,
            18.38459
          ],
          [
            74.02262,
            18.38467
          ],
          [
            74.02299,
            18.38474
          ],
          [
            74.02337,
            18.3849
          ],
          [
            74.0238,
            18.385
          ],
          [
            74.02423,
            18.38507
          ],
          [
            74.02466,
            18.38513
          ],
          [
            74.02508,
            18.3852
          ],
          [
            74.02562,
            18.3853
          ],
          [
            74.02616,
            18.38541
          ],
          [
            74.02669,
            18.38551
          ],
          [
            74.02725,
            18.38561
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Central Gaothan Bazaar Lane (Gali No. 1)",
        "width_m": 4.0,
        "surface": "Concrete Paved Village Lane"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            74.0238,
            18.385
          ],
          [
            74.0238,
            18.38538
          ],
          [
            74.0238,
            18.38574
          ],
          [
            74.02374,
            18.38609
          ],
          [
            74.02369,
            18.38645
          ],
          [
            74.02364,
            18.3868
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Bhairavnath Mandir Chowk Pathway",
        "width_m": 3.5,
        "surface": "Stone Paver Village Pathway"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            74.0238,
            18.38538
          ],
          [
            74.02337,
            18.38535
          ],
          [
            74.02299,
            18.38533
          ],
          [
            74.02267,
            18.3853
          ],
          [
            74.02235,
            18.38528
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "ZP Primary School Access Lane",
        "width_m": 3.5,
        "surface": "Concrete Village Lane"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            74.0238,
            18.38574
          ],
          [
            74.02423,
            18.38576
          ],
          [
            74.02466,
            18.38579
          ],
          [
            74.02508,
            18.38581
          ],
          [
            74.02551,
            18.38584
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "South Gat Farm Access Cart Track",
        "width_m": 4.0,
        "surface": "Unpaved Murrum Farm Track"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            74.02423,
            18.38507
          ],
          [
            74.02423,
            18.38467
          ],
          [
            74.02428,
            18.38426
          ],
          [
            74.02433,
            18.3838
          ],
          [
            74.02444,
            18.38329
          ],
          [
            74.02455,
            18.38279
          ],
          [
            74.02466,
            18.38228
          ]
        ]
      }
    }
  ]
}

    parcels_fc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": p.geometry,
                "properties": {
                    "parcel_id": p.parcel_id,
                    "ulpin": p.ulpin,
                    "area_sqm": p.area_sqm,
                    "perimeter_m": p.perimeter_m,
                    "land_use_class": p.land_use_class,
                    "coverage_type": p.coverage_type,
                    "confidence_score": p.confidence_score,
                    "validation_status": p.validation_status,
                    "topology_status": p.topology_status,
                    "gt_status": p.gt_status,
                    "dispute_risk_score": p.dispute_risk_score,
                    "dispute_risk_factors": p.dispute_risk_factors
                }
            }
            for p in parcels
        ]
    }

    buildings_fc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": b.geometry,
                "properties": {
                    "building_id": b.building_id,
                    "parcel_id": b.parcel_id,
                    "height_m": b.height_m,
                    "confidence_score": b.confidence_score,
                    "is_flagged": b.is_flagged
                }
            }
            for b in buildings
        ]
    }

    encroachments_fc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": next((p.geometry for p in parcels if p.parcel_id == e.parcel_id), None),
                "properties": {
                    "encroachment_flag_id": e.encroachment_flag_id,
                    "parcel_id": e.parcel_id,
                    "flag_type": e.flag_type,
                    "overlap_area_sqm": e.overlap_area_sqm,
                    "confidence": e.confidence,
                    "status": e.status,
                    "notes": e.notes
                }
            }
            for e in encroachments if e.status == "Open"
        ]
    }

    return {
        "parcels": parcels_fc,
        "buildings": buildings_fc,
        "roads": roads_fc,
        "encroachments": encroachments_fc
    }
