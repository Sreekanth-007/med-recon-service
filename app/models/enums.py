from enum import Enum


class SourceType(str, Enum):
    clinic_emr = "clinic_emr"
    hospital_discharge = "hospital_discharge"
    patient_reported = "patient_reported"


class MedicationStatus(str, Enum):
    active = "active"
    stopped = "stopped"


class ConflictType(str, Enum):
    dose_mismatch = "dose_mismatch"
    class_conflict = "class_conflict"
    stopped_vs_active = "stopped_vs_active"


class ConflictStatus(str, Enum):
    unresolved = "unresolved"
    resolved = "resolved"