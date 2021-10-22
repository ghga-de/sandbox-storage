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
import logging
import requests
from os import listdir, remove
from os.path import isfile, join
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


HERE = Path(__file__).parent.resolve()
DIR_PATH = HERE.parent.resolve() / "examples/files"
TEMP_PATH = HERE.parent.resolve() / "temp"
S3_URL = "http://s3-localstack:4566"


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


def s3_connect():
    # Connect to s3
    s3 = boto3.client(  # pylint: disable=invalid-name
        service_name="s3",
        endpoint_url=S3_URL,
    )

    return s3


def create_bucket(s3, bucket_name):
    # Create bucket
    s3_bucket = s3.create_bucket(Bucket=bucket_name)

    return s3_bucket


def create_presigned_post(
    s3_client, bucket_name, object_name, fields=None, conditions=None, expiration=3600
):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    try:
        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


def upload_file(file, url, fields, md5_checksum):

    # Demonstrate how another Python program can use the presigned URL to upload a file
    with open(join(DIR_PATH, file), "rb") as f:

        files = {"file": (file, f)}
        headers = {"ContentMD5": md5_checksum}
        http_response = requests.post(url, fields, files=files, headers=headers)

        return http_response


def remove_bucket(bucket_name):

    # Connect to s3
    s3_client = boto3.resource(
        service_name="s3",
        endpoint_url=S3_URL,
    )

    # Remove test files from bucket
    bucket = s3_client.Bucket(bucket_name)

    try:
        bucket.objects.all().delete()
        bucket.delete()
    except ClientError:
        print(f"No such bucket: {bucket_name}")


def check_successfull_upload(s3_client, bucket_name, key, md5_checksum):

    # event_system = s3_client.meta.events
    # event_system.register_first("before-sign..*", _add_header)

    try:
        object_metadata = s3_client.head_object(
            Bucket=bucket_name,
            Key=key,
        )
    except ClientError:
        return False

    etag = object_metadata["ResponseMetadata"]["HTTPHeaders"]["etag"]
    etag = etag.strip('"')
    if etag == md5_checksum:
        print(f"File {key} was successfully uploaded to bucket {bucket_name}.")
        return True
    else:
        print(f"Checksum didn't match.")
        return False


def run():
    # Connect to S3
    s3_client = s3_connect()

    # Create buckets
    create_bucket(s3_client, "inbox")
    create_bucket(s3_client, "outbox")

    files = [file for file in listdir(DIR_PATH) if isfile(join(DIR_PATH, file))]

    for file in files:
        # Generate a presigned S3 POST URL
        presigend_post = create_presigned_post(s3_client, "inbox", file)
        if presigend_post is None:
            exit(1)

        file_path = join(DIR_PATH, file)

        md5_checksum = md5(file_path)

        while not check_successfull_upload(s3_client, "inbox", file, md5_checksum):
            # Upload file using presigned url
            response = upload_file(
                file,
                presigend_post["url"],
                presigend_post["fields"],
                md5_checksum,
            )

        # Copy to other bucket
        copy_source = {
            "Bucket": "inbox",
            "Key": file,
        }

        while not check_successfull_upload(s3_client, "outbox", file, md5_checksum):
            # Try to copy to other bucket
            s3_client.copy(copy_source, "outbox", file)

        # Delete file from inbox
        s3_client.delete_object(
            Bucket="inbox",
            Key=file,
        )

        # Get presigned URL
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": "outbox", "Key": file},
            ExpiresIn=3600,
        )

        if presigned_url is not None:
            response = requests.get(presigned_url)
            if response.status_code == 200:

                with open(f"./temp/{file}", "wb") as new_file:
                    new_file.write(response.content)
                    new_file.close()

                    new_checksum = md5(f"./temp/{file}")

                if md5_checksum == new_checksum:
                    path = "http://localhost:4566" + presigned_url.removeprefix(S3_URL)
                    print(f"It worked. Presigned url: {path}")
                else:
                    print("Chechsum Wrong")
            else:
                print("File Request did not work")
        else:
            print("Presigned URL is None")

    # cleanup()


def cleanup():
    remove_temp_files()
    remove_bucket("inbox")
    remove_bucket("outbox")


def remove_temp_files():
    files = [file for file in listdir(TEMP_PATH) if isfile(join(TEMP_PATH, file))]

    for file in files:
        remove(join(TEMP_PATH, file))


if __name__ == "__main__":
    run()
