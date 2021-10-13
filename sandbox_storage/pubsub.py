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
Consuming or Subscribing to Async Messaging Topics
"""

import pika
from ghga_service_chassis_lib.pubsub import AmqpTopic
from .config import get_config


def get_connection_params() -> pika.ConnectionParameters:
    """
    Return a configuration object for pika

    Returns:
        An instance of ``pika.ConnectionParameters``

    """
    config = get_config()
    return pika.ConnectionParameters(
        host=config.rabbitmq_host, port=config.rabbitmq_port
    )


def send_message(drs_id: str, access_id: str, user_id: str) -> None:
    """
    Send a message when download request arrives

    Args:
        drs_id: the DRS ID for the file object
        access_id: the access ID for the file object
        user_id: the user ID

    """

    config = get_config()
    message = {"drs_id": drs_id, "access_id": access_id, "user_id": user_id}
    topic = AmqpTopic(
        connection_params=get_connection_params(),
        topic_name=config.topic_name_download_requested,
        service_name="storage",
    )
    topic.publish(message)
