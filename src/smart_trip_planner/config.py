from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE : float = 0.1
    OPENAI_API_KEY: SecretStr = SecretStr("")
    TRAVEL_PROVIDER: str = "mock"
    SERPAPI_KEY: SecretStr = SecretStr("")
    DB_PATH: str = "smart_trip_planner.db"
    LANGFUSE_PUBLIC_KEY: SecretStr = SecretStr("")
    LANGFUSE_SECRET_KEY: SecretStr = SecretStr("")
    LANGFUSE_HOST: str = "https://us.cloud.langfuse.com"
    
    model_config = {"env_file": ".env"}

settings = Settings()