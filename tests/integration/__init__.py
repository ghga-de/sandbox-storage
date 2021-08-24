# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Package containing integration tests.
The __init__ module contains a skeleton of the test framework.
"""


import unittest
from webtest import TestApp

import transaction
from sqlalchemy_utils import create_database, drop_database, database_exists

from sandbox_storage.config import get_config
from sandbox_storage.database import Base, get_engine, get_session
from sandbox_storage.api import get_app

from ..scripts.populate import populate_database, remove_test_files

from .fixtures import db_url


class BaseIntegrationTest(unittest.TestCase):
    """Base TestCase to inherit from"""

    def initDb(self):
        # create database from scratch:
        if database_exists(db_url):
            drop_database(db_url)
        create_database(db_url)

        # get engine and session factory
        self.session_factory = get_session
        self.engine = get_engine(db_url)

        # create models:
        Base.metadata.create_all(self.engine)

    def setUp(self):
        """Setup Test Server"""
        self.config = get_config()

        # initialize DB and provide metadata and file fixtures
        self.initDb()
        populate_database()

        app = get_app(config_settings=self.config)
        self.testapp = TestApp(app)

    def tearDown(self):
        """Teardown Test Server"""
        transaction.abort()
        remove_test_files()
        drop_database(db_url)
        del self.testapp
