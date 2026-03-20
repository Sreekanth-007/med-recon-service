from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.db import patients_collection, snapshots_collection, conflicts_collection
from app.schemas.snapshot import SnapshotIngestRequest
from app.services.normalization import normalize_medication_list
from app.services.conflict_detector import detect_conflicts

router = APIRouter(prefix="/patients", tags=["Medication Snapshots"])


@router.post("/{patient_id}/medication-snapshots")
def ingest_snapshot(patient_id: str, payload: SnapshotIngestRequest):
    # 1. Check if patient exists
    patient = patients_collection.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # 2. Normalize medications
    normalized_meds = normalize_medication_list(payload.medications)

    # 3. Determine next version number
    last_snapshot = snapshots_collection.find_one(
        {"patient_id": patient_id},
        sort=[("version_number", -1)]
    )
    next_version = 1 if not last_snapshot else last_snapshot["version_number"] + 1

    # 4. Store snapshot
    snapshot_doc = {
        "patient_id": patient_id,
        "clinic_id": patient["clinic_id"],
        "source": payload.source.value if hasattr(payload.source, "value") else payload.source,
        "source_timestamp": payload.source_timestamp,
        "ingested_at": datetime.utcnow(),
        "version_number": next_version,
        "medications": [m.model_dump() for m in normalized_meds],
        "raw_payload": payload.model_dump()
    }

    snapshot_result = snapshots_collection.insert_one(snapshot_doc)
    snapshot_id = str(snapshot_result.inserted_id)

    # 5. Load all snapshots for conflict detection
    all_snapshots = list(snapshots_collection.find({"patient_id": patient_id}))

    # 6. Detect conflicts
    detected_conflicts = detect_conflicts(all_snapshots)

    created_or_updated = 0

    for conflict in detected_conflicts:
        

        existing_conflict = conflicts_collection.find_one({
            "patient_id": patient_id,
            "conflict_type": conflict["conflict_type"],
            "drug_names": sorted(conflict["drug_names"]),
            "status": "unresolved"
        })

        if existing_conflict:
            conflicts_collection.update_one(
                {"_id": existing_conflict["_id"]},
                {
                    "$set": {
                        "description": conflict["description"],
                        "snapshot_ids": [str(s["_id"]) for s in all_snapshots],
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        else:
            conflict_doc = {
                "patient_id": patient_id,
                "clinic_id": patient["clinic_id"],
                "snapshot_ids": [str(s["_id"]) for s in all_snapshots],
                "conflict_type": conflict["conflict_type"],
                "drug_names": sorted(conflict["drug_names"]),
                "description": conflict["description"],
                "status": "unresolved",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "resolution": None
            }
            conflicts_collection.insert_one(conflict_doc)

        created_or_updated += 1

    return {
        "message": "Snapshot ingested successfully",
        "snapshot_id": snapshot_id,
        "version": next_version,
        "conflicts_detected": len(detected_conflicts),
        "conflicts_processed": created_or_updated
    }