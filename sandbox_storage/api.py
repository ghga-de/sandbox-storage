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

from dataclasses import dataclass
import typing as t
from pyramid.view import view_config
from pyramid.config import Configurator, settings
from pyramid.request import Request
from pyramid.httpexceptions import HTTPNotFound

from .config import get_settings
from .database import get_session
from .models import DrsObject

config_settings = get_settings()


@dataclass
class DrsReturnObject:
    """A DrsObject"""

    id: str
    self_uri: str
    size: int
    created_time: str
    checksums: list

    def __json__(self) -> t.Dict[str, t.Any]:
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

    def __json__(self) -> t.Dict[str, str]:
        """JSON-renderer for this object."""
        return {"url": self.url}


def get_app():
    """Builds the App"""
    api_path = config_settings.api_path

    with Configurator() as config:
        config.include("pyramid_openapi3")
        config.pyramid_openapi3_spec(
            "/workspace/sandbox_storage/openapi.yaml", route=api_path + "openapi.yaml"
        )
        config.pyramid_openapi3_add_explorer(api_path)

        config.add_route("hello", "/")
        config.add_route("health", "/health")

        config.add_route("objects_id", api_path + "/objects/{object_id}")
        config.add_route(
            "objects_id_access_id", api_path + "/objects/{object_id}/access/{access_id}"
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

    db = get_session()
    target_object = (
        db.query(DrsObject).filter(DrsObject.drs_id == object_id).one_or_none()
    )

    if target_object is not None:
        return DrsReturnObject(
            id=target_object.drs_id,
            self_uri=config_settings.drs_path + target_object.drs_id,
            size=target_object.size,
            created_time=target_object.created_time.isoformat() + "Z",
            checksums=[
                {
                    "checksum": target_object.checksum_md5,
                    "type": "md5",
                }
            ],
        )

    raise HTTPNotFound(
        json={"msg": "The requested 'DrsObject' wasn't found", "status_code": 404}
    )


@view_config(
    route_name="objects_id_access_id",
    renderer="json",
    openapi=True,
    request_method="GET",
)
def get_objects_id_access_id(request: Request):
    """Get a URL for fetching bytes."""
    # Needed for next PR
    # object_id = request.matchdict["object_id"]
    # access_id = request.matchdict["access_id"]

    return AccessURL(url="https://drs.access.dummy")


@view_config(route_name="health", renderer="json", openapi=False, request_method="GET")
def get_health(context, request):
    """Health check"""
    return {"status": "OK"}
