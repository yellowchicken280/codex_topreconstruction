import os
import json
import requests

MODEL = "lbl/gpt-oss-120b-high"
BASE_URL = os.environ.get("OPENAI_BASE_URL")
API_KEY = os.environ.get("OPENAI_API_KEY")

if not BASE_URL or not API_KEY:
    raise SystemExit("ERROR: OPENAI_BASE_URL and OPENAI_API_KEY must be set in the environment.")

url = BASE_URL.rstrip("/") + "/v1/responses"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "model": MODEL,
    "input": "Hello, are you responsive?",
    "max_output_tokens": 32,
}

print(f"Testing model {MODEL} at {url}")
try:
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    print("HTTP status:", response.status_code)
    try:
        body = response.json()
    except ValueError:
        body = response.text
    print("Response body:", json.dumps(body, indent=2) if isinstance(body, dict) else body)
except requests.RequestException as exc:
    print("Request failed:", repr(exc))
    raise
