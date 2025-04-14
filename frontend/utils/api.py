import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")

def upload_csv(file, user: str):
    try:
        files = {"file": (file.name, file, "text/csv")}
        data = {"user": user}
        res = requests.post(f"{BACKEND_URL}/upload/", files=files, data=data)
        return res.json() if res.status_code == 200 else None
    except Exception as e:
        print(f"Erro: {e}")
        return None
    
def create_table_api(table_name: str, file):
    files = {'file': (file.name, file.getvalue())}
    data = {'table_name': table_name}
    response = requests.post(f"{BACKEND_URL}/athena/", files=files, data=data)
    return response.json()