#!/usr/bin/env python3

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

import hashlib
from datetime import datetime
from os import listdir
from os.path import getctime, getsize, isfile, join
from pathlib import Path

import boto3
import transaction
import zope.sqlalchemy
from sqlalchemy.exc import IntegrityError

from sandbox_storage.config import get_config
from sandbox_storage.dao.db import get_session
from sandbox_storage.dao.db_models import DrsObject

HERE = Path(__file__).parent.resolve()
DIR_PATH = HERE.parent.resolve() / "examples"
S3_URL = get_config().s3_url

path = "http://s3-localstack:4566/test/"

# Connect to s3
s3 = boto3.resource(  # pylint: disable=invalid-name
    service_name="s3",
    endpoint_url=S3_URL,
)
