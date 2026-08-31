from pathlib import Path
import subprocess, sys

BASE = Path(__file__).resolve().parent
subprocess.check_call([sys.executable, str(BASE / "seed.py"), "--reset"])
print("Seed complete. Configure SCHOLARSHIP-APP-API-Key if you want to refresh ScholarshipOwl data.")
