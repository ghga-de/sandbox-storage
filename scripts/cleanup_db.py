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

import transaction
import zope.sqlalchemy

from sandbox_storage.dao.db import get_session
from sandbox_storage.dao.db_models import DrsObject


def cleanup_database():
    """
    Remove all DRS objects from the Database
    """

    with transaction.manager:
        db = get_session()
        zope.sqlalchemy.register(db, transaction.manager)

        drs_objects = db.query(DrsObject).all()
        for drs_object in drs_objects:
            db.delete(drs_object)

        db.flush()


if __name__ == "__main__":
    cleanup_database()
