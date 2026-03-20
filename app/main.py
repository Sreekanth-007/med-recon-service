from fastapi import FastAPI

from app.api.patients import router as patients_router
from app.api.snapshots import router as snapshots_router
from app.api.conflicts import router as conflicts_router
from app.api.reports import router as reports_router

app = FastAPI(
    title="Medication Reconciliation & Conflict Reporting Service",
    description="Backend service for ingesting medication data, detecting conflicts, and reporting.",
    version="1.0.0"
)

app.include_router(patients_router)
app.include_router(snapshots_router)
app.include_router(conflicts_router)
app.include_router(reports_router)

@app.get("/")
def health_check():
    return {
        "status": "success",
        "message": "Medication reconciliation service is running"
    }