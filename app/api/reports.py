from fastapi import APIRouter, HTTPException
from app.db import conflicts_collection

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/unresolved-conflicts")
def get_unresolved_conflicts(clinic_id: str):
    try:
        pipeline = [
            {
                "$match": {
                    "clinic_id": clinic_id,
                    "status": "unresolved"
                }
            },
            {
                "$group": {
                    "_id": "$patient_id",
                    "conflict_count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "conflict_count": {"$gte": 1}
                }
            }
        ]

        result = list(conflicts_collection.aggregate(pipeline))

        return {
            "clinic_id": clinic_id,
            "patients": [
                {
                    "patient_id": r["_id"],
                    "unresolved_conflicts": r["conflict_count"]
                }
                for r in result
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reporting failed: {str(e)}")