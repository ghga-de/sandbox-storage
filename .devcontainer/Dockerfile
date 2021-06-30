# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.177.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Install other dependencies:
RUN apt update -qq -y \
    && apt install -y \
        postgresql-client

# Copy install and launcher script to bin:
COPY ./dev_install /bin
COPY ./dev_launcher /bin
