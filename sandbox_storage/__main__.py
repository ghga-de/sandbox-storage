# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
"""Entrypoint for the Package"""

from wsgiref.simple_server import make_server
from .config import get_settings

settings = get_settings()

from .api import get_app


def run():
    """Starts backend server"""

    server = make_server(settings.host, settings.port, get_app())
    server.serve_forever()

if __name__ == "__main__":
    run()
