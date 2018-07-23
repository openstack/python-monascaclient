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

Usage Examples
----------------

metric-create::

  monasca metric-create cpu1 123.40
  monasca metric-create metric1 1234.56 --dimensions instance_id=123,service=ourservice
  monasca metric-create metric1 2222.22 --dimensions instance_id=123,service=ourservice
  monasca metric-create metric1 3333.33 --dimensions instance_id=222,service=ourservice
  monasca metric-create metric1 4444.44 --dimensions instance_id=222 --value-meta rc=404

metric-list::

  monasca metric-list
  +---------+--------------------+
  | name    | dimensions         |
  +---------+--------------------+
  | cpu1    |                    |
  | metric1 | instance_id:123    |
  |         | service:ourservice |
  +---------+--------------------+

measurement-list::

  monasca measurement-list metric1 2014-01-01T00:00:00Z
  +---------+--------------------+----------------+----------------------+--------------+-------------+
  | name    | dimensions         | measurement_id | timestamp            | value        |  value_meta |
  +---------+--------------------+----------------+----------------------+--------------+-------------+
  | metric1 | instance_id:123    |     723885     | 2014-05-08T21:46:32Z |      1234.56 |             |
  |         | service:ourservice |     725951     | 2014-05-08T21:48:50Z |      2222.22 |             |
  | metric1 | instance_id:222    |     726837     | 2014-05-08T21:49:47Z |      3333.33 |             |
  |         | service:ourservice |     726983     | 2014-05-08T21:50:27Z |      4444.44 | rc: 404     |
  +---------+--------------------+----------------+----------------------+--------------+-------------+

  monasca measurement-list metric1 2014-01-01T00:00:00Z --dimensions instance_id=123
  +---------+--------------------+----------------+----------------------+--------------+-------------+
  | name    | dimensions         | measurement_id | timestamp            | value        |  value_meta |
  +---------+--------------------+----------------+----------------------+--------------+-------------+
  | metric1 | instance_id:123    |     723885     | 2014-05-08T21:46:32Z |      1234.56 |             |
  |         | service:ourservice |     725951     | 2014-05-08T21:48:50Z |      2222.22 |             |
  +---------+--------------------+----------------+----------------------+--------------+-------------+


Notifications Examples
~~~~~~~~~~~~~~~~~~~~~~
Note:  To see complete usage: 'monasca help' and 'monasca help <command>'

notification-create::

  monasca notification-create cindyemail1 EMAIL cindy.employee@hp.com
  monasca notification-create myapplication WEBHOOK http://localhost:5000
  monasca notification-create mypagerduty PAGERDUTY nzH2LVRdMzun11HNC2oD

notification-list::

  monasca notification-list
  +---------------+--------------------------------------+-------+----------------------+
  | name          | id                                   | type  | address              |
  +---------------+--------------------------------------+-------+----------------------+
  | cindyemail1   | 5651406c-447d-40bd-b868-b2b3e6b59e32 | EMAIL |cindy.employee@hp.com |
  | myapplication | 55905ce2-91e3-41ce-b45a-de7032f8d718 | WEBHOOK |http://localhost:5000
  | mypagerduty   | 5720ccb5-6a3d-22ba-545g-ce467a5b41a2 | PAGERDUTY |nzH2LVRdMzun11HNC2oD
  +---------------+--------------------------------------+-------+----------------------+


Alarms Examples
~~~~~~~~~~~~~~~
Note:  To see complete usage: 'monasca help' and 'monasca help <command>'

alarm-definition-create::

  monasca alarm-definition-create alarmPerHost "max(cpu.load_avg_1_min) > 0" --match-by hostname

alarm-definition-list::

  +--------------+--------------------------------------+-----------------------------+----------+-----------------+
  | name         | id                                   | expression                  | match_by | actions_enabled |
  +--------------+--------------------------------------+-----------------------------+----------+-----------------+
  | alarmPerHost | 4bf6bfc2-c5ac-4d57-b7db-cf5313b05412 | max(cpu.load_avg_1_min) > 0 | hostname | True            |
  +--------------+--------------------------------------+-----------------------------+----------+-----------------+

alarm-definition-show::

  monasca alarm-definition-show 4bf6bfc2-c5ac-4d57-b7db-cf5313b05412
  +----------------------+----------------------------------------------------------------------------------------------------+
  | Property             | Value                                                                                              |
  +----------------------+----------------------------------------------------------------------------------------------------+
  | actions_enabled      | true                                                                                               |
  | alarm_actions        | []                                                                                                 |
  | description          | ""                                                                                                 |
  | expression           | "max(cpu.load_avg_1_min) > 0"                                                                      |
  | id                   | "4bf6bfc2-c5ac-4d57-b7db-cf5313b05412"                                                             |
  | links                | href:http://192.168.10.4:8070/v2.0/alarm-definitions/4bf6bfc2-c5ac-4d57-b7db-cf5313b05412,rel:self |
  | match_by             | [                                                                                                  |
  |                      |   "hostname"                                                                                       |
  |                      | ]                                                                                                  |
  | name                 | "alarmPerHost"                                                                                     |
  | ok_actions           | []                                                                                                 |
  | severity             | "LOW"                                                                                              |
  | undetermined_actions | []                                                                                                 |
  +----------------------+----------------------------------------------------------------------------------------------------+

alarm-definition-delete::

  monasca alarm-definition-delete 4bf6bfc2-c5ac-4d57-b7db-cf5313b05412

alarm-list::

  monasca alarm-list
  +--------------------------------------+--------------------------------------+----------------+---------------+---------------------+----------+-------+--------------------------+--------------------------+
  | id                                   | alarm_definition_id                  | alarm_name     | metric_name   | metric_dimensions   | severity | state | state_updated_timestamp  | created_timestamp        |
  +--------------------------------------+--------------------------------------+----------------+---------------+---------------------+----------+-------+--------------------------+--------------------------+
  | 11e8c15d-0263-4b71-a8b8-4ecdaeb2902c | af1f347b-cddb-46da-b7cc-924261eeecdf | High CPU usage | cpu.idle_perc | hostname: devstack  | LOW      | OK    | 2015-03-26T21:45:15.000Z | 2015-03-26T21:41:50.000Z |
  | e5797cfe-b66e-4d44-98cd-3c7fc62d4c33 | af1f347b-cddb-46da-b7cc-924261eeecdf | High CPU usage | cpu.idle_perc | hostname: mini-mon  | LOW      | OK    | 2015-03-26T21:43:15.000Z | 2015-03-26T21:41:47.000Z |
  |                                      |                                      |                |               | service: monitoring |          |       |                          |                          |
  +--------------------------------------+--------------------------------------+----------------+---------------+---------------------+----------+-------+--------------------------+--------------------------+

alarm-history::

  monasca alarm-history 9d748b72-939b-45e7-a807-c0c5ad88d3e4
  +--------------------------------------+-----------+--------------+------------------------------------------------------------------------------+-------------+--------------------+---------------------+--------------------------+
  | alarm_id                             | new_state | old_state    | reason                                                                       | reason_data | metric_name        | metric_dimensions   | timestamp                |
  +--------------------------------------+-----------+--------------+------------------------------------------------------------------------------+-------------+--------------------+---------------------+--------------------------+
  | 9d748b72-939b-45e7-a807-c0c5ad88d3e4 | ALARM     | UNDETERMINED | Thresholds were exceeded for the sub-alarms: [max(cpu.load_avg_1_min) > 0.0] | {}          | cpu.load_avg_1_min | hostname: mini-mon  | 2014-10-14T21:14:11.000Z |
  |                                      |           |              |                                                                              |             |                    | service: monitoring |                          |
  +--------------------------------------+-----------+--------------+------------------------------------------------------------------------------+-------------+--------------------+---------------------+--------------------------+


alarm-patch::

  monasca alarm-patch fda5537b-1550-435f-9d6c-262b7e05065b --state OK
