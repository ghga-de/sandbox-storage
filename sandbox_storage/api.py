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

@view_config(route_name="hello", renderer='json', openapi="true")
def index(request):
    return {'content': 'Hello World!'}

@view_config(route_name="objects_id", renderer='json', openapi="true")
def get_objects_id(request):
    drs_id = request.matchdict['DRS_ID']
    return {'DRS_ID_': drs_id}

@view_config(route_name="objects_id_access_id", renderer='json', openapi="true")
def get_objects_id_access_id(request):
    drs_id = request.matchdict['DRS_ID']
    access_id = request.matchdict['access_id']
    return {'DRS_ID': drs_id, 'access_id': access_id}
