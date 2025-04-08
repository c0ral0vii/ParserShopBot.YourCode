import os
import pathlib
from pydantic_settings import BaseSettings,  SettingsConfigDict

ROOT_PATH = pathlib.Path(__file__).parent

class Settings(BaseSettings):
    bot_token: str
    model_config = SettingsConfigDict(env_file=ROOT_PATH / ".env", env_file_encoding="utf-8")
    
settings = Settings()