"""Auto-CAM prototype v2: generates simple CAM reports from input items.

This is a lightweight prototype intended to demonstrate structure and outputs
for the Auto-CAM v2 capability. It generates a JSON-like report summarizing
findings, scores, and supporting metadata.
"""
from typing import Dict, Any, List
from datetime import datetime


def generate_cam_report(items: List[Dict[str, Any]], report_meta: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate a CAM (Content/Compliance/Audit/Model) report from items.

    Args:
        items: List of detected items or findings. Each item is a dict with at least `id` and `score`.
        report_meta: Optional metadata for the report (author, dataset, org_id, etc.)

    Returns:
        A dictionary representing a CAM report.
    """
    report_meta = report_meta or {}
    timestamp = datetime.utcnow().isoformat() + "Z"
    summary = {
        "report_id": report_meta.get("report_id", f"cam_{int(datetime.utcnow().timestamp())}"),
        "generated_at": timestamp,
        "author": report_meta.get("author", "auto_cam_v2"),
        "org_id": report_meta.get("org_id"),
        "item_count": len(items),
        "aggregate_score": None,
        "items": []
    }

    if items:
        total = 0.0
        for it in items:
            score = float(it.get("score", 0.0))
            total += score
            summary["items"].append({
                "id": it.get("id"),
                "label": it.get("label"),
                "score": score,
                "notes": it.get("notes")
            })
        summary["aggregate_score"] = total / len(items)
    else:
        summary["aggregate_score"] = 0.0

    # Simple severity calculation
    if summary["aggregate_score"] >= 0.8:
        severity = "high"
    elif summary["aggregate_score"] >= 0.5:
        severity = "medium"
    else:
        severity = "low"

    summary["severity"] = severity

    return summary


if __name__ == "__main__":
    # Quick self-test
    sample_items = [
        {"id": "a1", "label": "face_match", "score": 0.92},
        {"id": "b2", "label": "doc_quality", "score": 0.77},
        {"id": "c3", "label": "liveness", "score": 0.85},
    ]
    report = generate_cam_report(sample_items, {"author": "dev", "org_id": "org_legacy"})
    import json
    print(json.dumps(report, indent=2))
