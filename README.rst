Python bindings to the Monitoring API
=======================================

This is a client library for Monitoring built to interface with the Monitoring API. It
provides a Python API (the ``monclient`` module) and a command-line tool
(``mon``).

The Monitoring Client was written using the OpenStack Heat Python client as a framework. 

.. contents:: Contents:
   :local:

Ubuntu Install
--------------
Requires:
  - pip - version >= 1.4.  python get-pip.py
  
Install It:
  - sudo pip install python-monclient
  
Alternative Manual Install Steps:
  - cd to your python-monclient repo
  - sudo pip install -r requirements.txt
  - python setup.py install 

Command-line API
----------------
Installing this distribution gets you a shell command, ``mon``, that you
can use to interact with the Monitoring API server.

Usage:
  mon

  mon help

  mon help <command>
  
  mon -j <command>
  
    This outputs the results in jason format.  Normally output is in table format.
  

The monclient CLI needs the Monitoring API endpoint url and the OS_AUTH_TOKEN to pass to the 
Monitoring API RESTful interface.  This is provided through environment or CLI 
parameters.

Environmental Variables
~~~~~~~~~~~~~~~~~~~~~~~  

Environmental variables can be sourced, or optionally passed in as CLI arguments.
It is easiest to source them first and then use the CLI.

When token and endpoint are known::
  
  export OS_AUTH_TOKEN=XXX
  export MON_API_URL=http://192.168.10.4:8080/v2.0/

When using Keystone to obtain the token and endpoint::
  
  export OS_USERNAME=
  export OS_PASSWORD=
  export OS_TENANT_NAME=
  export OS_AUTH_URL=
  export OS_REGION_NAME=

When using Vagrant Environment for test which doesn't use Keystone::
  
  export OS_AUTH_TOKEN=82510970543135
  export OS_NO_CLIENT_AUTH=1
  export MON_API_URL=http://192.168.10.4:8080/v2.0/

The Monitoring API will treat the auth token as the tenant ID when Keystone is not enabled, which is the case for the Vagrant develpment environment.

You'll find complete documentation on the shell by running
``mon help``::
  
  usage: mon [-j] [--version] [-d] [-v] [-k] [--cert-file CERT_FILE]
             [--key-file KEY_FILE] [--ca-file CA_FILE] [--timeout TIMEOUT]
             [--os-username OS_USERNAME] [--os-password OS_PASSWORD]
             [--os-tenant-id OS_TENANT_ID] [--os-tenant-name OS_TENANT_NAME]
             [--os-auth-url OS_AUTH_URL] [--os-region-name OS_REGION_NAME]
             [--os-auth-token OS_AUTH_TOKEN] [--os-no-client-auth]
             [--mon-api-url MON_API_URL] [--mon-api-version MON_API_VERSION]
             [--os-service-type OS_SERVICE_TYPE]
             [--os-endpoint-type OS_ENDPOINT_TYPE]
             <subcommand> ...

  Command-line interface to the mon-client API.
  
  positional arguments:
    <subcommand>
      alarm-create         Create alarm.
      alarm-delete         Delete alarm.
      alarm-history        List alarm state history.
      alarm-list           List alarms for this tenant.
      alarm-patch          Patch the alarm.
      alarm-show           Describe the alarm.
      alarm-update         Update the alarm.
      measurement-list     List measurements for the specified metric.
      metric-create        Create metric.
      metric-create-raw    Create metric from raw json body.
      metric-list          List metrics for this tenant.
      metric-statistics    List measurement statistics for the specified metric.
      notification-create  Create notification.
      notification-delete  Delete notification.
      notification-list    List notifications for this tenant.
      notification-show    Describe the notification.
      notification-update  Update notification.
      bash-completion      Prints all of the commands and options to stdout.
      help                 Display help about this program or one of its
                           subcommands.
  
  optional arguments:
    -j, --json             output raw json response
    --version              Shows the client version and exits.
    -d, --debug            Defaults to env[MON_DEBUG].
    -v, --verbose          Print more verbose output.
    -k, --insecure         Explicitly allow the client to perform "insecure" SSL
                           (https) requests. The server's certificate will not
                           be verified against any certificate authorities. This
                           option should be used with caution.
    --cert-file CERT_FILE  Path of certificate file to use in SSL connection.
                           This file can optionally be prepended with the
                           private key.
    --key-file KEY_FILE    Path of client key to use in SSL connection.This
                           option is not necessary if your key is prepended to
                           your cert file.
    --ca-file CA_FILE      Path of CA SSL certificate(s) used to verify the
                           remote server's certificate. Without this option the
                           client looks for the default system CA certificates.
    --timeout TIMEOUT      Number of seconds to wait for a response.
    --os-username OS_USERNAME
                           Defaults to env[OS_USERNAME].
    --os-password OS_PASSWORD
                           Defaults to env[OS_PASSWORD].
    --os-tenant-id OS_TENANT_ID
                           Defaults to env[OS_TENANT_ID].
    --os-tenant-name OS_TENANT_NAME
                           Defaults to env[OS_TENANT_NAME].
    --os-auth-url OS_AUTH_URL
                           Defaults to env[OS_AUTH_URL].
    --os-region-name OS_REGION_NAME
                           Defaults to env[OS_REGION_NAME].
    --os-auth-token OS_AUTH_TOKEN
                           Defaults to env[OS_AUTH_TOKEN].
    --os-no-client-auth    Do not contact keystone for a token. Defaults to
                           env[OS_NO_CLIENT_AUTH].
    --mon-api-url MON_API_URL
                           Defaults to env[MON_API_URL].
    --mon-api-version MON_API_VERSION
                           Defaults to env[MON_API_VERSION] or 2_0
    --os-service-type OS_SERVICE_TYPE
                           Defaults to env[OS_SERVICE_TYPE].
    --os-endpoint-type OS_ENDPOINT_TYPE
                           Defaults to env[OS_ENDPOINT_TYPE].
  
  See "mon help COMMAND" for help on a specific command.


Bash Completion
~~~~~~~~~~~~~~~
Basic command tab completion can be enabled by sourcing the bash completion script.
::
  
  source /usr/local/share/mon.bash_completion


Metrics Examples
~~~~~~~~~~~~~~~~
Note: this is not meant to be a complete list.

metric-create::
  
  mon metric-create cpu1 123.40
  mon metric-create metric1 1234.56 --dimensions instance_id=123,service=ourservice
  mon metric-create metric1 2222.22 --dimensions instance_id=123,service=ourservice
  mon metric-create metric1 3333.33 --dimensions instance_id=222,service=ourservice

metric-list::
  
  mon metric-list
  +---------+--------------------+
  | name    | dimensions         |
  +---------+--------------------+
  | cpu1    |                    |
  | metric1 | instance_id:123    |
  |         | service:ourservice |
  +---------+--------------------+

measurement-list::
  
  mon measurement-list metric1 2014-01-01T00:00:00Z
  +---------+--------------------+----------------+----------------------+--------------+
  | name    | dimensions         | measurement_id | timestamp            | value        |
  +---------+--------------------+----------------+----------------------+--------------+
  | metric1 | instance_id:123    |     723885     | 2014-05-08T21:46:32Z |      1234.56 |
  |         | service:ourservice |     725951     | 2014-05-08T21:48:50Z |      2222.22 |
  | metric1 | instance_id:222    |     726837     | 2014-05-08T21:49:47Z |      3333.33 |
  |         | service:ourservice |                |                      |              |
  +---------+--------------------+----------------+----------------------+--------------+
  
  mon measurement-list metric1 2014-01-01T00:00:00Z --dimensions instance_id=123
  +---------+--------------------+----------------+----------------------+--------------+
  | name    | dimensions         | measurement_id | timestamp            | value        |
  +---------+--------------------+----------------+----------------------+--------------+
  | metric1 | instance_id:123    |     723885     | 2014-05-08T21:46:32Z |      1234.56 |
  |         | service:ourservice |     725951     | 2014-05-08T21:48:50Z |      2222.22 |
  +---------+--------------------+----------------+----------------------+--------------+
  

Notifications Examples
~~~~~~~~~~~~~~~~~~~~~~
Note: this is not meant to be a complete list.

notification-create::
  
  mon notification-create cindyemail1 EMAIL cindy.employee@hp.com

notification-list::
  
  mon notification-list
  +---------------+--------------------------------------+-------+----------------------+
  | name          | id                                   | type  | address              |
  +---------------+--------------------------------------+-------+----------------------+
  | cindyemail1   | 5651406c-447d-40bd-b868-b2b3e6b59e32 | EMAIL |cindy.employee@hp.com |
  +---------------+--------------------------------------+-------+----------------------+


Alarms Examples
~~~~~~~~~~~~~~~
Note: this is not meant to be a complete list.

alarm-create::
  
  mon alarm-create cpu1alarm 'cpu1>10'
  mon alarm-create cpu2alarm 'cpu1>99' --severity HIGH
  mon alarm-create test1alarm1 'avg(metric1{instance_id=123)>=10' --severity CRITICAL --description 'avg greater than thresh' --alarm-actions 5651406c-447d-40bd-b868-b2b3e6b59e32

alarm-list::
  
  mon alarm-list
  +-------------+--------------------------------------+------------------------------------+--------------+-----------------+
  | name        | id                                   | expression                         | state        | actions_enabled |
  +-------------+--------------------------------------+------------------------------------+--------------+-----------------+
  | cpu1alarm   | 67b9f4cc-3d57-4c6c-848c-555d0b3a8579 | cpu1>10                            | UNDETERMINED | True            |
  | cpu2alarm   | 9e6b9fad-ef1b-4030-beab-10678bcc758a | cpu1>99                            | UNDETERMINED | True            |
  | test1alarm1 | c81e1d40-2115-4557-96f4-eda6b8823fd6 | avg(metric1{instance_id=123}) >= 10| UNDETERMINED | True            |
  +-------------+--------------------------------------+------------------------------------+--------------+-----------------+

alarm-show::
  
  mon alarm-show c81e1d40-2115-4557-96f4-eda6b8823fd6
  +----------------------+----------------------------------------------------------------------------------------------------+
  | Property             | Value                                                                                              |
  +----------------------+----------------------------------------------------------------------------------------------------+
  | actions_enabled      | true                                                                                               |
  | alarm_actions        | [                                                                                                  |
  |                      |   "5651406c-447d-40bd-b868-b2b3e6b59e32"                                                           |
  |                      | ]                                                                                                  |
  | description          | "avg greater than thresh"                                                                          |
  | expression           | "avg(metric1{instance_id=123})>=10"                                                                |
  | expression_data      | function: AVG                                                                                      |
  |                      | metric_name: metric1                                                                               |
  |                      | period: 60                                                                                         |
  |                      | threshold: 10.0                                                                                    |
  |                      | periods: 1                                                                                         |
  |                      | operator: GTE                                                                                      |
  |                      | dimensions: {                                                                                      |
  |                      | instance_id: 123                                                                                   |
  |                      | }                                                                                                  |
  | id                   | "c81e1d40-2115-4557-96f4-eda6b8823fd6"                                                             |
  | links                | href:http://192.168.10.4:8080/v2.0/alarms/c81e1d40-2115-4557-96f4-eda6b8823fd6,rel:self            |
  |                      | href:http://192.168.10.4:8080/v2.0/alarms/c81e1d40-2115-4557-96f4-eda6b8823fd6/history,rel:history |
  | name                 | "test1alarm1"                                                                                      |
  | ok_actions           | []                                                                                                 |
  | severity             | "CRITICAL"                                                                                         |
  | state                | "UNDETERMINED"                                                                                     |
  | undetermined_actions | []                                                                                                 |
  +----------------------+----------------------------------------------------------------------------------------------------+

alarm-patch::
  
  mon alarm-patch c81e1d40-2115-4557-96f4-eda6b8823fd6 --state OK


Python API
----------

There's also a complete Python API.

In order to use the python api directly, you must first obtain an auth token and 
identify the monitoring api endpoint.

The api_version matches the version of the Monitoring API.  Currently it is 'v2_0'.

When calling the commands, refer to monclient.v2_0.shell.py 'do_<command>'
to see the required and optional fields for each command.

Refer to this example in python-monclient/client_api_example.py::
    
  from monclient import client
  import monclient.exc as exc
  import time
   
  api_version = '2_0'
  endpoint = 'http://192.168.10.4:8080/v2.0'
  kwargs = {
      'token': '12345678'
  }
   
  # construct the mon client
  mon_client = client.Client(api_version, endpoint, **kwargs)
   
  # call the metric-create command
  dimensions = {'instance_id': '12345', 'service': 'hello'}
  fields = {}
  fields['name'] = 'cindy1'
  fields['dimensions'] = dimensions
  fields['timestamp'] = time.time()
  fields['value'] = 222.333
  try:
      resp = mon_client.metrics.create(**fields)
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
