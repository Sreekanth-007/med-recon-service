def detect_conflicts(snapshots: list[dict]) -> list[dict]:
    conflicts = []

    # Flatten all meds
    meds_by_name = {}

    for snap in snapshots:
        for med in snap["medications"]:
            name = med["normalized_name"]

            if name not in meds_by_name:
                meds_by_name[name] = []

            meds_by_name[name].append(med)

    # --- Rule 1: Dose mismatch ---
    for name, meds in meds_by_name.items():
        doses = set((m.get("dose_value"), m.get("dose_unit")) for m in meds if m.get("dose_value"))

        if len(doses) > 1:
            conflicts.append({
                "conflict_type": "dose_mismatch",
                "drug_names": [name],
                "description": f"Different doses found for {name}: {doses}"
            })

    # --- Rule 2: stopped vs active ---
    for name, meds in meds_by_name.items():
        statuses = set(m.get("status") for m in meds)

        if "active" in statuses and "stopped" in statuses:
            conflicts.append({
                "conflict_type": "stopped_vs_active",
                "drug_names": [name],
                "description": f"{name} is active in one source and stopped in another"
            })

    # --- Rule 3: class conflicts ---
    all_classes = {}

    for meds in meds_by_name.values():
        for med in meds:
            if med.get("drug_class"):
                all_classes.setdefault(med["drug_class"], []).append(med["normalized_name"])

    # Simple rule: ACE + ARB conflict
    if "ace_inhibitor" in all_classes and "arb" in all_classes:
        conflicts.append({
            "conflict_type": "class_conflict",
            "drug_names": all_classes["ace_inhibitor"] + all_classes["arb"],
            "description": "ACE inhibitor and ARB should not be combined"
        })

    return conflicts