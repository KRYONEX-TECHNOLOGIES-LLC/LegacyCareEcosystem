from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str
    tf_model_path: str
    anomaly_threshold: float
    wearable_update_interval: int
    max_bluetooth_connections: int

    class Config:
        env_file = ".env"

settings = Settings()