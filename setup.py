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

from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent.resolve()
with open(HERE / "README.md") as f:
    README = f.read()

requires = [
    "PyYAML==5.4.1",
    "typer==0.3.2",
    "psycopg2==2.9.1",
    "sqlalchemy==1.4.19",
    "psycopg2==2.9.1",
    "pyramid==2.0",
    "pyramid_beaker==0.8",
    "pyramid_openapi3==0.11",
    "openapi-core==0.13.8",
    "zope.sqlalchemy==1.5",
    "pydantic==1.8.2",
    "ghga-service-chassis-lib[pubsub]==0.3.0",
    "transaction==3.0.1",
]

testing_require = [
    "alembic==1.6.5",
    "pytest",
    "pytest-cov",
    "mypy",
    "pylint",
    "flake8",
    "black",
    "bandit",
]

setup(
    name="sandbox_storage",
    version="0.1.0",
    description=(
        "Sandbox-Storage - a DRS-compliant service for delivering files from S3"
    ),
    long_description=README,
    author="German Human Genome Phenome Archive (GHGA)",
    author_email="contact@ghga.de",
    url="",
    keywords="",
    packages=find_packages(),
    license="Apache 2.0",
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        "testing": testing_require,
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Internet :: WWW/HTTP",
    ],
    entry_points={
        "console_scripts": [
            "sandbox-storage=sandbox_storage.__main__:run",
        ],
    },
)
