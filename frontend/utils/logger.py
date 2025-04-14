import csv
from datetime import datetime
import os

LOG_FILE = "frontend/assets/action_log.csv"

def log_action(user: str, action: str, status: str):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user, action, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status])
