# Copyright 2021 Universität Tübingen, DKFZ and EMBL for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
from pydantic import BaseSettings
from typing import Literal, Dict, Any, Optional, Callable
import yaml

# A abbreviation of this app:
config_prefix = "sbstorage"
# When defined via enviroment variables, all
# variables have to be prefixed with this string
# (like this "{config_prefix}_{actual_variable_name}").
# Moreover, this prefix is used to derive the default 
# location for the config yaml file ("~/.{config_prefix}.yaml"):
default_config_yaml = os.path.join(pathlib.Path.home(), f".{config_prefix}.yaml")

# type alias for log level parameter
LogLevel = Literal[
    'critical', 
    'error', 
    'warning', 
    'info',
    'debug',
    'trace'
]


def yaml_settings_factory(
    config_yaml: Optional[str] = None
) -> Callable[[BaseSettings], Dict[str, Any]]:
    """
    A factory for source methods for Pydantic's BaseSettings Config that load
    settings from a yaml file.
    """   
    if config_yaml is None and os.path.isfile(default_config_yaml):
        config_yaml = default_config_yaml

    def yaml_settings(settings: BaseSettings)-> Dict[str, Any]:
        if config_yaml is None:
            return {}
        else:
            with open(config_yaml, "r") as yaml_file:
                return yaml.safe_load(yaml_file)
    
    return yaml_settings

class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080
    log_level: LogLevel = "info"

def get_settings(
    config_yaml: Optional[str] = None,
    **kwargs,
) -> Settings:
    """A wrapper around pydantics BaseSettings that allows to specify the path to a
    yaml file for reading config parameters. 
    Priorities of config sources are as follows (highest Priority first):
        - parameters passed using **kwargs
        - environment variables
        - file secrets
        - yaml config file
        - defaults

    Args:
        config_yaml (Optional[str], optional): Path to config yaml. 
            Defaults to "~/.{config_prefix}.yaml"
        **kwargs: All other arguments are passed on to the Settings class.

    Returns:
        BaseSettings: Settings class based on pydantic.BaseSettings.

    """

    class ModSettings(Settings):
        class Config:
            # add this prefix to all variable names to
            # define them as environment variables:
            env_prefix = f'{config_prefix}_'

            @classmethod
            def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
            ):
                return (
                    init_settings,
                    env_settings,
                    file_secret_settings,
                    yaml_settings_factory(config_yaml),
                )
    
    return ModSettings(**kwargs)
