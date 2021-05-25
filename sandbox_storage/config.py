from pydantic import BaseSettings
from typing import Literal

LogLevel = Literal[
    'critical', 
    'error', 
    'warning', 
    'info',
    'debug',
    'trace'
]


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080
    log_level: LogLevel = "info"

    class Config:
        # add this prefix to all variable names to
        # define them as environment variables:
        env_prefix = 'sbstore_'