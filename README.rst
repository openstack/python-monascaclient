========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/python-monascaclient.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

Python bindings to the Monasca API
=======================================

This is a client library for Monasca built to interface with the Monasca API. It
provides a Python API (the ``monascaclient`` module) and a command-line tool
(``monasca``).

The Monasca Client was written using the OpenStack Heat Python client as a framework.

.. contents:: Contents:
   :local:

Ubuntu Install
--------------
Requires:
  - pip - version >= 1.4.  python get-pip.py

See versions on PYPI:
  https://pypi.org/project/python-monascaclient/

Install It:
  - sudo pip install python-monascaclient

Alternative Manual Install Steps:
  - cd to your python-monascaclient repo
  - sudo pip install -r requirements.txt
  - python setup.py install

Building and Packaging
----------------------
Install the tool dependencies
    sudo apt-get install python-pip python-virtualenv

In the python-monascaclient source directory
    virtualenv --no-site-packages .venv

    source ./.venv/bin/activate

    pip install wheel

    python setup.py bdist_wheel

    pip install $(ls -1rt dist/*.whl | tail -1) --upgrade

Command-line API
----------------
Installing this distribution gets you a shell command, ``monasca``, that you
can use to interact with the Monitoring API server.

Usage:
  monasca

  monasca help

  monasca help <command>

    This outputs the results in json format.  Normally output is in table format.


The monascaclient CLI needs the Monasca API endpoint url and the OS_AUTH_TOKEN to pass to the
Monasca API RESTful interface.  This is provided through environment or CLI
parameters.

Environmental Variables
=======================

Environmental variables can be sourced, or optionally passed in as CLI arguments.
It is easiest to source them first and then use the CLI.

When token and endpoint are known::

  export OS_AUTH_TOKEN=XXX
  export MONASCA_API_URL=http://192.168.10.4:8070/v2.0/

When using Keystone to obtain the token and endpoint::

  export OS_USERNAME=
  export OS_PASSWORD=
  export OS_USER_DOMAIN_NAME=
  export OS_PROJECT_NAME=
  export OS_AUTH_URL=
  export OS_REGION_NAME=
  # Optional(specific version added to OS_AUTH_URL if (v2.0 or v3) not present already)
  export OS_AUTH_VERSION=

When OS_USER_DOMAIN_NAME is not set, then 'Default' is assumed. Alternatively IDs can be used instead of names.
Although *deprecated*, but OS_TENANT_NAME and OS_TENANT_ID can be used for
OS_PROEJCT_NAME and OS_PROJECT_ID respectively.

When using Vagrant Environment with middleware disabled::

  export OS_AUTH_TOKEN=82510970543135
  export OS_NO_CLIENT_AUTH=1
  export MONASCA_API_URL=http://192.168.10.4:8070/v2.0/

The Monasca API will treat the auth token as the tenant ID when Keystone is not enabled.

License
=======

(C) Copyright 2014-2016 Hewlett Packard Enterprise Development LP
Copyright 2017 Fujitsu LIMITED

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.
See the License for the specific language governing permissions and
limitations under the License.
