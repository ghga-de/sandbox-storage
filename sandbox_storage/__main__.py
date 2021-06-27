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

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import typer
from typing import Optional


def hello_world(request):
    return Response('Hello World!')

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
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 8080, app)
    server.serve_forever()

def run_cli():
    typer.run(run)

if __name__ == "__main__":
    run_cli()