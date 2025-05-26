from pydantic import BaseModel


class ServiceConfig(BaseModel):
    name: str
    auth_url: str = None
    base_url: str
    timeout: int = 30


class ApiAutoTestConfig(BaseModel):
    environment: str
    services: ServiceConfig
    trace: bool = False
