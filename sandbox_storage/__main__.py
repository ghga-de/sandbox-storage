# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
"""Entrypoint for the Package"""


from typing import Optional
import uvicorn
import typer
from fastapi import FastAPI

from .config import get_settings

settings = get_settings()  # pylint: disable=invalid-name
app = FastAPI()


def run(config: Optional[str] = typer.Option(None, help="Path to config yaml.")):
    """Starts backend server"""
    global settings  # pylint: disable=global-statement,invalid-name
    if config:
        # overwrite settings
        settings = get_settings(config_yaml=config)

    from .api import (  # noqa: F401 pylint: disable=unused-import,import-outside-toplevel
        index,
        get_objects_id,
        get_objects_id_access_id,
    )

    uvicorn.run(
        app, host=settings.host, port=settings.port, log_level=settings.log_level
    )


def run_cli():
    """Run the command line interface"""
    typer.run(run)


if __name__ == "__main__":
    run_cli()
