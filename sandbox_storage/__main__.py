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
import pyramid_openapi3
from typing import Optional
from .config import get_settings

settings = get_settings()

from .api import (
        index,
        get_health,
        get_objects_id,
        get_objects_id_access_id,
        get_app,
    )
    
def run():
    """Starts backend server
    """

    server = make_server(settings.host, settings.port, get_app())
    server.serve_forever()

if __name__ == "__main__":
    run()
    