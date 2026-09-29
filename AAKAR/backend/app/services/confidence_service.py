from typing import Dict, Any, Tuple

def compute_confidence_and_dispute_risk(
    base_prob: float = 0.88,
    has_ambiguity: bool = False,
    ndsm_mismatch: bool = False,
    boundary_offset_gt_2m: bool = False,
    image_quality_issue: bool = False,
    has_topology_error: bool = False,
    gis_alignment_lt_half_meter: bool = True,
    multi_source_agreement: bool = True,
    gt_confirmed: bool = False,
    has_encroachment: bool = False,
    multiple_gt_owners: bool = False
) -> Tuple[float, int, Dict[str, Any]]:
    """
    Computes parcel AI confidence score (0.0 to 1.0) and dispute risk score (0 to 100).
    """
    # 1. Confidence Score Computation
    score = base_prob
    factors = {
        "base_prob": round(base_prob, 3),
        "adjustments": []
    }

    if has_ambiguity:
        score -= 0.15
        factors["adjustments"].append({"reason": "Ambiguous multi-model edge prediction", "delta": -0.15})
    if ndsm_mismatch:
        score -= 0.10
        factors["adjustments"].append({"reason": "nDSM roof-to-ground height discontinuity", "delta": -0.10})
    if boundary_offset_gt_2m:
        score -= 0.10
        factors["adjustments"].append({"reason": "Historical GIS record offset > 2m", "delta": -0.10})
    if image_quality_issue:
        score -= 0.10
        factors["adjustments"].append({"reason": "Tile shadow/occlusion detection", "delta": -0.10})
    if has_topology_error:
        score -= 0.15
        factors["adjustments"].append({"reason": "Unresolved topology validation error", "delta": -0.15})

    if gis_alignment_lt_half_meter:
        score += 0.10
        factors["adjustments"].append({"reason": "Concordance with registered survey edge (< 0.5m)", "delta": +0.10})
    if multi_source_agreement:
        score += 0.05
        factors["adjustments"].append({"reason": "Multi-spectral + LiDAR/nDSM consensus", "delta": +0.05})
    if gt_confirmed:
        score += 0.20
        factors["adjustments"].append({"reason": "Field ground-truth GNSS verification", "delta": +0.20})

    final_confidence = max(0.05, min(0.99, score))
    final_confidence = round(final_confidence, 2)

    # 2. Dispute Risk Score Computation (0 to 100)
    risk_score = 0
    risk_items = []

    if has_encroachment:
        risk_score += 40
        risk_items.append({"factor": "Encroachment flag present", "points": 40})
    if has_topology_error:
        risk_score += 15
        risk_items.append({"factor": "Topology error on feature", "points": 15})
    if final_confidence < 0.50:
        risk_score += 20
        risk_items.append({"factor": "Low AI confidence score (< 0.50)", "points": 20})
    if boundary_offset_gt_2m:
        risk_score += 15
        risk_items.append({"factor": "Significant GIS boundary deviation (> 2m)", "points": 15})
    if multiple_gt_owners:
        risk_score += 10
        risk_items.append({"factor": "Conflicting claimant records in field survey", "points": 10})

    risk_score = min(100, risk_score)
    factors["dispute_factors"] = risk_items
    factors["dispute_tier"] = "High" if risk_score >= 60 else ("Medium" if risk_score >= 30 else "Low")
    factors["confidence_tier"] = "High" if final_confidence >= 0.85 else ("Medium" if final_confidence >= 0.50 else "Low")

    return final_confidence, risk_score, factors
