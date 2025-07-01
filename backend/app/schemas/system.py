from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Model to validate and return in response to healthcheck."""

    status: str = "OK"
    uptime: str
