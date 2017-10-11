=================
Using monasca CLI
=================

The **monasca** shell utility interacts with OpenStack Monitoring API from the
command-line. It supports the entire features of OpenStack Monitoring API.

Basic Usage
-----------

In order to use the CLI, you must provide your OpenStack username, password,
project, domain information for both user and project, and auth endpoint. Use
the corresponding configuration options (``--os-username``, ``--os-password``,
``--os-project-name``, ``--os-user-domain-id``, ``os-project-domain-id``, and
``--os-auth-url``), but it is easier to set them in environment variables.

.. code-block:: shell

    export OS_USERNAME=mini-mon
    export OS_PASSWORD=password
    export OS_PROJECT_NAME=mini-mon
    export OS_USER_DOMAIN_ID=default
    export OS_PROJECT_DOMAIN_ID=default
    export OS_AUTH_URL=http://keystone:5000/v3

If you are using Identity v2.0 API (DEPRECATED), you don't need to pass domain
information.

.. code-block:: shell

    export OS_USERNAME=mini-mon
    export OS_PASSWORD=password
    export OS_TENANT_NAME=mini-mon
    export OS_AUTH_URL=http://keystone:5000/v2.0

Once you've configured your authentication parameters, you can run **monasca**
commands.  All commands take the form of:

.. code-block:: text

    monasca <command> [arguments...]

Run **monasca help** to get a full list of all possible commands, and run
**monasca help <command>** to get detailed help for that command.

Using with os-client-config
~~~~~~~~~~~~~~~~~~~~~~~~~~~

`os-client-config <https://docs.openstack.org/os-client-config/latest/>`_
provides more convenient way to manage a collection of client configurations
and you can easily switch multiple OpenStack-based configurations.

To use os-client-config, you first need to prepare
``~/.config/openstack/clouds.yaml`` like the following.

.. code-block:: yaml

    clouds:
      monitoring:
        auth:
          auth_url: http://keystone:5000
          password: password
          project_domain_id: default
          project_name: mini-mon
          user_domain_id: default
          username: mini-mon
        identity_api_version: '3'
        region_name: RegionOne

Then, you need to specify a configuration name defined in the above
clouds.yaml.

.. code-block:: shell

    export OS_CLOUD=monitoring

For more detail information, see the
`os-client-config <https://docs.openstack.org/os-client-config/latest/>`_
documentation.

Using with keystone token
~~~~~~~~~~~~~~~~~~~~~~~~~

The command-line tool will attempt to re-authenticate using your provided
credentials for every request. You can override this behavior by manually
supplying an auth token using ``--os-url`` and ``--os-auth-token``. You can
alternatively set these environment variables.

.. code-block:: shell

    export OS_URL=http://monasca.example.org:8070/
    export OS_TOKEN=3bcc3d3a03f44e3d8377f9247b0ad155
