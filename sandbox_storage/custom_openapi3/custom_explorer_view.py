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

"""Customize the pyramid-openapi3 swagger explorer"""

from pathlib import Path
from typing import Optional
from string import Template

from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.exceptions import ConfigurationError
from pyramid.config import PHASE0_CONFIG

HERE = Path(__file__).parent.resolve()
SWAGGER_HTML = HERE / "swagger.html"


# ignore some pylint error
# as this code comes directly from
# pyramid-openapi and should thus
# be mpdofied as little as possible:
def add_custom_explorer_view(  # pylint: disable=too-many-arguments
    config: Configurator,
    route: str = "/docs/",
    route_name: str = "pyramid_openapi3.explorer",
    ui_version: str = "3.17.1",
    permission: str = NO_PERMISSION_REQUIRED,
    apiname: str = "pyramid_openapi3",
    custom_spec_url: Optional[str] = None,
) -> None:
    """
    Modified from
    https://github.com/Pylons/pyramid_openapi3/blob/d181ac4bc7baa7cae50ab16797d6cb5b7c3ae24c/pyramid_openapi3/__init__.py#L130
    to make the target openapi.yaml URL configurable.

    :param route: URL path where to serve
    :param route_name: Route name that's being added
    :param ui_version: Swagger UI version string
    :param permission: Permission for the explorer view
    :param permission: Permission for the explorer view
    """

    def register() -> None:
        def explorer_view(request: Request) -> Response:
            settings = config.registry.settings
            if settings.get(apiname) is None:
                raise ConfigurationError(
                    "You need to call config.pyramid_openapi3_spec for the explorer "
                    "to work."
                )
            with open(SWAGGER_HTML) as file:  # pylint: disable=unspecified-encoding
                template = Template(file.read())
                spec_url = (
                    custom_spec_url
                    if custom_spec_url
                    else request.route_url(settings[apiname]["spec_route_name"])
                )
                html = template.safe_substitute(
                    ui_version=ui_version,
                    spec_url=spec_url,
                )
            return Response(html)

        config.add_route(route_name, route)
        config.add_view(
            route_name=route_name, permission=permission, view=explorer_view
        )

    config.action((f"{apiname}_add_explorer",), register, order=PHASE0_CONFIG)
