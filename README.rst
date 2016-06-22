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
  https://pypi.python.org/pypi/python-monascaclient/

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

  monasca -j <command>

    This outputs the results in json format.  Normally output is in table format.


The monascaclient CLI needs the Monasca API endpoint url and the OS_AUTH_TOKEN to pass to the
Monasca API RESTful interface.  This is provided through environment or CLI
parameters.

Environmental Variables
~~~~~~~~~~~~~~~~~~~~~~~

Environmental variables can be sourced, or optionally passed in as CLI arguments.
It is easiest to source them first and then use the CLI.

When token and endpoint are known::

  export OS_AUTH_TOKEN=XXX
  export MONASCA_API_URL=http://192.168.10.4:8080/v2.0/

When using Keystone to obtain the token and endpoint::

  export OS_USERNAME=
  export OS_PASSWORD=
  export OS_USER_DOMAIN_NAME=
  export OS_PROJECT_NAME=
  export OS_AUTH_URL=
  export OS_REGION_NAME=

When OS_USER_DOMAIN_NAME is not set, then 'Default' is assumed. Alternatively IDs can be used instead of names.

When using Vagrant Environment with middleware disabled::

  export OS_AUTH_TOKEN=82510970543135
  export OS_NO_CLIENT_AUTH=1
  export MONASCA_API_URL=http://192.168.10.4:8080/v2.0/

The Monasca API will treat the auth token as the tenant ID when Keystone is not enabled.

You'll find complete documentation on the shell by running
``monasca help``::

  usage: monasca [-j] [--version] [-d] [-v] [-k] [--cert-file CERT_FILE]
               [--key-file KEY_FILE] [--os-cacert OS_CACERT]
               [--timeout TIMEOUT] [--os-username OS_USERNAME]
               [--os-password OS_PASSWORD] [--os-project-id OS_PROJECT_ID]
               [--os-user-domain-id OS_USER_DOMAIN_ID] [--os-user-domain-name OS_USER_DOMAIN_NAME]
               [--os-project-name OS_PROJECT_NAME]
               [--os-domain-id OS_DOMAIN_ID] [--os-domain-name OS_DOMAIN_NAME]
               [--os-auth-url OS_AUTH_URL] [--os-region-name OS_REGION_NAME]
               [--os-auth-token OS_AUTH_TOKEN] [--os-no-client-auth]
               [--monasca-api-url MONASCA_API_URL]
               [--monasca-api-version MONASCA_API_VERSION]
               [--os-service-type OS_SERVICE_TYPE]
               [--os-endpoint-type OS_ENDPOINT_TYPE]
               <subcommand> ...

  Command-line interface to the monasca-client API.

  positional arguments:
    <subcommand>
      alarm-definition-create  Create an alarm definition.
      alarm-definition-delete  Delete the alarm definition.
      alarm-definition-list    List alarm definitions for this tenant.
      alarm-definition-patch   Patch the alarm definition.
      alarm-definition-show    Describe the alarm definition.
      alarm-definition-update  Update the alarm definition.
      alarm-delete             Delete the alarm.
      alarm-history            Alarm state history.
      alarm-history-list       List alarms state history.
      alarm-list               List alarms for this tenant.
      alarm-patch              Patch the alarm.
      alarm-show               Describe the alarm.
      alarm-update             Update the alarm.
      measurement-list         List measurements for the specified metric.
      metric-create            Create metric.
      metric-create-raw        Create metric from raw json body.
      metric-list              List metrics for this tenant.
      metric-name-list         List names of metrics.
      metric-statistics        List measurement statistics for the specified metric.
      notification-create      Create notification.
      notification-delete      Delete notification.
      notification-list        List notifications for this tenant.
      notification-show        Describe the notification.
      notification-update      Update notification.
      bash-completion          Prints all of the commands and options to stdout.
      help                     Display help about this program or one of its
                               subcommands.

  optional arguments:
    -j, --json                 output raw json response
    --version                  Shows the client version and exits.
    -d, --debug                Defaults to env[MONASCA_DEBUG].
    -v, --verbose              Print more verbose output.
    -k, --insecure             Explicitly allow the client to perform "insecure" SSL
                               (https) requests. The server's certificate will not
                               be verified against any certificate authorities. This
                               option should be used with caution.
    --cert-file CERT_FILE      Path of certificate file to use in SSL connection.
                               This file can optionally be prepended with the
                               private key.
    --key-file KEY_FILE        Path of client key to use in SSL connection.This
                               option is not necessary if your key is prepended to
                               your cert file.
    --os-cacert OS_CACERT      Specify a CA bundle file to use in verifying a
                               TLS (https) server certificate. Defaults to
                               env[OS_CACERT]. Without either of these, the
                               client looks for the default system CA
                               certificates.
    --timeout TIMEOUT          Number of seconds to wait for a response.
    --os-username OS_USERNAME  Defaults to env[OS_USERNAME].
    --os-password OS_PASSWORD  Defaults to env[OS_PASSWORD].
    --os-project-id OS_PROJECT_ID
                               Defaults to env[OS_PROJECT_ID].
    --os-project-name OS_PROJECT_NAME
                               Defaults to env[OS_PROJECT_NAME].
    --os-domain-id OS_DOMAIN_ID
                               Defaults to env[OS_DOMAIN_ID].
    --os-domain-name OS_DOMAIN_NAME
                               Defaults to env[OS_DOMAIN_NAME].
    --os-auth-url OS_AUTH_URL  Defaults to env[OS_AUTH_URL].
    --os-region-name OS_REGION_NAME
                               Defaults to env[OS_REGION_NAME].
    --os-auth-token OS_AUTH_TOKEN
                               Defaults to env[OS_AUTH_TOKEN].
    --os-no-client-auth        Do not contact keystone for a token. Defaults to
                               env[OS_NO_CLIENT_AUTH].
    --monasca-api-url MONASCA_API_URL
                               Defaults to env[MONASCA_API_URL].
    --monasca-api-version MONASCA_API_VERSION
                               Defaults to env[MONASCA_API_VERSION] or 2_0
    --os-service-type OS_SERVICE_TYPE
                               Defaults to env[OS_SERVICE_TYPE].
    --os-endpoint-type OS_ENDPOINT_TYPE
                               Defaults to env[OS_ENDPOINT_TYPE].

  See "mon help COMMAND" for help on a specific command.


Bash Completion
~~~~~~~~~~~~~~~
Basic command tab completion can be enabled by sourcing the bash completion script.
::

  source /usr/local/share/monasca.bash_completion


Metrics Examples
~~~~~~~~~~~~~~~~
Note:  To see complete usage: 'monasca help' and 'monasca help <command>'

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
  | links                | href:http://192.168.10.4:8080/v2.0/alarm-definitions/4bf6bfc2-c5ac-4d57-b7db-cf5313b05412,rel:self |
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


Python API
----------

There's also a complete Python API.

In order to use the python api directly, you must pass in a valid auth token and
monasca api endpoint, or you can pass in the credentials required by the keystone
client and let the Python API do the authentication.  The user can obtain the token
and endpoint using the keystone client api:
http://docs.openstack.org/developer/python-keystoneclient/.
The service catalog name for our API endpoint is "monasca".

Start using the monascaclient API by constructing the monascaclient client.Client class.
The Client class takes these parameters: api_version, endpoint, and token.
The Client class is used to call all monasca-api resource commands (i.e.
client.Client.metrics.create(fields)).

Long running users of the Client will recieve an indication
that the keystone token has expired when they receive an HTTP response
code of 401 Unauthorized from the monasca-API.  In this case, it is
up to the user to get a new token from keystone which can be passed
into the client.Client.replace_token(token) method.  If you constructed
the Client with all the keystone credentials needed to authenticate,
then the API will automatically try one time to re-authenticate with
keystone whenever the token expires.

The api_version matches the version of the Monasca API.  Currently it is 'v2_0'.

When calling the commands, refer to monascaclient.v2_0.shell.py 'do_<command>'
to see the required and optional fields for each command.
https://github.com/openstack/python-monascaclient/blob/master/monascaclient/v2_0/shell.py

Refer to the example in python-monascaclient/client_api_example.py for more detail::

  from monascaclient import client
  from monascaclient import ksclient
  import monascaclient.exc as exc
  import time

  api_version = '2_0'

  # Authenticate to Keystone
  keystone_url = 'http://keystone:5000/v3'
  ks = ksclient.KSClient(auth_url=keystone_url, username='user', password='password')

  # construct the mon client
  monasca_client = client.Client(api_version, ks.monasca_url, token=ks.token)

  # call the metric-create command
  dimensions = {'instance_id': '12345', 'service': 'hello'}
  fields = {}
  fields['name'] = 'cindy1'
  fields['dimensions'] = dimensions
  fields['timestamp'] = time.time() * 1000
  fields['value'] = 222.333
  try:
      resp = monasca_client.metrics.create(**fields)
  except exc.HTTPException as he:
      print(he.code)
      print(he.message)
  else:
      print(resp)



License
-------

Copyright (c) 2014 Hewlett-Packard Development Company, L.P.

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
