# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)

"""Entrypoint for the Package"""

from wsgiref.simple_server import make_server
from .config import get_settings
from .api import get_app

app = get_app()
settings = get_settings()


def run():
    """Starts backend server"""

    server = make_server(settings.host, settings.port, app)
    server.serve_forever()


if __name__ == "__main__":
    run()
