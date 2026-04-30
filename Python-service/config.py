import os
from dataclasses import dataclass


@dataclass
class Config:
    node_api_url: str
    admin_email: str
    admin_password: str
    port: int


def load_config() -> Config:
    return Config(
        node_api_url=os.getenv("NODE_API_URL", "http://localhost:5007/api/v1"),
        admin_email=os.getenv("ADMIN_EMAIL", "admin@school-admin.com"),
        admin_password=os.getenv("ADMIN_PASSWORD", "3OU4zn3q6Zh9"),
        port=int(os.getenv("PORT", "5008")),
    )
