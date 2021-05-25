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

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def index():
    return ('Hello World')

@app.get('/objects/{DRS_ID}')
def get_objects_id(DRS_ID: str):
    return {'DRS_ID': DRS_ID}

@app.get('/objects/{DRS_ID}/access/{access_id}')
def get_objects_id_access_id(DRS_ID: str, access_id: str):
    return {'DRS_ID': DRS_ID, 'access_id': access_id}


def main():
    """Starts backend server
    """
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        log_level="info"
    )


if __name__ == "__main__":
    main()