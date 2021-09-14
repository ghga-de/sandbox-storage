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
Connect to Database
"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import register
from ..config import get_config

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = get_config().db_url


def get_engine(db_url: str) -> sqlalchemy.engine:
    """
    Get sqlalchemy engine

    Args:
        db_url: the database URL

    Returns:
        An instance of a SQLAlchemy engine

    """
    return create_engine(db_url)


engine = get_engine(SQLALCHEMY_DATABASE_URL)
DBSession = scoped_session(sessionmaker(bind=engine))
register(DBSession)

Base = declarative_base()


def get_session() -> scoped_session:
    """
    Returns the database session

    Returns:
        An instance of ``DBSession``

    """
    return DBSession()
