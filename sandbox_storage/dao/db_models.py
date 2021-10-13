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
Database Models
"""

from sqlalchemy import Column, Integer, String, DateTime
from .db import Base


class DrsObject(Base):
    """
    GA4GH DRS Object that links to an S3 object.
    """

    __tablename__ = "drs_objects"
    id = Column(Integer, primary_key=True)
    drs_id = Column(String, nullable=False, unique=True)
    path = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    created_time = Column(DateTime, nullable=False)
    checksum_md5 = Column(String, nullable=False)
