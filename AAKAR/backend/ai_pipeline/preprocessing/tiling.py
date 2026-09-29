import numpy as np
from typing import List, Tuple, Dict, Any

def compute_ndsm(dsm_raster: np.ndarray, dtm_raster: np.ndarray) -> np.ndarray:
    """
    Computes normalized Digital Surface Model:
    nDSM = DSM - DTM (represents true above-ground object heights).
    """
    if dsm_raster.shape != dtm_raster.shape:
        raise ValueError("DSM and DTM dimensions must match for nDSM computation.")
    ndsm = dsm_raster.astype(np.float32) - dtm_raster.astype(np.float32)
    # Clip negative micro-discrepancies below 0
    ndsm[ndsm < 0] = 0.0
    return ndsm

def generate_tiles(
    image_shape: Tuple[int, int],
    tile_size: int = 512,
    overlap_pct: int = 20
) -> List[Dict[str, int]]:
    """
    Divides high-resolution orthomosaic into overlapping tiles for batch inference.
    """
    height, width = image_shape
    stride = int(tile_size * (1 - overlap_pct / 100.0))
    tiles = []

    y = 0
    while y < height:
        x = 0
        while x < width:
            x_end = min(x + tile_size, width)
            y_end = min(y + tile_size, height)
            tiles.append({
                "x_min": x,
                "y_min": y,
                "x_max": x_end,
                "y_max": y_end,
                "tile_width": x_end - x,
                "tile_height": y_end - y
            })
            if x_end == width:
                break
            x += stride
        if y_end == height:
            break
        y += stride

    return tiles

def radiometric_normalize(image_tile: np.ndarray) -> np.ndarray:
    """
    Normalizes contrast and brightness across drone flight paths.
    """
    norm = image_tile.astype(np.float32)
    min_val = np.percentile(norm, 2)
    max_val = np.percentile(norm, 98)
    if max_val > min_val:
        norm = (norm - min_val) / (max_val - min_val)
        norm = np.clip(norm * 255.0, 0, 255).astype(np.uint8)
    return norm
