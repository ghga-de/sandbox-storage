# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)

"""
Entrypoint for the package.
"""

from wsgiref.simple_server import make_server
from .config import get_config
from .api import get_app

app = get_app()
config = get_config()


def run() -> None:
    """
    Starts backend server
    """
    server = make_server(config.host, config.port, app)
    server.serve_forever()


if __name__ == "__main__":
    run()
