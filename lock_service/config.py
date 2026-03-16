from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LOCK_EXPIRY:int

    class Config:
        env_file = ".env"

settings=Settings()
