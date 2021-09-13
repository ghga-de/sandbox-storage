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


# This script is currently not in use and might be broken

"""
Provides a script function to populate a database
"""

from datetime import datetime
from pathlib import Path
from os import listdir
from os.path import isfile, join, getsize, getctime
import hashlib
from sqlalchemy.exc import IntegrityError
import transaction
import zope.sqlalchemy
import boto3

from sandbox_storage.database import get_session
from sandbox_storage.models import DrsObject
from sandbox_storage.config import get_config


HERE = Path(__file__).parent.resolve()
DIR_PATH = HERE.parent.resolve() / "examples"
S3_URL = get_config().s3_url


def md5(fname):
    """
    Returns md5 checksum of a file by cutting it in parts of 4096 bytes each
    The Hash is not used in a secure context, but to provide a checksum
    """
    hash_md5 = hashlib.md5()  # nosec
    with open(fname, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# pylint: disable=duplicate-code
def populate_database():
    """
    Populates the database by retrieving the required attributes
    and then making a commit to the database
    """

    files = [file for file in listdir(DIR_PATH) if isfile(join(DIR_PATH, file))]

    # Connect to s3
    s3 = boto3.resource(  # pylint: disable=invalid-name
        service_name="s3",
        endpoint_url=S3_URL,
    )

    # Remove remnants of previous tests
    s3_bucket = s3.Bucket("test")
    if s3_bucket:
        s3_bucket.objects.all().delete()
    else:
        # Create bucket "test" if it does not exist
        s3_bucket = s3.create_bucket(Bucket="test")

    for file in files:
        # Get full path
        file_path = join(DIR_PATH, file)

        # Get file size
        size = getsize(file_path)

        # Get creation time
        created_time = datetime.fromtimestamp(getctime(file_path)).isoformat()

        # Get md5 checksum
        checksum_md5 = md5(file_path)

        # Upload file to "test" bucket
        s3_bucket.upload_file(file_path, file)

        # Build file path
        path = "http://s3-localstack:4566/test/" + file

        try:
            # Create Object in Database
            drs_object = DrsObject(
                drs_id=file,
                path=path,
                size=size,
                created_time=created_time,
                checksum_md5=checksum_md5,
            )
            with transaction.manager:
                db = get_session()
                zope.sqlalchemy.register(db, transaction.manager)
                db.add(drs_object)
                db.flush()
        except IntegrityError as exception:
            raise exception


def remove_test_files():
    """
    Removes the created test files
    """

    with transaction.manager:
        db = get_session()
        zope.sqlalchemy.register(db, transaction.manager)
        db.query(DrsObject).filter(DrsObject.drs_id.like("Test%")).delete(
            synchronize_session=False
        )
        db.flush()

    # Connect to s3
    s3_client = boto3.resource(
        service_name="s3",
        endpoint_url=S3_URL,
    )

    # Remove test files from bucket
    bucket = s3_client.Bucket("test")
    if bucket:
        bucket.objects.all().delete()


if __name__ == "__main__":
    populate_database()
