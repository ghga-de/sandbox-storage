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
from datetime import datetime
from os import listdir
from os.path import getctime, getsize, isfile, join
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from sandbox_storage.config import get_config

HERE = Path(__file__).parent.resolve()
DIR_PATH = HERE.parent.resolve() / "examples"
S3_URL = "http://s3-localstack:4566"


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
    bucket_name, object_name, fields=None, conditions=None, expiration=3600
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
    s3_client = boto3.client("s3")
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


def run():

    files = [file for file in listdir(DIR_PATH) if isfile(join(DIR_PATH, file))]

    # Generate a presigned S3 POST URL
    object_name = "OBJECT_NAME"
    response = create_presigned_post("BUCKET_NAME", object_name)
    if response is None:
        exit(1)

    # Demonstrate how another Python program can use the presigned URL to upload a file
    with open(object_name, "rb") as f:
        files = {"file": (object_name, f)}
        http_response = requests.post(
            response["url"], data=response["fields"], files=files
        )
    # If successful, returns HTTP status code 204
    logging.info(f"File upload HTTP status code: {http_response.status_code}")
