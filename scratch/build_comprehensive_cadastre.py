import json
import math
from PIL import Image, ImageDraw

nw_lat, nw_lon = 18.38711, 74.02176
se_lat, se_lon = 18.38190, 74.02725

def ll(px, py):
    lon = nw_lon + (px / 1024.0) * (se_lon - nw_lon)
    lat = nw_lat - (py / 1024.0) * (nw_lat - se_lat)
    return [round(lon, 5), round(lat, 5)]

def to_px(lon, lat):
    px = ((lon - nw_lon) / (se_lon - nw_lon)) * 1024.0
    py = ((nw_lat - lat) / (nw_lat - se_lat)) * 1024.0
    return (int(round(px)), int(round(py)))

# Define all 48 parcels with pixel definitions (xmin, ymin, xmax, ymax) or arbitrary polygons
# Grouped by village section:

parcels_def = []

def add_box_parcel(pid, ulpin, x1, y1, x2, y2, land_use, name, conf=0.95, top_status="Valid", val_status="Approved", gt="Verified", drs=10, factors=None):
    coords = [ll(x1, y1), ll(x2, y1), ll(x2, y2), ll(x1, y2), ll(x1, y1)]
    # calculate area in sqm approx (0.56m per pixel)
    w_m = (x2 - x1) * 0.56
    h_m = (y2 - y1) * 0.56
    area = round(w_m * h_m, 1)
    peri = round(2 * (w_m + h_m), 1)
    lats = [c[1] for c in coords]
    lons = [c[0] for c in coords]
    clat = round(sum(lats) / len(lats), 6)
    clon = round(sum(lons) / len(lons), 6)
    
    parcels_def.append({
        "parcel_id": pid,
        "ulpin": ulpin,
        "name": name,
        "coords": coords,
        "area_sqm": area,
        "perimeter_m": peri,
        "centroid_lat": clat,
        "centroid_lon": clon,
        "coverage_type": "Rural",
        "land_use_class": land_use,
        "confidence_score": conf,
        "topology_status": top_status,
        "validation_status": val_status,
        "gt_status": gt,
        "dispute_risk_score": drs,
        "dispute_risk_factors": factors or {"confidence_tier": "High", "dispute_tier": "Low", "dispute_factors": []},
        "created_by": "u-admin-01",
        "approved_by": "u-reviewer-01" if val_status == "Approved" else None,
        "px_box": (x1, y1, x2, y2)
    })

# 1. CORE GAOTHAN RESIDENTIAL & CIVIC (Mandir & West)
add_box_parcel("p-saswad-101", "MH251200104101", 340, 340, 375, 375, "Rural Residential (Abadi)", "Koli Homestead (Stone Masonry Roof)", 0.96)
add_box_parcel("p-saswad-102", "MH251200104102", 375, 340, 415, 375, "Rural Residential (Abadi)", "Jadhav Pucca House & Gotha", 0.94)
add_box_parcel("p-saswad-103", "MH251200104103", 265, 335, 340, 380, "Gram Panchayat Common Land", "Bhairavnath Mandir & Sabha Mandap", 0.98, drs=8)
add_box_parcel("p-saswad-104", "MH251200104104", 200, 335, 265, 380, "Rural Residential (Abadi)", "Shinde Ancestral Wada & Courtyard", 0.93)
add_box_parcel("p-saswad-105", "MH251200104105", 130, 335, 200, 380, "Rural Residential (Abadi)", "Patil Wada (Residential & Cattle Shed)", 0.92)
add_box_parcel("p-saswad-106", "MH251200104106", 130, 280, 200, 335, "Rural Residential (Abadi)", "Jagtap Pucca House", 0.95)
add_box_parcel("p-saswad-107", "MH251200104107", 200, 280, 265, 335, "Rural Residential (Abadi)", "Pawar Family Homestead", 0.94)
add_box_parcel("p-saswad-108", "MH251200104108", 265, 280, 335, 335, "Rural Residential (Abadi)", "Gaikwad Residence & Verandah", 0.96)
add_box_parcel("p-saswad-109", "MH251200104109", 335, 280, 375, 335, "Gram Panchayat Common Land", "Gram Panchayat Kacheri & Chawdi", 0.97, drs=6)
add_box_parcel("p-saswad-110", "MH251200104110", 375, 280, 415, 335, "Gram Panchayat Common Land", "Dive Seva Sahakari Vikas Sanstha", 0.95)

# 2. EASTERN GAOTHAN & SCHOOL WARD
add_box_parcel("p-saswad-004", None, 340, 220, 415, 280, "Gram Panchayat Common Land", "Zilla Parishad Primary School & Grounds", 0.45, top_status="HasErrors", val_status="Pending", gt="Pending", drs=75, factors={
    "confidence_tier": "Low",
    "dispute_tier": "High",
    "dispute_factors": [
        {"factor": "Vertex self-intersection at northwest school playground boundary", "points": 40},
        {"factor": "Low AI segmentation confidence score (< 0.50)", "points": 20},
        {"factor": "Unregistered pathway easement dispute logged with Gram Panchayat", "points": 15}
    ]
})
add_box_parcel("p-saswad-111", "MH251200104111", 415, 280, 475, 335, "Gram Panchayat Common Land", "Anganwadi & Arogya Upakendra", 0.96)
add_box_parcel("p-saswad-112", "MH251200104112", 475, 280, 535, 335, "Rural Residential (Abadi)", "Chavan Homestead & Courtyard", 0.94)
add_box_parcel("p-saswad-113", "MH251200104113", 535, 280, 600, 335, "Rural Residential (Abadi)", "Kamble Pucca Residence", 0.93)
add_box_parcel("p-saswad-115", "MH251200104115", 415, 335, 475, 390, "Rural Residential (Abadi)", "Thorat Ancestral Wada", 0.95)
add_box_parcel("p-saswad-116", "MH251200104116", 475, 335, 535, 390, "Rural Residential (Abadi)", "Bhosle Residence & Shop", 0.92)
add_box_parcel("p-saswad-117", "MH251200104117", 535, 335, 600, 390, "Rural Residential (Abadi)", "Kadam Homestead", 0.94)
add_box_parcel("p-saswad-118", "MH251200104118", 415, 220, 475, 280, "Rural Residential (Abadi)", "Mane Family Dwelling", 0.95)
add_box_parcel("p-saswad-119", "MH251200104119", 475, 220, 535, 280, "Rural Residential (Abadi)", "Ghadge Residence", 0.93)
add_box_parcel("p-saswad-120", "MH251200104120", 535, 220, 600, 280, "Rural Residential (Abadi)", "More Pucca House", 0.96)

# 3. NORTH GAOTHAN (Nava Vasti & Upper Settlement)
add_box_parcel("p-saswad-009", "MH251200107000", 415, 160, 510, 220, "Gram Panchayat Common Land", "Nava Vasti Panchayat Plot", 0.92)
add_box_parcel("p-saswad-122", "MH251200104122", 340, 160, 415, 220, "Rural Residential (Abadi)", "Nava Vasti Residential Plot 1", 0.93)
add_box_parcel("p-saswad-123", "MH251200104123", 265, 160, 340, 220, "Rural Residential (Abadi)", "Nava Vasti Residential Plot 2", 0.94)
add_box_parcel("p-saswad-124", "MH251200104124", 200, 160, 265, 220, "Rural Residential (Abadi)", "Nava Vasti Residential Plot 3", 0.91)
add_box_parcel("p-saswad-125", "MH251200104125", 130, 160, 200, 220, "Rural Residential (Abadi)", "Northern Settlement House 4", 0.90)
add_box_parcel("p-saswad-126", "MH251200104126", 130, 90, 230, 160, "Rural Residential (Abadi)", "North Hillside Homestead", 0.92)
add_box_parcel("p-saswad-127", "MH251200104127", 230, 90, 330, 160, "Rural Residential (Abadi)", "Upper Gaothan Stone Dwelling", 0.94)
add_box_parcel("p-saswad-128", "MH251200104128", 330, 90, 430, 160, "Gram Panchayat Common Land", "Upper Hanuman Mandir & Chhatri", 0.97)
add_box_parcel("p-saswad-129", "MH251200104129", 430, 90, 530, 160, "Rural Residential (Abadi)", "Northeast Habitation Block", 0.91)

# 4. VILLAGE MAIN STREET / COMMERCIAL BAZAAR CORRIDOR
add_box_parcel("p-saswad-130", "MH251200104130", 300, 380, 340, 435, "Rural Residential (Abadi)", "Dive Kirana & Provision Stores", 0.96)
add_box_parcel("p-saswad-131", "MH251200104131", 340, 375, 375, 425, "Rural Residential (Abadi)", "Krishi Seva Kendra Depot", 0.95)
add_box_parcel("p-saswad-132", "MH251200104132", 375, 375, 415, 415, "Rural Residential (Abadi)", "Dive Dudh Utpadak Sahakari Dairy", 0.97)
add_box_parcel("p-saswad-133", "MH251200104133", 415, 380, 455, 420, "Rural Residential (Abadi)", "Laxmi Flour Mill (Atta Chakki)", 0.94)
add_box_parcel("p-saswad-134", "MH251200104134", 455, 380, 500, 415, "Rural Residential (Abadi)", "Sanjivani Medical & General Store", 0.95)

# 5. WATER BODIES & COMMONS
add_box_parcel("p-saswad-008", "MH251200105000", 510, 160, 620, 240, "Water Body", "Gaothan Talav (Community Water Reservoir)", 0.94)
add_box_parcel("p-saswad-212", "MH251200105001", 600, 240, 750, 350, "Gram Panchayat Common Land", "Village Pasture & Gairan Common Land", 0.92)
add_box_parcel("p-saswad-213", "MH251200105002", 750, 240, 920, 350, "Agricultural (Dry)", "East Buffer Fallow Agricultural Land", 0.89)
add_box_parcel("p-saswad-214", "MH251200105003", 0, 335, 130, 480, "Agricultural (Irrigated)", "West Gaothan Fruit Orchard & Borewell", 0.93)
add_box_parcel("p-saswad-215", "MH251200105004", 0, 160, 130, 335, "Agricultural (Irrigated)", "Northwest Agricultural Gateway", 0.91)

# 6. SURROUNDING AGRICULTURAL GAT PARCELS (South & East)
add_box_parcel("p-saswad-005", "MH251200104001", 230, 435, 380, 490, "Agricultural (Irrigated)", "Gat No. 101/1 (Irrigated Sugarcane & Drip)", 0.94)
add_box_parcel("p-saswad-006", "MH251200104002", 380, 415, 470, 480, "Agricultural (Irrigated)", "Gat No. 101/2 (Farm Pumphouse with Road Setback Intrusion)", 0.88, drs=28, factors={
    "confidence_tier": "High", "dispute_tier": "Low",
    "dispute_factors": [{"factor": "Pumphouse roof eave projects 1.2m into road corridor setback", "points": 28}]
})
add_box_parcel("p-saswad-007", None, 470, 400, 580, 480, "Agricultural (Irrigated)", "Gat No. 103 (High Dispute Onion & Wheat Plot)", 0.48, top_status="HasErrors", val_status="Pending", gt="Pending", drs=65, factors={
    "confidence_tier": "Low", "dispute_tier": "High",
    "dispute_factors": [
        {"factor": "Historical revenue boundary discrepancy vs Talab buffer", "points": 40},
        {"factor": "Low AI confidence score (< 0.50)", "points": 25}
    ]
})
add_box_parcel("p-saswad-201", "MH251200104201", 580, 375, 720, 480, "Agricultural (Irrigated)", "Gat No. 104 (Pomegranate Orchard & Well)", 0.93)
add_box_parcel("p-saswad-202", "MH251200104202", 720, 355, 870, 480, "Agricultural (Irrigated)", "Gat No. 105 (Guava & Fig Plantation)", 0.92)
add_box_parcel("p-saswad-203", "MH251200104203", 90, 480, 230, 620, "Agricultural (Irrigated)", "Gat No. 106 (Southwest Fertile Farm)", 0.94)
add_box_parcel("p-saswad-204", "MH251200104204", 230, 490, 380, 620, "Agricultural (Irrigated)", "Gat No. 107 (Sugarcane & Jowar Field)", 0.95)
add_box_parcel("p-saswad-205", "MH251200104205", 380, 480, 510, 620, "Agricultural (Irrigated)", "Gat No. 108 (Irrigated Vegetable Plot)", 0.93)
add_box_parcel("p-saswad-206", "MH251200104206", 510, 480, 680, 620, "Agricultural (Irrigated)", "Gat No. 109 (Farmland with Farmhouse)", 0.94)
add_box_parcel("p-saswad-207", "MH251200104207", 180, 620, 380, 770, "Agricultural (Irrigated)", "Gat No. 110 (Deep South Agricultural Field)", 0.92)
add_box_parcel("p-saswad-208", "MH251200104208", 380, 620, 560, 770, "Agricultural (Dry)", "Gat No. 111 (South Fodder & Cattle Grazing)", 0.90)
add_box_parcel("p-saswad-209", "MH251200104209", 560, 620, 750, 770, "Agricultural (Irrigated)", "Gat No. 112 (Southern Outskirts Farm)", 0.91)
add_box_parcel("p-saswad-210", "MH251200104210", 240, 770, 460, 930, "Agricultural (Dry)", "Gat No. 113 (Far South Agricultural Boundary)", 0.89)
add_box_parcel("p-saswad-211", "MH251200104211", 460, 770, 700, 930, "Agricultural (Irrigated)", "Gat No. 114 (South Canal Buffer Orchard)", 0.93)

print(f'Total parcels generated: {len(parcels_def)}')

# BUILDINGS: Define building footprint nested inside each parcel
buildings_def = []

def add_bldg(bid, pid, name, x1, y1, x2, y2, height=3.8, conf=0.95, flagged=False, notes=None):
    coords = [ll(x1, y1), ll(x2, y1), ll(x2, y2), ll(x1, y2), ll(x1, y1)]
    buildings_def.append({
        "building_id": bid,
        "parcel_id": pid,
        "name": name,
        "geometry": {"type": "Polygon", "coordinates": [coords]},
        "height_m": height,
        "confidence_score": conf,
        "is_flagged": flagged,
        "notes": notes,
        "px_box": (x1, y1, x2, y2)
    })

# Core Mandir & West
add_bldg("b-saswad-101", "p-saswad-101", "Koli Homestead (Stone Masonry Roof)", 346, 346, 368, 368, 4.2, 0.96)
add_bldg("b-saswad-102", "p-saswad-102", "Jadhav Pucca House & Gotha", 382, 346, 408, 368, 3.8, 0.94)
add_bldg("b-saswad-103", "p-saswad-103", "Bhairavnath Mandir (Historic Saffron Sanctum)", 275, 344, 310, 370, 6.8, 0.98)
add_bldg("b-saswad-104", "p-saswad-104", "Shinde Old Wada Dwelling", 212, 344, 252, 370, 4.5, 0.93)
add_bldg("b-saswad-105-res", "p-saswad-105", "Patil Wada Main Residence", 142, 344, 188, 370, 4.2, 0.92)
add_bldg("b-saswad-106", "p-saswad-106", "Jagtap Stone Dwelling", 145, 290, 185, 325, 3.6, 0.95)
add_bldg("b-saswad-107", "p-saswad-107", "Pawar Homestead & Cattle Shed", 212, 290, 252, 325, 3.8, 0.94)
add_bldg("b-saswad-108", "p-saswad-108", "Gaikwad Residence", 278, 290, 322, 325, 4.0, 0.96)
add_bldg("b-saswad-109", "p-saswad-109", "Gram Panchayat Administrative Bhavan", 342, 290, 368, 325, 5.2, 0.97)
add_bldg("b-saswad-110", "p-saswad-110", "Dive Seva Sahakari Office Building", 382, 290, 408, 325, 4.8, 0.95)

# School & East Ward
add_bldg("b-saswad-114", "p-saswad-004", "Zilla Parishad Primary School Building", 355, 235, 400, 268, 4.8, 0.95)
add_bldg("b-saswad-111", "p-saswad-111", "Anganwadi & Arogya Upakendra Centre", 425, 292, 465, 325, 4.0, 0.96)
add_bldg("b-saswad-112", "p-saswad-112", "Chavan House & Cattle Shed", 485, 292, 525, 325, 3.6, 0.94)
add_bldg("b-saswad-113", "p-saswad-113", "Kamble Pucca Dwelling", 545, 292, 590, 325, 3.8, 0.93)
add_bldg("b-saswad-115", "p-saswad-115", "Thorat Wada Residential Wing", 425, 345, 465, 380, 4.5, 0.95)
add_bldg("b-saswad-116", "p-saswad-116", "Bhosle House & Corner Shop", 485, 345, 525, 380, 3.8, 0.92)
add_bldg("b-saswad-117", "p-saswad-117", "Kadam Family Homestead", 545, 345, 590, 380, 3.6, 0.94)
add_bldg("b-saswad-118", "p-saswad-118", "Mane Family House", 425, 230, 465, 270, 3.5, 0.95)
add_bldg("b-saswad-119", "p-saswad-119", "Ghadge Residence", 485, 230, 525, 270, 3.8, 0.93)
add_bldg("b-saswad-120", "p-saswad-120", "More Pucca House", 545, 230, 590, 270, 4.0, 0.96)

# North Gaothan / Nava Vasti
add_bldg("b-saswad-121", "p-saswad-009", "Nava Vasti Community Shed", 430, 175, 490, 205, 3.4, 0.92)
add_bldg("b-saswad-122", "p-saswad-122", "Nava Vasti House 1", 355, 175, 400, 205, 3.6, 0.93)
add_bldg("b-saswad-123", "p-saswad-123", "Nava Vasti House 2", 280, 175, 325, 205, 3.5, 0.94)
add_bldg("b-saswad-124", "p-saswad-124", "Nava Vasti House 3", 215, 175, 252, 205, 3.4, 0.91)
add_bldg("b-saswad-125", "p-saswad-125", "Northern Settlement Dwelling 4", 145, 175, 185, 205, 3.2, 0.90)
add_bldg("b-saswad-126", "p-saswad-126", "North Hillside Homestead", 150, 105, 210, 145, 3.6, 0.92)
add_bldg("b-saswad-127", "p-saswad-127", "Upper Gaothan Stone Dwelling", 250, 105, 310, 145, 3.8, 0.94)
add_bldg("b-saswad-128", "p-saswad-128", "Upper Hanuman Mandir", 360, 105, 400, 145, 5.0, 0.97)

# Bazaar Street Shops
add_bldg("b-saswad-130", "p-saswad-130", "Dive Kirana Store Building", 310, 390, 335, 425, 3.8, 0.96)
add_bldg("b-saswad-131", "p-saswad-131", "Krishi Seva Kendra Retail Depot", 348, 385, 370, 415, 3.6, 0.95)
add_bldg("b-saswad-132", "p-saswad-132", "Dive Dudh Dairy Chilling Unit", 382, 385, 408, 410, 4.2, 0.97)
add_bldg("b-saswad-133", "p-saswad-133", "Laxmi Flour Mill Machine Room", 422, 388, 448, 415, 3.5, 0.94)
add_bldg("b-saswad-134", "p-saswad-134", "Medical Store & Clinic", 462, 388, 492, 410, 3.6, 0.95)

# Farm Pumphouses & Encroachment Demo
add_bldg("b-saswad-105", "p-saswad-006", "Farm Pumphouse & Shed (Roof Edge Intrusion)", 405, 412, 435, 435, 3.4, 0.89, flagged=True, notes="Roof eaves extend 1.2m across survey boundary into Dive village road corridor setback")
add_bldg("b-saswad-204", "p-saswad-204", "Gat 107 Well Pumphouse & Tractor Shed", 270, 520, 320, 555, 3.5, 0.94)
add_bldg("b-saswad-206", "p-saswad-206", "Gat 109 Farmer Residence & Barn", 560, 510, 620, 550, 4.0, 0.93)

print(f'Total building footprints generated: {len(buildings_def)}')

# ROADS
roads_def = [
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
encroachments_def = [
    {
        "encroachment_flag_id": "enc-001",
        "parcel_id": "p-saswad-006",
        "building_id": "b-saswad-105",
        "flag_type": "PossibleEncroachment",
        "overlap_area_sqm": 12.8,
        "confidence": 0.89,
        "status": "Open",
        "notes": "Farm storage roof eaves of b-saswad-105 project 1.2m across northern survey boundary into Saswad-Purandar road corridor setback."
    },
    {
        "encroachment_flag_id": "enc-002",
        "parcel_id": "p-saswad-007",
        "building_id": None,
        "flag_type": "BoundaryMismatch",
        "overlap_area_sqm": 8.5,
        "confidence": 0.91,
        "status": "InReview",
        "notes": "Minor field bund alignment discrepancy with high water mark of adjacent Talav buffer."
    },
    {
        "encroachment_flag_id": "enc-003",
        "parcel_id": "p-saswad-004",
        "building_id": None,
        "flag_type": "UnauthorizedConstruction",
        "overlap_area_sqm": 18.2,
        "confidence": 0.86,
        "status": "Open",
        "notes": "Temporary cattle enclosure barrier erected along school perimeter pathway without Gram Panchayat sanction."
    },
    {
        "encroachment_flag_id": "enc-004",
        "parcel_id": "p-saswad-204",
        "building_id": "b-saswad-204",
        "flag_type": "NeedsVerification",
        "overlap_area_sqm": 5.4,
        "confidence": 0.88,
        "status": "Open",
        "notes": "Borewell pumphouse overhang near irrigation channel boundary requiring field verification."
    }
]

# Export verification image
im = Image.open('C:/Users/study/.gemini/antigravity-ide/brain/78de7bc3-810f-4631-a008-a63aa98a1aa9/scratch/survey_grid.jpg')
draw = ImageDraw.Draw(im)

# Draw roads
for r in roads_def:
    pts = [to_px(c[0], c[1]) for c in r["coords"]]
    draw.line(pts, fill='#F59E0B', width=5)

# Draw parcels
for p in parcels_def:
    pts = [to_px(c[0], c[1]) for c in p["coords"]]
    color = '#10B981' if 'Residential' in p['land_use_class'] else ('#3B82F6' if 'Agricultural' in p['land_use_class'] else '#F59E0B')
    draw.polygon(pts, outline=color, width=2)

# Draw buildings
for b in buildings_def:
    pts = [to_px(c[0], c[1]) for c in b["geometry"]["coordinates"][0]]
    color = '#EF4444' if b['is_flagged'] else '#8B5CF6'
    draw.polygon(pts, outline=color, width=2)

im.save('C:/Users/study/.gemini/antigravity-ide/brain/78de7bc3-810f-4631-a008-a63aa98a1aa9/scratch/expanded_village_overlay.jpg')
print('Overlay image saved to scratch/expanded_village_overlay.jpg')
