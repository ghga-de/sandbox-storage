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

"""
Provides a script function to populate the database
with example DRS objects
"""

import json
from pathlib import Path

import transaction
import zope.sqlalchemy

from sandbox_storage.dao.db import get_session
from sandbox_storage.dao.db_models import DrsObject

HERE = Path(__file__).parent.resolve()
DRS_OBJECTS_JSON = HERE.parent.resolve() / "examples" / "drs_objects.json"


def populate_database():
    """
    Populates the database with example DRS objects
    that point to http URLs to files on GitHub
    """

    with open(DRS_OBJECTS_JSON, "r") as drs_object_json:
        drs_objects = json.load(drs_object_json)

    for drs_object in drs_objects:
        # Create Object in Database
        drs_object = DrsObject(
            drs_id=drs_object["drs_id"],
            path=drs_object["path"],
            size=drs_object["size"],
            created_time=drs_object["created_time"],
            checksum_md5=drs_object["checksum_md5"],
        )

        with transaction.manager:
            db = get_session()
            zope.sqlalchemy.register(db, transaction.manager)
            db.add(drs_object)
            db.flush()


if __name__ == "__main__":
    populate_database()
