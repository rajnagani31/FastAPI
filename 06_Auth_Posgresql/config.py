from functools import lru_cache
from typing import Optional
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseConfig(BaseSettings):
    ENV_STATE: str = "dev"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    USER : str | None = None
    SECRET_KEY : str | None = None


class GlobalConfig(BaseConfig):
    DB_URL : str | None = None
    FORCE_ROLLBACK : bool = False

class DevConfig(GlobalConfig):
    # model_config= SettingsConfigDict(env_prefix="DEV_", extra="ignore")
    pass

@lru_cache()
def get_config(env_state: str):
    logger.info(f"Loading {env_state} configuration")
    logger.info(f"ENV_STATE: {env_state}")
    config= {"dev":DevConfig}
    return config[env_state]()

config = get_config(BaseConfig().ENV_STATE)