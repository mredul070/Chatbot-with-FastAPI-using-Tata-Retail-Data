import os
from typing import Optional, ClassVar
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

# if not os.getenv("SQLALCHEMY_DATABASE_URI"):
load_dotenv()


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)
    PROJECT_NAME: str = "TATA Chatbot App"
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.environ['SQLALCHEMY_DATABASE_URI']
    ALGORITHM: ClassVar = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60* 24
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    JWT_SECRET_KEY: str = os.environ['JWT_SECRET_KEY']
    JWT_REFRESH_SECRET_KEY: str = os.environ['JWT_REFRESH_SECRET_KEY']
    JARVIS_APP: str = "https://nspectai-service-w6obo6kgla-uc.a.run.app/chat"


settings = Settings()