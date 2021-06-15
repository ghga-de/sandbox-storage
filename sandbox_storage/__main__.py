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

import uvicorn
import typer
from fastapi import FastAPI
from typing import Optional

from .config import get_settings

settings = get_settings()
app = FastAPI()


def run(
    config: Optional[str] = typer.Option(
        None,
        help = "Path to config yaml."
    )
):
    """Starts backend server
    """
    global settings
    if config:
        # overwrite settings
        settings = get_settings(config_yaml=config)
    
    from .api import index, get_objects_id, get_objects_id_access_id
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level
    )


def run_cli():
    typer.run(run)

if __name__ == "__main__":
    run_cli()


@app.get('/')
def index():
    return ('Hello World')


@app.get('/objects/{DRS_ID}')
def get_objects_id(DRS_ID: str):
    return {'DRS_ID': DRS_ID}


@app.get('/objects/{DRS_ID}/access/{access_id}')
def get_objects_id_access_id(DRS_ID: str, access_id: str):
    return {'DRS_ID': DRS_ID, 'access_id': access_id}

