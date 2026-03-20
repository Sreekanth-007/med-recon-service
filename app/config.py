import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "med_recon_db")

print("DEBUG MONGODB_URL:", MONGODB_URL)
print("DEBUG DATABASE_NAME:", DATABASE_NAME)