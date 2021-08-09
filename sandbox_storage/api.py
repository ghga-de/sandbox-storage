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

""" Provides the API endpoints """

import typing as t
from pyramid.view import view_config
from pyramid.config import Configurator, settings
from pyramid.request import Request

from dataclasses import dataclass
from .config import get_settings

config_settings = get_settings


@dataclass
class DrsObject:
    """A DrsObject"""

    id: str
    self_uri: str
    size: int
    created_time: str
    checksums: dict

    def __json__(self, request: Request) -> t.Dict[str, str]:
        """JSON-renderer for this object."""
        return {
            "id": self.id,
            "self_uri": self.self_uri,
            "size": self.size,
            "created_time": self.created_time,
            "checksums": self.checksums,
        }


@dataclass
class AccessURL:
    """An AccessURL"""

    url: str

    def __json__(self, request: Request) -> t.Dict[str, str]:
        """JSON-renderer for this object."""
        return {"url": self.url}


def get_app():
    """Builds the App"""
    base_url = "/ga4gh/drs/v1"

    with Configurator() as config:
        config.include("pyramid_openapi3")
        config.pyramid_openapi3_spec(
            "sandbox_storage/openapi.yaml", route="/ghga/drs/v1/openapi.yaml"
        )
        config.pyramid_openapi3_add_explorer(base_url)

        config.add_route("hello", "/")
        config.add_route("health", "/health")

        config.add_route("objects_id", base_url + "/objects/{object_id}")
        config.add_route(
            "objects_id_access_id", base_url + "/objects/{object_id}/access/{access_id}"
        )
        config.scan(".")

    return config.make_wsgi_app()


@view_config(route_name="hello", renderer="json", openapi=False, request_method="GET")
def index(context, request):
    """Index Enpoint, returns 'Hello World'"""
    return {"content": "Hello World!"}


@view_config(
    route_name="objects_id", renderer="json", openapi=True, request_method="GET"
)
def get_objects_id(request: Request):
    """Get info about a `DrsObject`."""
    object_id = request.matchdict["object_id"]

    db = request.dbsession
    target_object = resource_by_id(db, User, object_id)

    return DrsObject(
        id=object_id,
        self_uri=config_settings.drs_path + object_id,
        size=1,
        created_time="2002-10-02T15:00:00Z",
        checksums=[
            {
                "checksum": "62361711c02eaa44409b79ebee049268",
                "type": "md5",
            }
        ],
    )


@view_config(
    route_name="objects_id_access_id",
    renderer="json",
    openapi=True,
    request_method="GET",
)
def get_objects_id_access_id(request: Request):
    """Get a URL for fetching bytes."""
    object_id = request.matchdict["object_id"]
    access_id = request.matchdict["access_id"]

    return AccessURL(url="https://drs.access.dummy")


@view_config(route_name="health", renderer="json", openapi=False, request_method="GET")
def get_health(context, request):
    """Health check"""
    return {"status": "OK"}
