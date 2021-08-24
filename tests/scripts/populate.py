#!/usr/bin/env python3

# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)

# Can't populate S3 yet
# So, just take example files and hard links right now

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

from sandbox_storage.database import get_session
from sandbox_storage.models import DrsObject
from sandbox_storage.config import get_config


HERE = Path(__file__).parent.resolve()
DIR_PATH = HERE.parent.resolve() / "examples"
TEST_FILE_PATH = get_config().examples_path


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


def populate_database():
    """
    Populates the database by retrieving the required attributes
    and then making a commit to the database
    """

    files = [file for file in listdir(DIR_PATH) if isfile(join(DIR_PATH, file))]

    # TODO:
    # Connect to s3
    # Create bucket "test"

    for file in files:
        # Get full path
        file_path = join(DIR_PATH, file)

        # Get file size
        size = getsize(file_path)

        # Get creation time
        created_time = datetime.fromtimestamp(getctime(file_path)).isoformat()

        # Get md5 checksum
        checksum_md5 = md5(file_path)

        # Get downloadable path
        path = join(TEST_FILE_PATH, file)

        # TODO:
        # Upload file to "test" bucket
        # check return for correct checksum
        # find out what the file url will be

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

    # TODO: connect to s3, remove bucket "test"


if __name__ == "__main__":
    populate_database()
