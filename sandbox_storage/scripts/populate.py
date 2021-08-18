# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)

# Can't populate S3 yet
# So, just take example files and hard links right now

from datetime import datetime
from sandbox_storage.database import get_session
from sandbox_storage.config import get_settings
from sandbox_storage.models import DrsObject

from sqlalchemy.exc import IntegrityError
from os import listdir
from os.path import isfile, join, getsize, getctime
import time
import hashlib
from datetime import datetime


settings = get_settings()
dir_path = settings.example_files_path


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# def populate_database():

files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

for file in files:
    # Get full path
    file_path = join(dir_path, file)

    # Get file size
    size = getsize(file_path)

    # Get creation time
    created_time = datetime.fromtimestamp(getctime(file_path)).isoformat()

    # Get md5 checksum
    checksum_md5 = md5(file_path)

    # Get database
    db = get_session()

    # Get downloadable path
    path = join("https://github.com/ghga-de/sandbox-storage/raw/dev/", file_path)

    try:
        drs_object = DrsObject(
            drs_id=file,
            path=path,
            size=size,
            created_time=created_time,
            checksum_md5=checksum_md5,
        )
        db.add(drs_object)
        db.flush()
    except IntegrityError as e:
        raise e
