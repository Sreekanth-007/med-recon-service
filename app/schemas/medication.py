from pydantic import BaseModel, Field
from typing import Optional
from app.models.enums import MedicationStatus


class MedicationInput(BaseModel):
    name: str = Field(..., min_length=1)
    dose_value: Optional[float] = Field(default=None, ge=0)
    dose_unit: Optional[str] = None
    frequency: Optional[str] = None
    status: MedicationStatus = MedicationStatus.active


class MedicationNormalized(BaseModel):
    name: str
    normalized_name: str
    dose_value: Optional[float] = None
    dose_unit: Optional[str] = None
    frequency: Optional[str] = None
    status: MedicationStatus
    drug_class: Optional[str] = None