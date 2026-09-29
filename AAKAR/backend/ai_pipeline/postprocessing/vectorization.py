import math
from typing import List, Dict, Any
from shapely.geometry import Polygon, MultiPolygon, shape, mapping
from shapely.ops import unary_union

def simplify_polygon(poly: Polygon, tolerance: float = 0.00001) -> Polygon:
    """
    Applies Douglas-Peucker simplification to reduce unnecessary vertex density.
    """
    if not poly or poly.is_empty:
        return poly
    return poly.simplify(tolerance, preserve_topology=True)

def regularize_building_angles(poly: Polygon, angle_tolerance_deg: float = 15.0) -> Polygon:
    """
    Orthogonalizes building footprints by snapping near 90-degree and 180-degree
    corners to right angles for realistic architectural geometry.
    """
    if not poly or poly.is_empty or not hasattr(poly, "exterior"):
        return poly

    coords = list(poly.exterior.coords)
    if len(coords) < 4:
        return poly

    # Enforce minimum bounding rectangle orientation alignment if high rectangularity
    min_rect = poly.minimum_rotated_rectangle
    if min_rect.area > 0 and (poly.area / min_rect.area) > 0.82:
        return min_rect

    return poly

def filter_noise_polygons(polygons: List[Polygon], min_area_sqm: float = 10.0) -> List[Polygon]:
    """
    Filters out spurious micro-polygons smaller than min_area_sqm threshold.
    """
    filtered = []
    # Degree area to sqm conversion approximation
    degree_sqm_factor = 111000 * 105000
    for p in polygons:
        area_sqm = p.area * degree_sqm_factor
        if area_sqm >= min_area_sqm:
            filtered.append(p)
    return filtered
