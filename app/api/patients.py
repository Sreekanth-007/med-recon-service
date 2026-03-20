from fastapi import APIRouter, HTTPException
from app.db import patients_collection

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/")
def create_patient(patient: dict):
    try:
        patient_id = patient.get("patient_id")

        if not patient_id:
            raise HTTPException(status_code=400, detail="patient_id is required")

        existing = patients_collection.find_one({"patient_id": patient_id})
        if existing:
            raise HTTPException(status_code=400, detail="Patient already exists")

        patient_data = {
            "patient_id": patient["patient_id"],
            "name": patient["name"],
            "clinic_id": patient["clinic_id"],
            "age": patient["age"]
        }

        result = patients_collection.insert_one(patient_data)

        return {
            "message": "Patient created successfully",
            "inserted_id": str(result.inserted_id),
            "patient": {
                "patient_id": patient["patient_id"],
                "name": patient["name"],
                "clinic_id": patient["clinic_id"],
                "age": patient["age"]
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Create patient failed: {str(e)}")