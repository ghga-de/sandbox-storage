# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configuration parsing"""

from typing import List
from functools import lru_cache
from ghga_service_chassis_lib.config import config_from_yaml
from ghga_service_chassis_lib.api import LogLevel
from pydantic import BaseSettings


@config_from_yaml(prefix="sandbox_storage")
class Config(BaseSettings):
    """Config parameters and their defaults."""

    host: str = "127.0.0.1"
    port: int = 8080
    log_level: LogLevel = "info"
    drs_path: str = "drs://localhost:8080/"
    api_path: str = "/ga4gh/drs/v1"

    cors_allowed_origins: List[str] = []
    cors_allow_credentials: bool = False
    cors_allowed_methods: List[str] = []
    cors_allowed_headers: List[str] = []


@lru_cache
def get_config():
    """Get config parameter."""
    return Config()
