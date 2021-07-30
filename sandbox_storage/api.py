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

from pyramid.view import view_config

@view_config(route_name="hello", renderer='json', openapi=True, request_method="GET")
def index(request):
    return {'content': 'Hello World!'}

@view_config(route_name="objects_id", renderer='json', openapi=True, request_method="GET")
def get_objects_id(request):
    object_id = request.matchdict['object_id']
    return {'object_id': object_id}

@view_config(route_name="objects_id_access_id", renderer='json', openapi=True, request_method="GET")
def get_objects_id_access_id(request):
    object_id = request.matchdict['object_id']
    access_id = request.matchdict['access_id']
    return {'object_id': object_id, 'access_id': access_id}

# @app.get("/health")
# def index():
#     """Health check"""
#     return {"status": "OK"}


