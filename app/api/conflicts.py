from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.db import patients_collection, conflicts_collection

router = APIRouter(tags=["Conflicts"])


@router.get("/patients/{patient_id}/conflicts")
def list_patient_conflicts(patient_id: str):
    patient = patients_collection.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    conflicts = list(conflicts_collection.find({"patient_id": patient_id}))

    response = []
    for conflict in conflicts:
        response.append({
            "conflict_id": str(conflict["_id"]),
            "patient_id": conflict["patient_id"],
            "clinic_id": conflict["clinic_id"],
            "conflict_type": conflict["conflict_type"],
            "drug_names": conflict["drug_names"],
            "description": conflict["description"],
            "status": conflict["status"],
            "snapshot_ids": conflict.get("snapshot_ids", []),
            "created_at": conflict.get("created_at"),
            "updated_at": conflict.get("updated_at"),
            "resolution": conflict.get("resolution")
        })

    return {
        "patient_id": patient_id,
        "conflicts": response
    }


@router.patch("/conflicts/{conflict_id}/resolve")
def resolve_conflict(conflict_id: str, payload: dict):
    reason = payload.get("reason")
    chosen_source = payload.get("chosen_source")
    resolved_by = payload.get("resolved_by")

    if not reason or not chosen_source or not resolved_by:
        raise HTTPException(
            status_code=400,
            detail="reason, chosen_source, and resolved_by are required"
        )

    result = conflicts_collection.update_one(
        {"_id": __import__("bson").ObjectId(conflict_id)},
        {
            "$set": {
                "status": "resolved",
                "updated_at": datetime.utcnow(),
                "resolution": {
                    "reason": reason,
                    "chosen_source": chosen_source,
                    "resolved_by": resolved_by,
                    "resolved_at": datetime.utcnow()
                }
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conflict not found")

    return {
        "message": "Conflict resolved successfully",
        "conflict_id": conflict_id
    }