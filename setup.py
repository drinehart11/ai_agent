import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv


# local ai agent setup: connects to LM Studio
# will attempt connection without API_KEY if not present in .env

# last edit: 6-FEB-2026
# author: Duane Rinehart


script_dir = Path(__file__).resolve().parent
parent_env = script_dir.parent / ".env"
load_dotenv(parent_env)

ENDPOINT = os.getenv("LOCAL_LLM_ENDPOINT")
MODEL = os.getenv("MODEL_NAME")
API_KEY = os.getenv("API_KEY")

headers = {
    "Content-Type": "application/json"
}
if API_KEY:
    headers["Authorization"] = f"Bearer {API_KEY}"

response = requests.post(
  f"{ENDPOINT}",
  headers=headers,
  json={
    "model": MODEL,
    "input": "Write a short haiku about sunrise."
  }
)
print(json.dumps(response.json(), indent=2))

