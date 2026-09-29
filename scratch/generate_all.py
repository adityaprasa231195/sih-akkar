import os
import json
import math
from datetime import datetime, timedelta

nw_lat, nw_lon = 18.38711, 74.02176
se_lat, se_lon = 18.38190, 74.02725

def ll(px, py):
    lon = nw_lon + (px / 1024.0) * (se_lon - nw_lon)
    lat = nw_lat - (py / 1024.0) * (nw_lat - se_lat)
    return [round(lon, 5), round(lat, 5)]

parcels = []
aliases = {}

def add_p(pid, ulpin, x1, y1, x2, y2, land_use, name, conf=0.95, top="Valid", val="Approved", gt="Verified", drs=10, factors=None):
    coords = [ll(x1, y1), ll(x2, y1), ll(x2, y2), ll(x1, y2), ll(x1, y1)]
    w_m = (x2 - x1) * 0.56
    h_m = (y2 - y1) * 0.56
    area = round(w_m * h_m, 1)
    peri = round(2 * (w_m + h_m), 1)
    lats = [c[1] for c in coords]
    lons = [c[0] for c in coords]
    clat = round(sum(lats) / len(lats), 6)
    clon = round(sum(lons) / len(lons), 6)
    
    p = {
        "parcel_id": pid,
        "ulpin": ulpin,
        "name": name,
        "geometry": {
            "type": "Polygon",
            "coordinates": [coords]
        },
        "area_sqm": area,
        "perimeter_m": peri,
        "centroid_lat": clat,
        "centroid_lon": clon,
        "coverage_type": "Rural",
        "land_use_class": land_use,
        "confidence_score": conf,
        "topology_status": top,
        "validation_status": val,
        "gt_status": gt,
        "dispute_risk_score": drs,
        "dispute_risk_factors": factors or {"confidence_tier": "High", "dispute_tier": "Low", "dispute_factors": []},
        "created_at": "2026-09-20T10:00:00Z",
        "updated_at": "2026-09-29T11:20:00Z",
        "created_by": "u-admin-01",
        "approved_by": "u-reviewer-01" if val == "Approved" else None
    }
    parcels.append(p)
    aliases[pid] = name

# Foreign-key referenced core parcels
add_p("p-saswad-001", "MH251200103001", 130, 20, 230, 90, "Agricultural (Irrigated)", "Gat No. 99 (North Valley Orchard)", 0.95)
add_p("p-saswad-002", "MH251200103002", 230, 20, 330, 90, "Agricultural (Dry)", "Gat No. 100/1 (Terraced Jowar Field)", 0.94)
add_p("p-saswad-003", "MH251200103003", 330, 20, 430, 90, "Gram Panchayat Common Land", "Gat No. 100/2 (North Village Gairan)", 0.91)

# Core Mandir & Western Gaothan
add_p("p-saswad-101", "MH251200104101", 340, 340, 375, 375, "Rural Residential (Abadi)", "Dive Gaothan 101 (Koli Homestead & Wada)", 0.96)
add_p("p-saswad-102", "MH251200104102", 375, 340, 415, 375, "Rural Residential (Abadi)", "Dive Gaothan 102 (Jadhav Pucca House & Gotha)", 0.94)
add_p("p-saswad-103", "MH251200104103", 265, 335, 340, 380, "Gram Panchayat Common Land", "Dive Gaothan 103 (Bhairavnath Mandir Sanctum)", 0.98, drs=8)
add_p("p-saswad-104", "MH251200104104", 200, 335, 265, 380, "Rural Residential (Abadi)", "Dive Gaothan 104 (Shinde Ancestral Wada)", 0.93)
add_p("p-saswad-105", "MH251200104105", 130, 335, 200, 380, "Rural Residential (Abadi)", "Dive Gaothan 105 (Patil Wada Residence)", 0.92)
add_p("p-saswad-106", "MH251200104106", 130, 280, 200, 335, "Rural Residential (Abadi)", "Dive Gaothan 106 (Jagtap Pucca House)", 0.95)
add_p("p-saswad-107", "MH251200104107", 200, 280, 265, 335, "Rural Residential (Abadi)", "Dive Gaothan 107 (Pawar Family Homestead)", 0.94)
add_p("p-saswad-108", "MH251200104108", 265, 280, 335, 335, "Rural Residential (Abadi)", "Dive Gaothan 108 (Gaikwad Residence)", 0.96)
add_p("p-saswad-109", "MH251200104109", 335, 280, 375, 335, "Gram Panchayat Common Land", "Dive Gaothan 109 (Gram Panchayat & Chawdi)", 0.97, drs=6)
add_p("p-saswad-110", "MH251200104110", 375, 280, 415, 335, "Gram Panchayat Common Land", "Dive Gaothan 110 (Dive Seva Sahakari Sanstha)", 0.95)

# Eastern Gaothan & School Ward
add_p("p-saswad-004", None, 340, 220, 415, 280, "Gram Panchayat Common Land", "Dive Gaothan 104 (Z.P. Primary School & Grounds)", 0.45, top="HasErrors", val="Pending", gt="Pending", drs=75, factors={
    "confidence_tier": "Low", "dispute_tier": "High",
    "dispute_factors": [
        {"factor": "Vertex self-intersection at northwest school playground boundary", "points": 40},
        {"factor": "Low AI segmentation confidence score (< 0.50)", "points": 20},
        {"factor": "Unregistered pathway easement dispute logged with Gram Panchayat", "points": 15}
    ]
})
add_p("p-saswad-111", "MH251200104111", 415, 280, 475, 335, "Gram Panchayat Common Land", "Dive Gaothan 111 (Anganwadi & Arogya Kendra)", 0.96)
add_p("p-saswad-112", "MH251200104112", 475, 280, 535, 335, "Rural Residential (Abadi)", "Dive Gaothan 112 (Chavan Homestead)", 0.94)
add_p("p-saswad-113", "MH251200104113", 535, 280, 600, 335, "Rural Residential (Abadi)", "Dive Gaothan 113 (Kamble Pucca Residence)", 0.93)
add_p("p-saswad-115", "MH251200104115", 415, 335, 475, 390, "Rural Residential (Abadi)", "Dive Gaothan 115 (Thorat Ancestral Wada)", 0.95)
add_p("p-saswad-116", "MH251200104116", 475, 335, 535, 390, "Rural Residential (Abadi)", "Dive Gaothan 116 (Bhosle House & Corner Shop)", 0.92)
add_p("p-saswad-117", "MH251200104117", 535, 335, 600, 390, "Rural Residential (Abadi)", "Dive Gaothan 117 (Kadam Homestead)", 0.94)
add_p("p-saswad-118", "MH251200104118", 415, 220, 475, 280, "Rural Residential (Abadi)", "Dive Gaothan 118 (Mane Family Dwelling)", 0.95)
add_p("p-saswad-119", "MH251200104119", 475, 220, 535, 280, "Rural Residential (Abadi)", "Dive Gaothan 119 (Ghadge Residence)", 0.93)
add_p("p-saswad-120", "MH251200104120", 535, 220, 600, 280, "Rural Residential (Abadi)", "Dive Gaothan 120 (More Pucca House)", 0.96)

# North Gaothan (Nava Vasti)
add_p("p-saswad-009", "MH251200107000", 415, 160, 510, 220, "Gram Panchayat Common Land", "Dive Gaothan Nava Vasti Panchayat Plot", 0.92)
add_p("p-saswad-122", "MH251200104122", 340, 160, 415, 220, "Rural Residential (Abadi)", "Nava Vasti Residential Plot 1", 0.93)
add_p("p-saswad-123", "MH251200104123", 265, 160, 340, 220, "Rural Residential (Abadi)", "Nava Vasti Residential Plot 2", 0.94)
add_p("p-saswad-124", "MH251200104124", 200, 160, 265, 220, "Rural Residential (Abadi)", "Nava Vasti Residential Plot 3", 0.91)
add_p("p-saswad-125", "MH251200104125", 130, 160, 200, 220, "Rural Residential (Abadi)", "Nava Vasti Dwelling 4", 0.90)
add_p("p-saswad-126", "MH251200104126", 130, 90, 230, 160, "Rural Residential (Abadi)", "North Hillside Homestead", 0.92)
add_p("p-saswad-127", "MH251200104127", 230, 90, 330, 160, "Rural Residential (Abadi)", "Upper Gaothan Stone Dwelling", 0.94)
add_p("p-saswad-128", "MH251200104128", 330, 90, 430, 160, "Gram Panchayat Common Land", "Upper Hanuman Mandir", 0.97)
add_p("p-saswad-129", "MH251200104129", 430, 90, 530, 160, "Rural Residential (Abadi)", "Northeast Habitation Block", 0.91)

# Village Main Street / Bazaar Shops
add_p("p-saswad-130", "MH251200104130", 300, 380, 340, 435, "Rural Residential (Abadi)", "Dive Kirana & Provision Stores", 0.96)
add_p("p-saswad-131", "MH251200104131", 340, 375, 375, 425, "Rural Residential (Abadi)", "Krishi Seva Kendra Depot", 0.95)
add_p("p-saswad-132", "MH251200104132", 375, 375, 415, 415, "Rural Residential (Abadi)", "Dive Dudh Sahakari Dairy", 0.97)
add_p("p-saswad-133", "MH251200104133", 415, 380, 455, 420, "Rural Residential (Abadi)", "Laxmi Flour Mill (Atta Chakki)", 0.94)
add_p("p-saswad-134", "MH251200104134", 455, 380, 500, 415, "Rural Residential (Abadi)", "Sanjivani Pharmacy & Clinic", 0.95)

# Water Bodies & Commons
add_p("p-saswad-008", "MH251200105000", 510, 160, 620, 240, "Water Body", "Gat No. 105 (Dive Gaothan Talav / Pond)", 0.94)
add_p("p-saswad-212", "MH251200105001", 600, 240, 750, 350, "Gram Panchayat Common Land", "Village Pasture & Gairan Common Land", 0.92)
add_p("p-saswad-213", "MH251200105002", 750, 240, 920, 350, "Agricultural (Dry)", "East Buffer Fallow Agricultural Land", 0.89)
add_p("p-saswad-214", "MH251200105003", 0, 335, 130, 480, "Agricultural (Irrigated)", "West Gaothan Fruit Orchard & Well", 0.93)
add_p("p-saswad-215", "MH251200105004", 0, 160, 130, 335, "Agricultural (Irrigated)", "Northwest Agricultural Gateway", 0.91)

# Surrounding Agricultural Gat Parcels
add_p("p-saswad-005", "MH251200104001", 230, 435, 380, 490, "Agricultural (Irrigated)", "Gat No. 104/1 (Shinde Krishi Gat - Sugarcane)", 0.94)
add_p("p-saswad-006", "MH251200104002", 380, 415, 470, 480, "Agricultural (Irrigated)", "Gat No. 104/2 (Patil Krishi Gat - Encroachment Demo)", 0.88, drs=28, factors={
    "confidence_tier": "High", "dispute_tier": "Low",
    "dispute_factors": [{"factor": "Pumphouse roof eave projects 1.2m into road corridor setback", "points": 28}]
})
add_p("p-saswad-007", None, 470, 400, 580, 480, "Agricultural (Irrigated)", "Gat No. 104/3 (Babar Krishi Gat - Eastern Fields)", 0.48, top="HasErrors", val="Pending", gt="Pending", drs=65, factors={
    "confidence_tier": "Low", "dispute_tier": "High",
    "dispute_factors": [
        {"factor": "Historical revenue boundary discrepancy vs Talab buffer", "points": 40},
        {"factor": "Low AI confidence score (< 0.50)", "points": 25}
    ]
})
add_p("p-saswad-201", "MH251200104201", 580, 375, 720, 480, "Agricultural (Irrigated)", "Gat No. 108 (Pomegranate Orchard & Borewell)", 0.93)
add_p("p-saswad-202", "MH251200104202", 720, 355, 870, 480, "Agricultural (Irrigated)", "Gat No. 109 (Guava & Fig Plantation)", 0.92)
add_p("p-saswad-203", "MH251200104203", 90, 480, 230, 620, "Agricultural (Irrigated)", "Gat No. 110 (Southwest Fertile Farm)", 0.94)
add_p("p-saswad-204", "MH251200104204", 230, 490, 380, 620, "Agricultural (Irrigated)", "Gat No. 111 (Sugarcane & Jowar Field)", 0.95)
add_p("p-saswad-205", "MH251200104205", 380, 480, 510, 620, "Agricultural (Irrigated)", "Gat No. 112 (Irrigated Vegetable Plot)", 0.93)
add_p("p-saswad-206", "MH251200104206", 510, 480, 680, 620, "Agricultural (Irrigated)", "Gat No. 113 (Farmland with Farmhouse)", 0.94)
add_p("p-saswad-207", "MH251200104207", 180, 620, 380, 770, "Agricultural (Irrigated)", "Gat No. 114 (Deep South Agricultural Field)", 0.92)
add_p("p-saswad-208", "MH251200104208", 380, 620, 560, 770, "Agricultural (Dry)", "Gat No. 115 (South Fodder & Cattle Grazing)", 0.90)
add_p("p-saswad-209", "MH251200104209", 560, 620, 750, 770, "Agricultural (Irrigated)", "Gat No. 116 (Southern Outskirts Farm)", 0.91)
add_p("p-saswad-210", "MH251200104210", 240, 770, 460, 930, "Agricultural (Dry)", "Gat No. 117 (Far South Agricultural Boundary)", 0.89)
add_p("p-saswad-211", "MH251200104211", 460, 770, 700, 930, "Agricultural (Irrigated)", "Gat No. 118 (South Canal Buffer Orchard)", 0.93)

# BUILDINGS
buildings = []
def add_b(bid, pid, name, x1, y1, x2, y2, h=3.8, conf=0.95, flag=False, notes=None):
    coords = [ll(x1, y1), ll(x2, y1), ll(x2, y2), ll(x1, y2), ll(x1, y1)]
    buildings.append({
        "building_id": bid,
        "parcel_id": pid,
        "name": name,
        "geometry": {
            "type": "Polygon",
            "coordinates": [coords]
        },
        "height_m": h,
        "confidence_score": conf,
        "is_flagged": flag,
        "notes": notes
    })

# Mandir & Western Gaothan
add_b("b-saswad-101", "p-saswad-101", "Koli Homestead (Stone Masonry Roof)", 346, 346, 368, 368, 4.2, 0.96)
add_b("b-saswad-102", "p-saswad-102", "Jadhav Pucca House & Gotha", 382, 346, 408, 368, 3.8, 0.94)
add_b("b-saswad-103", "p-saswad-103", "Bhairavnath Mandir (Historic Saffron Sanctum)", 275, 344, 310, 370, 6.8, 0.98)
add_b("b-saswad-104", "p-saswad-104", "Shinde Old Wada Dwelling", 212, 344, 252, 370, 4.5, 0.93)
add_b("b-saswad-105-res", "p-saswad-105", "Patil Wada Main Residence", 142, 344, 188, 370, 4.2, 0.92)
add_b("b-saswad-106", "p-saswad-106", "Jagtap Stone Dwelling", 145, 290, 185, 325, 3.6, 0.95)
add_b("b-saswad-107", "p-saswad-107", "Pawar Homestead & Cattle Shed", 212, 290, 252, 325, 3.8, 0.94)
add_b("b-saswad-108", "p-saswad-108", "Gaikwad Residence", 278, 290, 322, 325, 4.0, 0.96)
add_b("b-saswad-109", "p-saswad-109", "Gram Panchayat Administrative Bhavan", 342, 290, 368, 325, 5.2, 0.97)
add_b("b-saswad-110", "p-saswad-110", "Dive Seva Sahakari Office Building", 382, 290, 408, 325, 4.8, 0.95)

# School & East Ward
add_b("b-saswad-114", "p-saswad-004", "Zilla Parishad Primary School Building", 355, 235, 400, 268, 4.8, 0.95)
add_b("b-saswad-111", "p-saswad-111", "Anganwadi & Arogya Upakendra Centre", 425, 292, 465, 325, 4.0, 0.96)
add_b("b-saswad-112", "p-saswad-112", "Chavan House & Cattle Shed", 485, 292, 525, 325, 3.6, 0.94)
add_b("b-saswad-113", "p-saswad-113", "Kamble Pucca Dwelling", 545, 292, 590, 325, 3.8, 0.93)
add_b("b-saswad-115", "p-saswad-115", "Thorat Wada Residential Wing", 425, 345, 465, 380, 4.5, 0.95)
add_b("b-saswad-116", "p-saswad-116", "Bhosle House & Corner Shop", 485, 345, 525, 380, 3.8, 0.92)
add_b("b-saswad-117", "p-saswad-117", "Kadam Family Homestead", 545, 345, 590, 380, 3.6, 0.94)
add_b("b-saswad-118", "p-saswad-118", "Mane Family House", 425, 230, 465, 270, 3.5, 0.95)
add_b("b-saswad-119", "p-saswad-119", "Ghadge Residence", 485, 230, 525, 270, 3.8, 0.93)
add_b("b-saswad-120", "p-saswad-120", "More Pucca House", 545, 230, 590, 270, 4.0, 0.96)

# North Gaothan / Nava Vasti
add_b("b-saswad-121", "p-saswad-009", "Nava Vasti Community Shed", 430, 175, 490, 205, 3.4, 0.92)
add_b("b-saswad-122", "p-saswad-122", "Nava Vasti House 1", 355, 175, 400, 205, 3.6, 0.93)
add_b("b-saswad-123", "p-saswad-123", "Nava Vasti House 2", 280, 175, 325, 205, 3.5, 0.94)
add_b("b-saswad-124", "p-saswad-124", "Nava Vasti House 3", 215, 175, 252, 205, 3.4, 0.91)
add_b("b-saswad-125", "p-saswad-125", "Northern Settlement Dwelling 4", 145, 175, 185, 205, 3.2, 0.90)
add_b("b-saswad-126", "p-saswad-126", "North Hillside Homestead", 150, 105, 210, 145, 3.6, 0.92)
add_b("b-saswad-127", "p-saswad-127", "Upper Gaothan Stone Dwelling", 250, 105, 310, 145, 3.8, 0.94)
add_b("b-saswad-128", "p-saswad-128", "Upper Hanuman Mandir", 360, 105, 400, 145, 5.0, 0.97)

# Bazaar Street Shops
add_b("b-saswad-130", "p-saswad-130", "Dive Kirana Store Building", 310, 390, 335, 425, 3.8, 0.96)
add_b("b-saswad-131", "p-saswad-131", "Krishi Seva Kendra Retail Depot", 348, 385, 370, 415, 3.6, 0.95)
add_b("b-saswad-132", "p-saswad-132", "Dive Dudh Dairy Chilling Unit", 382, 385, 408, 410, 4.2, 0.97)
add_b("b-saswad-133", "p-saswad-133", "Laxmi Flour Mill Machine Room", 422, 388, 448, 415, 3.5, 0.94)
add_b("b-saswad-134", "p-saswad-134", "Medical Store & Clinic", 462, 388, 492, 410, 3.6, 0.95)

# Farm Pumphouses & Encroachment Demo
add_b("b-saswad-105", "p-saswad-006", "Farm Pumphouse & Shed (Roof Edge Intrusion)", 405, 412, 435, 435, 3.4, 0.89, flag=True, notes="Roof eaves extend 1.2m across survey boundary into Dive village road corridor setback")
add_b("b-saswad-204", "p-saswad-204", "Gat 107 Well Pumphouse & Tractor Shed", 270, 520, 320, 555, 3.5, 0.94)
add_b("b-saswad-206", "p-saswad-206", "Gat 109 Farmer Residence & Barn", 560, 510, 620, 550, 4.0, 0.93)

# ROADS
roads = [
    {
        "name": "Pune-Saswad Dive Main Village Road",
        "width_m": 7.5,
        "surface": "Bituminous Paved Rural Highway",
        "coords": [
            ll(0, 510), ll(80, 495), ll(160, 480), ll(230, 465), ll(300, 435),
            ll(380, 415), ll(460, 400), ll(540, 390), ll(620, 375), ll(720, 355),
            ll(820, 335), ll(920, 315), ll(1024, 295)
        ]
    },
    {
        "name": "Central Gaothan Bazaar Lane (Gali No. 1)",
        "width_m": 4.0,
        "surface": "Concrete Paved Village Lane",
        "coords": [
            ll(380, 415), ll(380, 340), ll(380, 270), ll(370, 200), ll(360, 130), ll(350, 60)
        ]
    },
    {
        "name": "Bhairavnath Mandir Chowk Pathway",
        "width_m": 3.5,
        "surface": "Stone Paver Village Pathway",
        "coords": [
            ll(380, 340), ll(300, 345), ll(230, 350), ll(170, 355), ll(110, 360)
        ]
    },
    {
        "name": "ZP Primary School Access Lane",
        "width_m": 3.5,
        "surface": "Concrete Village Lane",
        "coords": [
            ll(380, 270), ll(460, 265), ll(540, 260), ll(620, 255), ll(700, 250)
        ]
    },
    {
        "name": "South Gat Farm Access Cart Track",
        "width_m": 4.0,
        "surface": "Unpaved Murrum Farm Track",
        "coords": [
            ll(460, 400), ll(460, 480), ll(470, 560), ll(480, 650), ll(500, 750), ll(520, 850), ll(540, 950)
        ]
    }
]

# ENCROACHMENTS
encroachments = [
    {
        "flag_id": "enc-001",
        "parcel_id": "p-saswad-006",
        "building_id": "b-saswad-105",
        "flag_type": "PossibleEncroachment",
        "overlap_area_sqm": 12.8,
        "confidence": 0.89,
        "description": "Farm storage roof eaves of b-saswad-105 project 1.2m across northern survey boundary into Dive village road corridor setback.",
        "coords": [
            ll(412, 410), ll(430, 408), ll(432, 413), ll(414, 414), ll(412, 410)
        ]
    },
    {
        "flag_id": "enc-002",
        "parcel_id": "p-saswad-007",
        "building_id": None,
        "flag_type": "BoundaryMismatch",
        "overlap_area_sqm": 8.5,
        "confidence": 0.91,
        "description": "Minor field bund alignment discrepancy with high water mark of adjacent Talav buffer.",
        "coords": [
            ll(570, 400), ll(585, 400), ll(585, 415), ll(570, 415), ll(570, 400)
        ]
    },
    {
        "flag_id": "enc-003",
        "parcel_id": "p-saswad-004",
        "building_id": None,
        "flag_type": "UnauthorizedConstruction",
        "overlap_area_sqm": 18.2,
        "confidence": 0.86,
        "description": "Temporary cattle enclosure barrier erected along school perimeter pathway without Gram Panchayat sanction.",
        "coords": [
            ll(405, 230), ll(420, 230), ll(420, 245), ll(405, 245), ll(405, 230)
        ]
    },
    {
        "flag_id": "enc-004",
        "parcel_id": "p-saswad-204",
        "building_id": "b-saswad-204",
        "flag_type": "NeedsVerification",
        "overlap_area_sqm": 5.4,
        "confidence": 0.88,
        "description": "Borewell pumphouse overhang near irrigation channel boundary requiring field verification.",
        "coords": [
            ll(315, 520), ll(325, 520), ll(325, 532), ll(315, 532), ll(315, 520)
        ]
    }
]

print(f"Generated {len(parcels)} parcels, {len(buildings)} buildings, {len(roads)} roads, {len(encroachments)} encroachments.")

# 1. WRITE FRONTEND CADASTRAL DATA FILE
fe_path = "AAKAR/frontend/src/data/cadastralData.ts"

buildings_fc = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "building_id": b["building_id"],
                "parcel_id": b["parcel_id"],
                "name": b["name"],
                "height_m": b["height_m"],
                "confidence_score": b["confidence_score"],
                "is_flagged": b["is_flagged"],
                **({"notes": b["notes"]} if b.get("notes") else {})
            },
            "geometry": b["geometry"]
        }
        for b in buildings
    ]
}

roads_fc = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": r["name"],
                "width_m": r["width_m"],
                "surface": r["surface"]
            },
            "geometry": {
                "type": "LineString",
                "coordinates": r["coords"]
            }
        }
        for r in roads
    ]
}

enc_fc = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "flag_id": e["flag_id"],
                "parcel_id": e["parcel_id"],
                "flag_type": e["flag_type"],
                "overlap_area_sqm": e["overlap_area_sqm"],
                "description": e["description"]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [e["coords"]]
            }
        }
        for e in encroachments
    ]
}

fe_parcels = [{k: v for k, v in p.items() if k != "name"} for p in parcels]

with open(fe_path, "w", encoding="utf-8") as f:
    f.write("import { Parcel } from '../types';\n\n")
    f.write(f"export const PUNE_CADASTRAL_DATA: Parcel[] = {json.dumps(fe_parcels, indent=2)};\n\n")
    f.write(f"export const RURAL_PARCEL_ALIASES: Record<string, string> = {json.dumps(aliases, indent=2)};\n\n")
    f.write(f"export const PUNE_BUILDINGS_GEOJSON: any = {json.dumps(buildings_fc, indent=2)};\n\n")
    f.write(f"export const PUNE_ROADS_GEOJSON: any = {json.dumps(roads_fc, indent=2)};\n\n")
    f.write(f"export const PUNE_ENCROACHMENTS_GEOJSON: any = {json.dumps(enc_fc, indent=2)};\n")

print(f"Wrote frontend data to {fe_path}")

# 2. WRITE BACKEND SEED DATA FILE
be_path = "AAKAR/backend/app/seed_data.py"

with open(be_path, "w", encoding="utf-8") as f:
    f.write('''import uuid
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import (
    User, Parcel, BuildingFootprint, EncroachmentFlag, TopologyError, ChangeRecord, ParcelVersion, AuditLog
)
from app.core.security import get_password_hash

def seed_database(db: Session, force: bool = False):
    first_p = db.query(Parcel).filter(Parcel.parcel_id == "p-saswad-101").first()
    # Check if up-to-date with 50+ parcels
    parcel_count = db.query(Parcel).count()
    if not force and first_p and parcel_count >= 50 and abs(first_p.centroid_lat - 18.3853) < 0.002:
        return

    # Clear outdated cadastral entities before reseeding
    db.query(AuditLog).delete()
    db.query(ParcelVersion).delete()
    db.query(ChangeRecord).delete()
    db.query(TopologyError).delete()
    db.query(EncroachmentFlag).delete()
    db.query(BuildingFootprint).delete()
    db.query(Parcel).delete()
    db.commit()

    # 1. Users (insert only if missing)
    if db.query(User).first() is None:
        users = [
            User(
                user_id="u-admin-01",
                username="admin",
                email="admin@aakar.gov.in",
                hashed_password=get_password_hash("admin123"),
                role="Administrator"
            ),
            User(
                user_id="u-reviewer-01",
                username="reviewer",
                email="reviewer@aakar.gov.in",
                hashed_password=get_password_hash("reviewer123"),
                role="Reviewer"
            ),
            User(
                user_id="u-editor-01",
                username="editor",
                email="editor@aakar.gov.in",
                hashed_password=get_password_hash("editor123"),
                role="Editor"
            ),
            User(
                user_id="u-viewer-01",
                username="viewer",
                email="viewer@aakar.gov.in",
                hashed_password=get_password_hash("viewer123"),
                role="Viewer"
            )
        ]
        db.add_all(users)
        db.commit()

    # 2. Comprehensive Rural Cadastral Parcels
''')
    f.write(f'    parcels_data = json.loads({json.dumps(json.dumps(parcels))})\n\n')
    f.write('''    for p in parcels_data:
        parcel = Parcel(
            parcel_id=p["parcel_id"],
            ulpin=p["ulpin"],
            geometry=p["geometry"],
            area_sqm=p["area_sqm"],
            perimeter_m=p["perimeter_m"],
            centroid_lat=p["centroid_lat"],
            centroid_lon=p["centroid_lon"],
            coverage_type=p["coverage_type"],
            land_use_class=p["land_use_class"],
            confidence_score=p["confidence_score"],
            topology_status=p["topology_status"],
            validation_status=p["validation_status"],
            gt_status=p["gt_status"],
            dispute_risk_score=p["dispute_risk_score"],
            dispute_risk_factors=p["dispute_risk_factors"],
            created_by=p["created_by"],
            approved_by=p["approved_by"]
        )
        db.add(parcel)
    db.commit()

    # 3. Rural Building Footprints
''')
    f.write(f'    buildings_data = json.loads({json.dumps(json.dumps(buildings))})\n\n')
    f.write('''    for b in buildings_data:
        bldg = BuildingFootprint(
            building_id=b["building_id"],
            parcel_id=b["parcel_id"],
            geometry=b["geometry"],
            height_m=b["height_m"],
            confidence_score=b["confidence_score"],
            is_flagged=b["is_flagged"]
        )
        db.add(bldg)
    db.commit()

    # 4. Encroachment Flags
''')
    f.write(f'    encroachments_data = json.loads({json.dumps(json.dumps(encroachments))})\n\n')
    
    f.write('''    for e in encroachments_data:
        flag = EncroachmentFlag(
            encroachment_flag_id=e["flag_id"],
            parcel_id=e["parcel_id"],
            building_id=e.get("building_id"),
            flag_type=e["flag_type"],
            overlap_area_sqm=e["overlap_area_sqm"],
            confidence=e["confidence"],
            status="Open",
            notes=e["description"]
        )
        db.add(flag)
    db.commit()

    # 5. Topology Errors (All 9 OGC error types)
    topology_errors = [
        TopologyError(
            error_id="top-001",
            feature_id="p-saswad-004",
            error_type="Overlap",
            severity="Critical",
            description="Abadi boundary polygon overlaps adjacent school compound corridor.",
            suggested_correction="Clip polygon along surveyed shared stone-wall centerline node.",
            status="Open"
        ),
        TopologyError(
            error_id="top-002",
            feature_id="p-saswad-003",
            error_type="Gap",
            severity="Warning",
            description="2.1m unallocated gap between Gat 105 (Talav) and Gat 104/2 boundary.",
            suggested_correction="Extend common vertex to snap along the high flood line contour.",
            status="Open"
        ),
        TopologyError(
            error_id="top-003",
            feature_id="p-saswad-007",
            error_type="Sliver",
            severity="Warning",
            description="High aspect-ratio sliver fragment (compactness < 0.03) along village drainage nala.",
            suggested_correction="Dissolve sliver into adjacent Gram Panchayat common land.",
            status="Open"
        ),
        TopologyError(
            error_id="top-004",
            feature_id="p-saswad-004",
            error_type="SelfIntersection",
            severity="Critical",
            description="Bowtie vertex crossing at Abadi courtyard corner.",
            suggested_correction="Untangle loop by splitting into standard non-intersecting rings.",
            status="Open"
        ),
        TopologyError(
            error_id="top-005",
            feature_id="p-saswad-008",
            error_type="Duplicate",
            severity="Critical",
            description="Near-duplicate polygon ring detected from overlapping drone orthophoto flight strip.",
            suggested_correction="Consolidate duplicate geometries into primary feature ID.",
            status="Open"
        ),
        TopologyError(
            error_id="top-006",
            feature_id="p-saswad-007",
            error_type="InvalidPolygon",
            severity="Critical",
            description="OGC invalid geometry: interior water hole ring touches exterior pasture boundary.",
            suggested_correction="Apply zero-width buffer repair to reset exterior ring coordinates.",
            status="Open"
        ),
        TopologyError(
            error_id="top-007",
            feature_id="p-saswad-009",
            error_type="UnclosedBoundary",
            severity="Critical",
            description="Boundary coordinate sequence does not close cleanly on start point.",
            suggested_correction="Snap terminal coordinate to start point.",
            status="Open"
        ),
        TopologyError(
            error_id="top-008",
            feature_id="p-saswad-003",
            error_type="Misalignment",
            severity="Warning",
            description="Node vertex within 0.25m snap tolerance of adjacent Gramin Marg edge.",
            suggested_correction="Snap to common road right-of-way alignment.",
            status="Open"
        ),
        TopologyError(
            error_id="top-009",
            feature_id="p-saswad-005",
            error_type="InconsistentRelationship",
            severity="Info",
            description="Internal village pathway crosses parcel without easement servitude attribute.",
            suggested_correction="Tag right-of-way easement in cadastral metadata.",
            status="Open"
        )
    ]
    db.add_all(topology_errors)

    # 6. Change Records (Epoch comparison)
    change_records = [
        ChangeRecord(
            change_record_id="chg-001",
            parcel_id="p-saswad-001",
            change_type="BuildingAdded",
            epoch_before=datetime.utcnow() - timedelta(days=730),
            epoch_after=datetime.utcnow(),
            attribute_diff={"building_id": "b-saswad-101", "structure": "Stone Homestead", "height_m": 4.2},
            detected_at=datetime.utcnow() - timedelta(days=2)
        ),
        ChangeRecord(
            change_record_id="chg-002",
            parcel_id="p-saswad-002",
            change_type="LandUseChanged",
            epoch_before=datetime.utcnow() - timedelta(days=730),
            epoch_after=datetime.utcnow(),
            attribute_diff={"before": "Agricultural (Dry)", "after": "Agricultural (Irrigated)"},
            detected_at=datetime.utcnow() - timedelta(days=5)
        ),
        ChangeRecord(
            change_record_id="chg-003",
            parcel_id="p-saswad-003",
            change_type="BoundaryChanged",
            epoch_before=datetime.utcnow() - timedelta(days=730),
            epoch_after=datetime.utcnow(),
            attribute_diff={"area_delta_sqm": -28.4, "cause": "Talab desiltation embankment realignment"},
            detected_at=datetime.utcnow() - timedelta(days=7)
        ),
        ChangeRecord(
            change_record_id="chg-004",
            parcel_id="p-saswad-006",
            change_type="NewParcel",
            epoch_before=datetime.utcnow() - timedelta(days=730),
            epoch_after=datetime.utcnow(),
            attribute_diff={"origin": "SVAMITVA village Abadi demarcation for Gram Panchayat Bhawan"},
            detected_at=datetime.utcnow() - timedelta(days=12)
        )
    ]
    db.add_all(change_records)

    # 7. Parcel Versions
    versions = [
        ParcelVersion(
            parcel_version_id="ver-001",
            parcel_id="p-saswad-001",
            version_number=1,
            geometry_snapshot={"type": "Polygon", "coordinates": [[[74.0280, 18.3850], [74.0305, 18.3850], [74.0302, 18.3860], [74.0288, 18.3860], [74.0280, 18.3850]]]},
            attributes_snapshot={"land_use": "Agricultural (Irrigated)", "area_sqm": 3380.0},
            changed_by="system",
            changed_at=datetime.utcnow() - timedelta(days=15),
            change_reason="Initial automated AI segmentation from drone orthophoto",
            approved_by=None
        ),
        ParcelVersion(
            parcel_version_id="ver-002",
            parcel_id="p-saswad-001",
            version_number=2,
            geometry_snapshot={"type": "Polygon", "coordinates": [[[74.0280, 18.3850], [74.0305, 18.3850], [74.0302, 18.3860], [74.0288, 18.3860], [74.0280, 18.3850]]]},
            attributes_snapshot={"land_use": "Agricultural (Irrigated)", "area_sqm": 3450.0},
            changed_by="editor",
            changed_at=datetime.utcnow() - timedelta(days=4),
            change_reason="Adjusted field bund boundary to match CORS GNSS rovers",
            approved_by="reviewer"
        )
    ]
    db.add_all(versions)

    # 8. Audit Logs
    audit_logs = [
        AuditLog(
            log_id="log-001",
            user_id="u-admin-01",
            user_name="admin",
            action="ModelRun",
            feature_id="Dive_Village_Comprehensive_SVAMITVA_Survey",
            timestamp=datetime.utcnow() - timedelta(hours=36),
            details={"tiles_processed": 144, "parcels_generated": len(parcels_data), "runtime_sec": 58.4}
        ),
        AuditLog(
            log_id="log-002",
            user_id="u-editor-01",
            user_name="editor",
            action="Edit",
            feature_id="p-saswad-101",
            timestamp=datetime.utcnow() - timedelta(hours=28),
            details={"edit_type": "Abadi stone-wall adjustment", "delta_sqm": 12.0}
        ),
        AuditLog(
            log_id="log-003",
            user_id="u-reviewer-01",
            user_name="reviewer",
            action="Approve",
            feature_id="p-saswad-101",
            timestamp=datetime.utcnow() - timedelta(hours=20),
            details={"ulpin_assigned": "MH251200104101", "confidence": 0.96}
        ),
        AuditLog(
            log_id="log-004",
            user_id="u-editor-01",
            user_name="editor",
            action="GTUpload",
            feature_id="Dive_Village_CORS_Ground_Truth_Survey",
            timestamp=datetime.utcnow() - timedelta(hours=14),
            details={"matched_parcels": 48, "unmatched": 0, "crs": "EPSG:4326"}
        ),
        AuditLog(
            log_id="log-005",
            user_id="u-admin-01",
            user_name="admin",
            action="Export",
            feature_id="Dive_Approved_SVAMITVA_Parcels",
            timestamp=datetime.utcnow() - timedelta(hours=5),
            details={"formats": ["GeoJSON", "ULPIN_CSV", "Shapefile"], "parcels_exported": 45}
        )
    ]
    db.add_all(audit_logs)
    db.commit()
''')

print(f"Wrote backend seed script to {be_path}")
