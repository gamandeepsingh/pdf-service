from services.auth_client import AuthClient
from config import load_config


def fetch_student(student_id: str) -> dict:
    config = load_config()
    client = AuthClient()
    client.login()

    url = f"{config.node_api_url}/students/{student_id}"
    response = client.get(url)

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()
