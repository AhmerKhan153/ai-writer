import requests

BASE_URL = "http://localhost:8080"
GATEWAY_TOKEN = "YOUR_OPENCLAW_GATEWAY_TOKEN"

headers = {
    "Authorization": f"Bearer {GATEWAY_TOKEN}",
    "Content-Type": "application/json"
}

def check_gateway_status():
    """Verifies connection to the dockerized OpenClaw instance."""
    try:
        response = requests.get(f"{BASE_URL}/status", headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError:
        return "Could not connect to OpenClaw container. Check your port mappings."

print(check_gateway_status())