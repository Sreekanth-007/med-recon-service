from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.enums import SourceType
from app.schemas.medication import MedicationInput, MedicationNormalized


class SnapshotIngestRequest(BaseModel):
    source: SourceType
    source_timestamp: Optional[datetime] = None
    medications: List[MedicationInput] = Field(..., min_length=1)


class SnapshotDocument(BaseModel):
    patient_id: str
    clinic_id: str
    source: SourceType
    source_timestamp: Optional[datetime] = None
    ingested_at: datetime
    version_number: int
    medications: List[MedicationNormalized]
    raw_payload: dict