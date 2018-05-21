=========
Using CLI
=========

monasca CLI
-----------

.. toctree::
   :maxdepth: 2

   monasca CLI guide <monasca>
   monasca CLI formatting <monasca-formatting>
   monasca CLI debugging <monasca-debug>


Usage
-----

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

Basic command tab completion can be enabled by sourcing the bash completion
script.

::

   monasca completion >> /usr/local/share/monasca.bash_completion
