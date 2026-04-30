import requests
from config import load_config


class AuthClient:
    def __init__(self):
        self.config = load_config()
        self.session = requests.Session()
        self.csrf_token: str | None = None
        self._cookie_header: str | None = None

    def login(self) -> None:
        url = f"{self.config.node_api_url}/auth/login"
        payload = {
            "username": self.config.admin_email,
            "password": self.config.admin_password,
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()

        access_token = self.session.cookies.get("accessToken")
        refresh_token = self.session.cookies.get("refreshToken")
        self.csrf_token = self.session.cookies.get("csrfToken")

        self._cookie_header = (
            f"accessToken={access_token}; "
            f"refreshToken={refresh_token}; "
            f"csrfToken={self.csrf_token}"
        )

    def get(self, url: str, **kwargs) -> requests.Response:
        if not self.csrf_token:
            self.login()

        headers = kwargs.pop("headers", {})
        headers["x-csrf-token"] = self.csrf_token
        headers["Cookie"] = self._cookie_header

        response = self.session.get(url, headers=headers, **kwargs)

        if response.status_code == 401:
            self.login()
            headers["x-csrf-token"] = self.csrf_token
            headers["Cookie"] = self._cookie_header
            response = self.session.get(url, headers=headers, **kwargs)

        return response
