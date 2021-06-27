# Copyright 2021 Universität Tübingen, DKFZ for the German Human Genome-Phenome Archive (GHGA)
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

from os import strerror
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import typer
from typing import Optional


@view_config(route_name="hello", renderer='json')
def hello_world(request):
    return {'content': 'Hello World!'}

@view_config(route_name="objects_id", renderer='json')
def get_objects_id(request):
    drs_id = request.matchdict['DRS_ID']
    return {'DRS_ID_': drs_id}

@view_config(route_name="objects_id_access_id", renderer='json')
def get_objects_id_access_id(request):
    drs_id = request.matchdict['DRS_ID']
    access_id = request.matchdict['access_id']
    return {'DRS_ID': drs_id, 'access_id': access_id}

def run(
    config: Optional[str] = typer.Option(
        None,
        help = "Path to config yaml."
    )
):
    """Starts backend server
    """
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello', renderer='json')
        config.add_route('objects_id', '/objects/{DRS_ID}')
        config.add_view(get_objects_id, route_name='objects_id', renderer='json')
        config.add_route('objects_id_access_id', '/objects/{DRS_ID}/access/{access_id}')
        config.add_view(get_objects_id_access_id, route_name='objects_id_access_id', renderer='json')
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 8080, app)
    server.serve_forever()

def run_cli():
    typer.run(run)

if __name__ == "__main__":
    run_cli()