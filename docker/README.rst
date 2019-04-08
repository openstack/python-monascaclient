===============================
Docker image for Monasca Client
===============================
The Monasca Client image is based on the monasca-base image.


Building monasca-base image
===========================
See https://github.com/openstack/monasca-common/tree/master/docker/README.rst


Building Monasca Client image
=============================

Example:
  $ ./build_image.sh <repository_version> <upper_constains_branch> <common_version>


Requirements from monasca-base image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
health_check.py
  This file will be used for checking the status of the Monasca API
  application.


Scripts
~~~~~~~
start.sh
    In this starting script provide all steps that lead to the proper service
    start. Including usage of wait scripts and templating of configuration
    files. You also could provide the ability to allow running container after
    service died for easier debugging.

build_image.sh
    Please read detailed build description inside the script.


Docker Compose
~~~~~~~~~~~~~~
When you want to use docker-compose add it as a new service and be sure that
property 'tty' is set to true to avoid exiting of container after startup.
Example:

    * monasca-client:
        * image: monasca/client:master
        * tty: true

Running
~~~~~~~
If you don't want to use docker-compose mechanism, you can run container manually
and connect it to existing docker Monasca network.
Example:
    docker network --network=<network-name> <container_name>

You can also use docker run option to start a container and connect it to a network immediately:
Example:
    docker run -itd --network=<network-name> <container-name>

Inside of container it is possible to run 'monasca' shell commands, e.g. to list all metrics.
Example:
    monasca metric-list

Links
~~~~~
https://docs.openstack.org/python-monascaclient/latest/
