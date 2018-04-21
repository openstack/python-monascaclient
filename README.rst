========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/badges/python-monascaclient.svg
    :target: https://governance.openstack.org/reference/tags/index.html

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

Usage
=====

You'll find complete documentation on the shell by running

``monasca help``::

  usage: monasca [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]
               [--os-cloud <cloud-config-name>]
               [--os-region-name <auth-region-name>]
               [--os-cacert <ca-bundle-file>] [--os-cert <certificate-file>]
               [--os-key <key-file>] [--verify | --insecure]
               [--os-default-domain <auth-domain>]
               [--os-interface <interface>] [--timing] [--os-beta-command]
               [--os-auth-type <auth-type>] [--os-code <auth-code>]
               [--os-protocol <auth-protocol>]
               [--os-project-name <auth-project-name>]
               [--os-trust-id <auth-trust-id>]
               [--os-domain-name <auth-domain-name>]
               [--os-user-domain-id <auth-user-domain-id>]
               [--os-access-token-type <auth-access-token-type>]
               [--os-default-domain-name <auth-default-domain-name>]
               [--os-access-token-endpoint <auth-access-token-endpoint>]
               [--os-access-token <auth-access-token>]
               [--os-domain-id <auth-domain-id>]
               [--os-user-domain-name <auth-user-domain-name>]
               [--os-openid-scope <auth-openid-scope>]
               [--os-user-id <auth-user-id>]
               [--os-identity-provider <auth-identity-provider>]
               [--os-username <auth-username>] [--os-auth-url <auth-auth-url>]
               [--os-client-secret <auth-client-secret>]
               [--os-default-domain-id <auth-default-domain-id>]
               [--os-discovery-endpoint <auth-discovery-endpoint>]
               [--os-client-id <auth-client-id>]
               [--os-project-domain-name <auth-project-domain-name>]
               [--os-project-domain-id <auth-project-domain-id>]
               [--os-password <auth-password>]
               [--os-redirect-uri <auth-redirect-uri>]
               [--os-endpoint <auth-endpoint>] [--os-token <auth-token>]
               [--os-passcode <auth-passcode>]
               [--os-project-id <auth-project-id>]
               [--monasca-api-url MONASCA_API_URL]
               [--monasca-api-version MONASCA_API_VERSION]

  Command-line interface to the OpenStack APIs

  optional arguments:
    --version             show program's version number and exit
    -v, --verbose         Increase verbosity of output. Can be repeated.
    -q, --quiet           Suppress output except warnings and errors.
    --log-file LOG_FILE   Specify a file to log output. Disabled by default.
    -h, --help            Show help message and exit.
    --debug               Show tracebacks on errors.
    --os-cloud <cloud-config-name>
                          Cloud name in clouds.yaml (Env: OS_CLOUD)
    --os-region-name <auth-region-name>
                          Authentication region name (Env: OS_REGION_NAME)
    --os-cacert <ca-bundle-file>
                          CA certificate bundle file (Env: OS_CACERT)
    --os-cert <certificate-file>
                          Client certificate bundle file (Env: OS_CERT)
    --os-key <key-file>   Client certificate key file (Env: OS_KEY)
    --verify              Verify server certificate (default)
    --insecure            Disable server certificate verification
    --os-default-domain <auth-domain>
                          Default domain ID, default=default. (Env:
                          OS_DEFAULT_DOMAIN)
    --os-interface <interface>
                          Select an interface type. Valid interface types:
                          [admin, public, internal]. (Env: OS_INTERFACE)
    --timing              Print API call timing info
    --os-beta-command     Enable beta commands which are subject to change
    --os-auth-type <auth-type>
                          Select an authentication type. Available types:
                          v2token, admin_token, v3oidcauthcode, v2password,
                          v3password, v3oidcaccesstoken, v3oidcpassword, token,
                          v3oidcclientcredentials, v3tokenlessauth, v3token,
                          v3totp, password. Default: selected based on --os-
                          username/--os-token (Env: OS_AUTH_TYPE)
    --os-code <auth-code>
                          With v3oidcauthcode: OAuth 2.0 Authorization Code
                          (Env: OS_CODE)
    --os-protocol <auth-protocol>
                          With v3oidcauthcode: Protocol for federated plugin
                          With v3oidcaccesstoken: Protocol for federated plugin
                          With v3oidcpassword: Protocol for federated plugin
                          With v3oidcclientcredentials: Protocol for federated
                          plugin (Env: OS_PROTOCOL)
    --os-project-name <auth-project-name>
                          With v3oidcauthcode: Project name to scope to With
                          v3password: Project name to scope to With
                          v3oidcaccesstoken: Project name to scope to With
                          v3oidcpassword: Project name to scope to With token:
                          Project name to scope to With v3oidcclientcredentials:
                          Project name to scope to With v3tokenlessauth: Project
                          name to scope to With v3token: Project name to scope
                          to With v3totp: Project name to scope to With
                          password: Project name to scope to (Env:
                          OS_PROJECT_NAME)
    --os-trust-id <auth-trust-id>
                          With v2token: Trust ID With v3oidcauthcode: Trust ID
                          With v2password: Trust ID With v3password: Trust ID
                          With v3oidcaccesstoken: Trust ID With v3oidcpassword:
                          Trust ID With token: Trust ID With
                          v3oidcclientcredentials: Trust ID With v3token: Trust
                          ID With v3totp: Trust ID With password: Trust ID (Env:
                          OS_TRUST_ID)
    --os-domain-name <auth-domain-name>
                          With v3oidcauthcode: Domain name to scope to With
                          v3password: Domain name to scope to With
                          v3oidcaccesstoken: Domain name to scope to With
                          v3oidcpassword: Domain name to scope to With token:
                          Domain name to scope to With v3oidcclientcredentials:
                          Domain name to scope to With v3tokenlessauth: Domain
                          name to scope to With v3token: Domain name to scope to
                          With v3totp: Domain name to scope to With password:
                          Domain name to scope to (Env: OS_DOMAIN_NAME)
    --os-user-domain-id <auth-user-domain-id>
                          With v3password: User's domain id With v3totp: User's
                          domain id With password: User's domain id (Env:
                          OS_USER_DOMAIN_ID)
    --os-access-token-type <auth-access-token-type>
                          With v3oidcauthcode: OAuth 2.0 Authorization Server
                          Introspection token type, it is used to decide which
                          type of token will be used when processing token
                          introspection. Valid values are: "access_token" or
                          "id_token" With v3oidcpassword: OAuth 2.0
                          Authorization Server Introspection token type, it is
                          used to decide which type of token will be used when
                          processing token introspection. Valid values are:
                          "access_token" or "id_token" With
                          v3oidcclientcredentials: OAuth 2.0 Authorization
                          Server Introspection token type, it is used to decide
                          which type of token will be used when processing token
                          introspection. Valid values are: "access_token" or
                          "id_token" (Env: OS_ACCESS_TOKEN_TYPE)
    --os-default-domain-name <auth-default-domain-name>
                          With token: Optional domain name to use with v3 API
                          and v2 parameters. It will be used for both the user
                          and project domain in v3 and ignored in v2
                          authentication. With password: Optional domain name to
                          use with v3 API and v2 parameters. It will be used for
                          both the user and project domain in v3 and ignored in
                          v2 authentication. (Env: OS_DEFAULT_DOMAIN_NAME)
    --os-access-token-endpoint <auth-access-token-endpoint>
                          With v3oidcauthcode: OpenID Connect Provider Token
                          Endpoint. Note that if a discovery document is being
                          passed this option will override the endpoint provided
                          by the server in the discovery document. With
                          v3oidcpassword: OpenID Connect Provider Token
                          Endpoint. Note that if a discovery document is being
                          passed this option will override the endpoint provided
                          by the server in the discovery document. With
                          v3oidcclientcredentials: OpenID Connect Provider Token
                          Endpoint. Note that if a discovery document is being
                          passed this option will override the endpoint provided
                          by the server in the discovery document. (Env:
                          OS_ACCESS_TOKEN_ENDPOINT)
    --os-access-token <auth-access-token>
                          With v3oidcaccesstoken: OAuth 2.0 Access Token (Env:
                          OS_ACCESS_TOKEN)
    --os-domain-id <auth-domain-id>
                          With v3oidcauthcode: Domain ID to scope to With
                          v3password: Domain ID to scope to With
                          v3oidcaccesstoken: Domain ID to scope to With
                          v3oidcpassword: Domain ID to scope to With token:
                          Domain ID to scope to With v3oidcclientcredentials:
                          Domain ID to scope to With v3tokenlessauth: Domain ID
                          to scope to With v3token: Domain ID to scope to With
                          v3totp: Domain ID to scope to With password: Domain ID
                          to scope to (Env: OS_DOMAIN_ID)
    --os-user-domain-name <auth-user-domain-name>
                          With v3password: User's domain name With v3totp:
                          User's domain name With password: User's domain name
                          (Env: OS_USER_DOMAIN_NAME)
    --os-openid-scope <auth-openid-scope>
                          With v3oidcauthcode: OpenID Connect scope that is
                          requested from authorization server. Note that the
                          OpenID Connect specification states that "openid" must
                          be always specified. With v3oidcpassword: OpenID
                          Connect scope that is requested from authorization
                          server. Note that the OpenID Connect specification
                          states that "openid" must be always specified. With
                          v3oidcclientcredentials: OpenID Connect scope that is
                          requested from authorization server. Note that the
                          OpenID Connect specification states that "openid" must
                          be always specified. (Env: OS_OPENID_SCOPE)
    --os-user-id <auth-user-id>
                          With v2password: User ID to login with With
                          v3password: User ID With v3totp: User ID With
                          password: User id (Env: OS_USER_ID)
    --os-identity-provider <auth-identity-provider>
                          With v3oidcauthcode: Identity Provider's name With
                          v3oidcaccesstoken: Identity Provider's name With
                          v3oidcpassword: Identity Provider's name With
                          v3oidcclientcredentials: Identity Provider's name
                          (Env: OS_IDENTITY_PROVIDER)
    --os-username <auth-username>
                          With v2password: Username to login with With
                          v3password: Username With v3oidcpassword: Username
                          With v3totp: Username With password: Username (Env:
                          OS_USERNAME)
    --os-auth-url <auth-auth-url>
                          With v2token: Authentication URL With v3oidcauthcode:
                          Authentication URL With v2password: Authentication URL
                          With v3password: Authentication URL With
                          v3oidcaccesstoken: Authentication URL With
                          v3oidcpassword: Authentication URL With token:
                          Authentication URL With v3oidcclientcredentials:
                          Authentication URL With v3tokenlessauth:
                          Authentication URL With v3token: Authentication URL
                          With v3totp: Authentication URL With password:
                          Authentication URL (Env: OS_AUTH_URL)
    --os-client-secret <auth-client-secret>
                          With v3oidcauthcode: OAuth 2.0 Client Secret With
                          v3oidcpassword: OAuth 2.0 Client Secret With
                          v3oidcclientcredentials: OAuth 2.0 Client Secret (Env:
                          OS_CLIENT_SECRET)
    --os-default-domain-id <auth-default-domain-id>
                          With token: Optional domain ID to use with v3 and v2
                          parameters. It will be used for both the user and
                          project domain in v3 and ignored in v2 authentication.
                          With password: Optional domain ID to use with v3 and
                          v2 parameters. It will be used for both the user and
                          project domain in v3 and ignored in v2 authentication.
                          (Env: OS_DEFAULT_DOMAIN_ID)
    --os-discovery-endpoint <auth-discovery-endpoint>
                          With v3oidcauthcode: OpenID Connect Discovery Document
                          URL. The discovery document will be used to obtain the
                          values of the access token endpoint and the
                          authentication endpoint. This URL should look like
                          https://idp.example.org/.well-known/openid-
                          configuration With v3oidcpassword: OpenID Connect
                          Discovery Document URL. The discovery document will be
                          used to obtain the values of the access token endpoint
                          and the authentication endpoint. This URL should look
                          like https://idp.example.org/.well-known/openid-
                          configuration With v3oidcclientcredentials: OpenID
                          Connect Discovery Document URL. The discovery document
                          will be used to obtain the values of the access token
                          endpoint and the authentication endpoint. This URL
                          should look like https://idp.example.org/.well-known
                          /openid-configuration (Env: OS_DISCOVERY_ENDPOINT)
    --os-client-id <auth-client-id>
                          With v3oidcauthcode: OAuth 2.0 Client ID With
                          v3oidcpassword: OAuth 2.0 Client ID With
                          v3oidcclientcredentials: OAuth 2.0 Client ID (Env:
                          OS_CLIENT_ID)
    --os-project-domain-name <auth-project-domain-name>
                          With v3oidcauthcode: Domain name containing project
                          With v3password: Domain name containing project With
                          v3oidcaccesstoken: Domain name containing project With
                          v3oidcpassword: Domain name containing project With
                          token: Domain name containing project With
                          v3oidcclientcredentials: Domain name containing
                          project With v3tokenlessauth: Domain name containing
                          project With v3token: Domain name containing project
                          With v3totp: Domain name containing project With
                          password: Domain name containing project (Env:
                          OS_PROJECT_DOMAIN_NAME)
    --os-project-domain-id <auth-project-domain-id>
                          With v3oidcauthcode: Domain ID containing project With
                          v3password: Domain ID containing project With
                          v3oidcaccesstoken: Domain ID containing project With
                          v3oidcpassword: Domain ID containing project With
                          token: Domain ID containing project With
                          v3oidcclientcredentials: Domain ID containing project
                          With v3tokenlessauth: Domain ID containing project
                          With v3token: Domain ID containing project With
                          v3totp: Domain ID containing project With password:
                          Domain ID containing project (Env:
                          OS_PROJECT_DOMAIN_ID)
    --os-password <auth-password>
                          With v2password: Password to use With v3password:
                          User's password With v3oidcpassword: Password With
                          password: User's password (Env: OS_PASSWORD)
    --os-redirect-uri <auth-redirect-uri>
                          With v3oidcauthcode: OpenID Connect Redirect URL (Env:
                          OS_REDIRECT_URI)
    --os-endpoint <auth-endpoint>
                          With admin_token: The endpoint that will always be
                          used (Env: OS_ENDPOINT)
    --os-token <auth-token>
                          With v2token: Token With admin_token: The token that
                          will always be used With token: Token to authenticate
                          with With v3token: Token to authenticate with (Env:
                          OS_TOKEN)
    --os-passcode <auth-passcode>
                          With v3totp: User's TOTP passcode (Env: OS_PASSCODE)
    --os-project-id <auth-project-id>
                          With v3oidcauthcode: Project ID to scope to With
                          v3password: Project ID to scope to With
                          v3oidcaccesstoken: Project ID to scope to With
                          v3oidcpassword: Project ID to scope to With token:
                          Project ID to scope to With v3oidcclientcredentials:
                          Project ID to scope to With v3tokenlessauth: Project
                          ID to scope to With v3token: Project ID to scope to
                          With v3totp: Project ID to scope to With password:
                          Project ID to scope to (Env: OS_PROJECT_ID)
    --monasca-api-url MONASCA_API_URL
                          Defaults to env[MONASCA_API_URL].
    --monasca-api-version MONASCA_API_VERSION
                          Defaults to env[MONASCA_API_VERSION] or 2_0

  Commands:
    alarm-count    Count alarms.
    alarm-definition-create  Create an alarm definition.
    alarm-definition-delete  Delete the alarm definition.
    alarm-definition-list  List alarm definitions for this tenant.
    alarm-definition-patch  Patch the alarm definition.
    alarm-definition-show  Describe the alarm definition.
    alarm-definition-update  Update the alarm definition.
    alarm-delete   Delete the alarm.
    alarm-history  Alarm state transition history.
    alarm-history-list  List alarms state history.
    alarm-list     List alarms for this tenant.
    alarm-patch    Patch the alarm state.
    alarm-show     Describe the alarm.
    alarm-update   Update the alarm state.
    complete       print bash completion command
    dimension-name-list  List names of metric dimensions.
    dimension-value-list  List names of metric dimensions.
    help           print detailed help for another command
    measurement-list  List measurements for the specified metric.
    metric-create  Create metric.
    metric-create-raw  Create metric from raw json body.
    metric-list    List metrics for this tenant.
    metric-name-list  List names of metrics.
    metric-statistics  List measurement statistics for the specified metric.
    notification-create  Create notification.
    notification-delete  Delete notification.
    notification-list  List notifications for this tenant.
    notification-patch  Patch notification.
    notification-show  Describe the notification.
    notification-type-list  List notification types supported by monasca.
    notification-update  Update notification.


Bash Completion
---------------

Basic command tab completion can be enabled by sourcing the bash completion script.
::

  monasca completion >> /usr/local/share/monasca.bash_completion


Metrics Examples
----------------

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


Python API
==========

There's also a complete Python API.

There are three possible approaches, at the moment, you can take to use the client
directly. On high level, these approaches can be described as:

* using **username** and **password**
* using **token**
* using existing <session `https://github.com/openstack/keystoneauth/blob/master/keystoneauth1/session.py>_`

Username & password
-------------------

Following approach allows to initialize the monascaclient in a traditional way.
It requires **username** and  **password**. Initialization of the client
can be threfore executed with::

  c = mon_client.Client(api_version='2_0',
                        username=os.environ.get('OS_USERNAME', 'mini-mon'),
                        password=os.environ.get('OS_PASSWORD', 'password'),
                        auth_url=os.environ.get('OS_AUTH_URL', 'http://127.0.0.1/identity'),
                        project_name=os.environ.get('OS_PROJECT_NAME', 'mini-mon'),
                        endpoint='http://127.0.0.1:8070/v2.0')

Token
-----

In order to use the monasclient directly, you must pass in a valid auth token and
monasca api endpoint, or you can pass in the credentials required by the keystone
client and let the Python API do the authentication.  The user can obtain the token
and endpoint using the keystone client api:
http://docs.openstack.org/developer/python-keystoneclient/. Once **token**
is available, a monascaclient can be initialized with following code::

  c = mon_client.Client(api_version='2_0',
                        endpoint='http://127.0.0.1:8070/v2.0'
                        token=token_id,
                        auth_url=os.environ.get('OS_AUTH_URL', 'http://127.0.0.1/identity'),
                        project_name=os.environ.get('OS_PROJECT_NAME', 'mini-mon'))

Session
-------

Usage of the monasclient with existing session can be expressed
with following code::

  from keystoneauth1 import session
  from keystoneauth1 import identity

  auth = identity.Token(auth_url=os.environ.get('OS_AUTH_URL', 'http://127.0.0.1/identity'),
                        token=token_id,
                        project_name=os.environ.get('OS_PROJECT_NAME', 'mini-mon'))
  sess = session.Session(auth=auth)

  c = client.Client(api_version='2_0',
                    endpoint='http://127.0.0.1:8070/v2.0'
                    session=sess)

The session object construction is much broader topic. It involves picking
one of the following authorization methods:

* Password
* Token

Alternatively, if Keystone version is known, you may choose:

* V2Password or V3Password
* V2Token of V3Token
* V3OidcClientCredentials
* V3OidcPassword
* V3OidcAuthorizationCode
* V3OidcAccessToken
* V3TOTP
* V3TokenlessAuth

For more details about each one of those methods, please visit
`official documentation <https://docs.openstack.org/keystoneauth/latest/authentication-plugins.html>`_.

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
