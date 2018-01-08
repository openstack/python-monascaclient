================
Using Python API
================

Python bindings to the OpenStack Monasca API
============================================

This is a client for the OpenStack Monasca API. It includes a Python
API (the :mod:`monascaclient` module) and a command-line script
(installed as :program:`monasca`).

Python API
==========

To use python-monascaclient in a project, you need to create a client instance
first. There are couple ways of doing this properly.

With session
------------

A pseudo-code would be similar to this::

  from keystoneauth1 import identity
  from keystoneauth1 import session
  from monascaclient import client

  auth = identity.Password(
    auth_url='http://my.keystone.com/identity',
    username='mini-mon',
    password='password',
    project_name='mini-mon',
    user_domain_id='default',
    project_domain_id='default'
  )
  sess = session.Session(auth=auth)

  endpoint = 'http://monasca:8070/v2.0'
  api_version = '2_0'

  c = client.Client(
    api_version=api_version,
    endpoint=endpoint,
    session=sess
  )

  c.alarms.list()

For more information on keystoneauth API, see `Using Sessions`_. We also
suggest taking closer look at `Keystone Auth Plugins`_. Each of the plugin
can be used to properly instantiate new session and pass it into the client.

  .. note:: This is recommended way to setup a client.
     Other cases, described below, create sessions internally.


Without session
---------------

If you do not want to use a session or simply prefer client to instantiate
one on its own, there are two supported ways

With token
~~~~~~~~~~

A pseudo-code would be similar to this::

  from monascaclient import client

  c = client.Client(
    api_version='2_0',
    endpoint='http://monasca:8070/v2.0',
    token='3bcc3d3a03f44e3d8377f9247b0ad155',
    project_name='mini-mon',
    auth_url='http://my.keystone.com/identity'
  )

  c.alarms.list()


With username & password
~~~~~~~~~~~~~~~~~~~~~~~~

A pseudo-code would be similar to this::

  from monascaclient import client

  c = client.Client(
    api_version='2_0',
    endpoint='http://monasca:8070/v2.0',
    username='mini-mon',
    password='password',
    project_name='mini-mon',
    auth_url='http://my.keystone.com/identity'
  )

  c.alarms.list()

Examples
========

* `Monasca Agent Example`_ - with session
* `Monasca UI Example`_ - with token

.. _Monasca Agent Example: https://github.com/openstack/monasca-agent/blob/master/monasca_agent/forwarder/api/monasca_api.py
.. _Monasca UI Example: https://github.com/openstack/monasca-ui/blob/master/monitoring/api/client.py
.. _Using Sessions: https://docs.openstack.org/keystoneauth/latest/using-sessions.html
.. _Keystone Auth Plugins: https://docs.openstack.org/keystoneauth/latest/authentication-plugins.html
