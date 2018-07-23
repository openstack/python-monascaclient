=====
Usage
=====

Devstack
--------

python-monascaclient is bundled inside `Monasca API Devstack Plugin`_ and is
available right after the devstack finished stacking up. It is always built
from the **master** branch, unless specified otherwise.

Docker
------

The client is also part of `monasca-docker`_, a community effort to put
**monasca** into containers. The image is available as **monasca/client** and
can be used as drop-in replacement for traditional way of
deploying the clients.

.. _Monasca API Devstack Plugin: https://github.com/openstack/monasca-api/tree/master/devstack
.. _monasca-docker: https://github.com/monasca/monasca-docker/tree/master/monasca-client
