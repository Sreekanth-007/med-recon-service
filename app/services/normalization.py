import json
from pathlib import Path

from app.schemas.medication import MedicationInput, MedicationNormalized

RULES_PATH = Path("data/conflict_rules.json")

with open(RULES_PATH, "r", encoding="utf-8") as f:
    RULES = json.load(f)

DRUG_CLASSES = RULES.get("drug_classes", {})


def normalize_unit(unit: str | None) -> str | None:
    if unit is None:
        return None
    return unit.strip().lower()


def normalize_name(name: str) -> str:
    return name.strip().lower()


def get_drug_class(normalized_name: str) -> str | None:
    return DRUG_CLASSES.get(normalized_name)


def normalize_medication_item(item: MedicationInput) -> MedicationNormalized:
    normalized_name = normalize_name(item.name)

    return MedicationNormalized(
        name=item.name.strip(),
        normalized_name=normalized_name,
        dose_value=item.dose_value,
        dose_unit=normalize_unit(item.dose_unit),
        frequency=item.frequency.strip().lower() if item.frequency else None,
        status=item.status,
        drug_class=get_drug_class(normalized_name)
    )


def normalize_medication_list(items: list[MedicationInput]) -> list[MedicationNormalized]:
    return [normalize_medication_item(item) for item in items]