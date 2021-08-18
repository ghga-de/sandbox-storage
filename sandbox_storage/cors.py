# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
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

"""Make CORS configurable"""

from typing import Callable, Type, List
from pyramid.events import NewRequest
from pyramid.request import Request
from pyramid.response import Response
from .config import Config


def list_to_comma_sep_str(list_of_str: List[str]):
    """Join a list of strings into one comma-seperated string."""
    if len(list_of_str) == 0:
        return ""
    else:
        return ",".join(list_of_str)


def cors_header_response_callback_factory(config: Type[Config]) -> Callable:
    """A factory for creating CORS header callbacks that are
    configured based on a config object"""

    def cors_headers_response_callback(event: NewRequest):
        """CORS header callback that can be added to a pyramid config
        by:
            `config.add_subscriber(<this_function>, NewRequest)`
        """

        def cors_headers(_: Request, response: Response):
            """Modifies Requests."""

            response.headers.update(
                {
                    "Access-Control-Allow-Origin": list_to_comma_sep_str(
                        config.cors_allowed_origins
                    ),
                    "Access-Control-Allow-Methods": list_to_comma_sep_str(
                        config.cors_allowed_methods
                    ),
                    "Access-Control-Allow-Headers": list_to_comma_sep_str(
                        config.cors_allowed_headers
                    ),
                    "Access-Control-Allow-Credentials": "true"
                    if config.cors_allow_credentials
                    else "false",
                }
            )

        event.request.add_response_callback(cors_headers)

    return cors_headers_response_callback
