from pydantic import BaseModel

class SecretIn(BaseModel):
    secret: str
    expire_seconds: int = 3600  # Default: 1 hour
    max_views: int = 1          # Default: 1 view
