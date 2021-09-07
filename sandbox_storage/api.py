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

"""
Provides the API endpoints for storage.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

from pyramid.events import NewRequest
from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

import boto3

from .cors import cors_header_response_callback_factory
from .config import get_config
from .database import get_session
from .models import DrsObject
from .pubsub import send_message

CONFIG_SETTINGS = get_config()
S3_PATH = CONFIG_SETTINGS.s3_path


@dataclass
class DrsReturnObject:
    """A DrsObject"""

    id: str
    self_uri: str
    size: int
    created_time: str
    checksums: list

    def __json__(self, _: Request) -> Dict[str, Any]:
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

    def __json__(self, _: Request) -> Dict[str, str]:
        """JSON-renderer for this object."""
        return {"url": self.url}


def get_app(config_settings=CONFIG_SETTINGS) -> Any:
    """
    Builds the Pyramid app

    Args:
        config_settings: Settings for the application

    Returns:
        An instance of Pyramid WSGI app

    """
    api_path = config_settings.api_path
    openapi_spec_path = Path(__file__).parent / "openapi.yaml"
    with Configurator() as pyramid_config:
        pyramid_config.add_subscriber(
            cors_header_response_callback_factory(config_settings), NewRequest
        )
        pyramid_config.include("pyramid_openapi3")
        pyramid_config.pyramid_openapi3_spec(
            openapi_spec_path, route=api_path + "openapi.yaml"
        )
        pyramid_config.pyramid_openapi3_add_explorer(api_path)

        pyramid_config.add_route("hello", "/")
        pyramid_config.add_route("health", "/health")

        pyramid_config.add_route("objects_id", api_path + "/objects/{object_id}")
        pyramid_config.add_route(
            "objects_id_access_id", api_path + "/objects/{object_id}/access/{access_id}"
        )
        pyramid_config.scan(".")
    return pyramid_config.make_wsgi_app()


@view_config(route_name="hello", renderer="json", openapi=False, request_method="GET")
def index(_, __):
    """
    Index Enpoint, returns 'Hello World'
    """
    return {"content": "Hello World!"}


@view_config(
    route_name="objects_id", renderer="json", openapi=True, request_method="GET"
)
def get_objects_id(request: Request) -> DrsReturnObject:
    """
    Get info about a ``DrsObject``.

    Args:
        request: An instance of ``pyramid.request.Request``

    Returns:
        An instance of ``DrsReturnObject``

    """
    object_id = request.matchdict["object_id"]
    db = get_session()
    target_object = (
        db.query(DrsObject).filter(DrsObject.drs_id == object_id).one_or_none()
    )
    if target_object is not None:
        return DrsReturnObject(
            id=target_object.drs_id,
            self_uri=CONFIG_SETTINGS.drs_path + target_object.drs_id,
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
def get_objects_id_access_id(request: Request) -> AccessURL:
    """
    Get a URL for fetching bytes.

    Args:
        request: An instance of ``pyramid.request.Request``

    Returns:
        An instance of ``AccessURL``

    """

    object_id = request.matchdict["object_id"]
    access_id = request.matchdict["access_id"]

    db = get_session()
    target_object = (
        db.query(DrsObject).filter(DrsObject.drs_id == object_id).one_or_none()
    )

    if target_object is None:
        raise HTTPBadRequest(
            json={"msg": "The requested 'DrsObject' wasn't found", "status_code": 400}
        )

    if access_id == "s3":
        send_message(object_id, access_id, "user_id")

        # Connect to s3
        s3_client = boto3.client(
            service_name="s3",
            endpoint_url=S3_PATH,
        )

        # Get presigned URL
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": "test", "Key": object_id},
            ExpiresIn=86400,
        )

        # change path to localhost
        path = "http://localhost:4566" + response.removeprefix(CONFIG_SETTINGS.s3_path)

        return AccessURL(url=path)

    raise HTTPBadRequest(
        json={"msg": "The requested access method does not exist", "status_code": 400}
    )


@view_config(route_name="health", renderer="json", openapi=False, request_method="GET")
def get_health(_, __):
    """
    Check for the health of the service.
    """
    return {"status": "OK"}
