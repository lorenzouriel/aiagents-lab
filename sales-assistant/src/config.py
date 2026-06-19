from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openai_model_default: str = "gpt-4o-mini"
    openai_model_quality: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"

    evolution_api_url: str
    evolution_api_key: str
    evolution_instance_name: str

    nuvemshop_store_id: str = "mock"
    nuvemshop_access_token: str = "mock"
    nuvemshop_mock: bool = False

    database_url: str
    redis_url: str = "redis://redis:6379"

    kestra_url: str = "http://kestra:8080"

    owner_phone_number: str

    max_discovery_turns: int = 3
    response_timeout_seconds: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
