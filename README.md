# Medication Reconciliation & Conflict Reporting Service

A robust backend service for ingesting medication lists from multiple clinical sources, maintaining longitudinal history, detecting inter-source conflicts, and supporting clinical review workflows.

---

## 🚀 Features

- **Multi-source Ingestion**: Accept medication lists from clinic EMRs, hospital discharge summaries, and patient-reported data
- **Medication Normalization**: Convert raw medication data into a standardized canonical format
- **Versioned Snapshots**: Maintain complete history of medication lists with version tracking
- **Conflict Detection**: Automatically identify discrepancies and differences across medication sources
- **Auditable Conflict Management**: Store detected conflicts with full traceability
- **Resolution Workflow**: Mark conflicts as resolved with documented reasoning and source selection
- **Reporting**: Query patients with unresolved conflicts by clinic for clinical review

---

## 🏗️ Architecture

```
FastAPI (API Layer)
│
├── Patients API              → Patient registration and management
├── Snapshots API             → Medication ingestion and versioning
├── Conflicts API             → Conflict listing and resolution
└── Reports API               → Unresolved conflicts reporting
│
├── Services Layer
│   ├── Normalization Service → Standardize medication data
│   └── Conflict Detector     → Identify medication conflicts
│
└── MongoDB (Persistence)
    ├── patients              → Patient demographic data
    ├── snapshots             → Medication snapshots with history
    └── conflicts             → Detected conflicts and resolutions
```

---

## 📋 Prerequisites

- Python 3.8+
- MongoDB 4.0+
- pip

---

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd med-recon-service
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection details
   ```

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
MONGODB_URI=mongodb://localhost:27017/med-recon-service
MONGODB_DB_NAME=med-recon-service
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🚀 Running the Service

**Start the development server:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 📡 API Endpoints

### Patients

**Create a patient**
```
POST /patients/
Content-Type: application/json

{
  "patient_id": "P001",
  "name": "John Doe",
  "clinic_id": "CLINIC_A",
  "age": 65
}
```

### Medication Snapshots

**Ingest medication snapshot**
```
POST /patients/{patient_id}/medication-snapshots
Content-Type: application/json

{
  "source": "clinic_emr",
  "source_timestamp": "2026-03-20T10:30:00Z",
  "medications": [
    {
      "drug_name": "Lisinopril",
      "dosage": "10mg",
      "frequency": "once daily",
      "indication": "Hypertension"
    },
    {
      "drug_name": "Metformin",
      "dosage": "500mg",
      "frequency": "twice daily",
      "indication": "Type 2 Diabetes"
    }
  ]
}
```

### Conflicts

**List patient conflicts**
```
GET /patients/{patient_id}/conflicts
```

Response:
```json
{
  "patient_id": "P001",
  "conflicts": [
    {
      "conflict_id": "60d5ec49c1234567890abcde",
      "conflict_type": "dosage_mismatch",
      "drug_names": ["Lisinopril"],
      "description": "Dosage differs between clinic EMR (10mg) and discharge summary (5mg)",
      "status": "unresolved",
      "created_at": "2026-03-20T10:35:00Z"
    }
  ]
}
```

**Resolve a conflict**
```
PATCH /conflicts/{conflict_id}/resolve
Content-Type: application/json

{
  "reason": "Discharge summary reflects dose reduction per cardiologist recommendation",
  "chosen_source": "hospital_discharge",
  "resolved_by": "Dr. Smith"
}
```

### Reports

**Get unresolved conflicts by clinic**
```
GET /reports/unresolved-conflicts?clinic_id=CLINIC_A
```

Response:
```json
{
  "clinic_id": "CLINIC_A",
  "patients": [
    {
      "patient_id": "P001",
      "unresolved_conflicts": 2
    },
    {
      "patient_id": "P003",
      "unresolved_conflicts": 1
    }
  ]
}
```

---

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/
pytest tests/test_conflict_detector.py -v
pytest tests/test_reporting.py -v
```

---

## 📁 Project Structure

```
med-recon-service/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration management
│   ├── db.py                   # MongoDB connections
│   ├── api/
│   │   ├── patients.py         # Patient endpoints
│   │   ├── snapshots.py        # Snapshot ingestion endpoints
│   │   ├── conflicts.py        # Conflict management endpoints
│   │   └── reports.py          # Reporting endpoints
│   ├── models/
│   │   └── enums.py            # Enum definitions (source types, conflict types)
│   ├── schemas/
│   │   ├── patient.py          # Patient schema
│   │   ├── snapshot.py         # Snapshot schema
│   │   ├── medication.py       # Medication schema
│   │   └── conflict.py         # Conflict schema
│   └── services/
│       ├── normalization.py    # Medication normalization logic
│       ├── conflict_detector.py # Conflict detection algorithms
│       └── reporting.py        # Reporting utilities
├── data/
│   └── conflict_rules.json     # Conflict detection rules
├── scripts/
│   └── seed_data.py            # Database seeding script
├── tests/
│   ├── test_conflict_detector.py
│   └── test_reporting.py
├── requirements.txt
└── README.md
```

---

## 🔄 Workflow Example

1. **Register a patient**
   ```
   POST /patients/ with patient details
   ```

2. **Ingest medication snapshot from clinic**
   ```
   POST /patients/{patient_id}/medication-snapshots with clinic source
   ```

3. **Ingest medication snapshot from hospital discharge**
   ```
   POST /patients/{patient_id}/medication-snapshots with discharge source
   ```

4. **System automatically detects conflicts** between the two sources

5. **Clinician reviews conflicts**
   ```
   GET /patients/{patient_id}/conflicts
   ```

6. **Clinician resolves conflict** with reasoning
   ```
   PATCH /conflicts/{conflict_id}/resolve
   ```

7. **Report unresolved conflicts** for clinic oversight
   ```
   GET /reports/unresolved-conflicts?clinic_id=CLINIC_A
   ```

---

## 🧩 Problem Statement

Medication data often comes from multiple sources (clinic EMR, hospital discharge summaries, patient-reported data), and these sources may contain conflicting or inconsistent information.

This system enables:
- Aggregation of medication data from multiple sources
- Detection of conflicts across sources
- Explicit, auditable conflict resolution by clinicians

Instead of assuming a single source of truth, the system **embraces ambiguity and manages it transparently**.

---

## ⚠️ Conflict Types Detected

- **Dose Mismatch**
  - Same drug prescribed with different dosages across sources

- **Class Conflict**
  - Medications from conflicting drug classes (e.g., ACE inhibitor + ARB)

- **Duplicate Therapy** *(extendable)*
  - Multiple drugs serving same therapeutic purpose

> Conflict detection is rule-based and configurable via `conflict_rules.json`

---

## ⚠️ Known Limitations

- Uses rule-based conflict detection (not integrated with real drug databases)
- No authentication or role-based access control
- Not optimized for high-scale production workloads
- MongoDB Atlas connectivity may face TLS/network issues in restricted environments

---

## 🔮 Future Improvements

- Integrate real drug interaction APIs (e.g., RxNorm, DrugBank)
- Improve normalization with NLP-based mapping
- Add frontend dashboard for clinicians
- Implement authentication & role-based access
- Optimize conflict detection for large datasets

---

## 🛠️ Development

**Install development dependencies:**
```bash
pip install -r requirements.txt
```

**Key service modules:**
- `normalization.py`: Implements medication normalization (dosage standardization, synonym resolution)
- `conflict_detector.py`: Implements conflict detection algorithms based on rules in `conflict_rules.json`
- `reporting.py`: Aggregation and reporting utilities

---

## 🤖 AI Usage

### What AI was used for:
- **Boilerplate generation**: FastAPI route templates, MongoDB connection setup, and Pydantic schema scaffolding
- **Debugging**: Connection errors, async handling patterns, and error response formatting
- **Documentation**: README structure, endpoint examples, and workflow descriptions

### What was reviewed and changed manually:
- **Conflict detection logic**: Reimplemented the core conflict detection algorithm to be more explicit about rule matching
- **Data schemas**: Modified Pydantic models to ensure strict validation and proper typing across all endpoints
- **API error handling**: Enhanced all error responses with meaningful messages and proper HTTP status codes
- **MongoDB queries**: Reviewed and optimized aggregation pipelines for reporting endpoints

### Example: Conflict Detection Disagreement
**Initial AI output**: Suggested a simple equality-based approach to detect dosage conflicts.

**Why it was changed**: This failed to account for dosage unit variations (e.g., "10mg" vs "1000mcg"). Instead, I implemented a normalization step that converts all dosages to a standard unit before comparison, which is clinically accurate and prevents false positives.

The final implementation in `conflict_detector.py` includes this normalization preprocessing, which the AI originally missed in its first suggestion.

---

## 📝 License

This project is licensed under the MIT License.

---

