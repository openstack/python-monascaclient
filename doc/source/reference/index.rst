==========
Python API
==========

There are currently three possible approaches for using the client
directly. On a high level, these approaches can be described as:

* using **username** and **password**
* using **token**
* using existing <session `https://github.com/openstack/keystoneauth/blob/master/keystoneauth1/session.py>_`

There are currently three possible approaches for using the client
directly. On a high level, these approaches can be described as:

* using **username** and **password**
* using **token**
* using existing <session `https://github.com/openstack/keystoneauth/blob/master/keystoneauth1/session.py>_`

Username & password
-------------------

The following approach allows to initialize the monascaclient in a traditional
way.
It requires **username** and  **password**. Initialization of the client
can therefore be executed with::

  c = mon_client.Client(api_version='2_0',
                        username=os.environ.get('OS_USERNAME', 'mini-mon'),
                        password=os.environ.get('OS_PASSWORD', 'password'),
                        auth_url=os.environ.get('OS_AUTH_URL', 'http://127.0.0.1/identity'),
                        project_name=os.environ.get('OS_PROJECT_NAME', 'mini-mon'),
                        endpoint='http://127.0.0.1:8070/v2.0')

Token
-----

In order to use monascaclient directly, you must pass in a valid auth token and
monasca api endpoint, or you can pass in the credentials required by the
keystoneclient and let the Python API do the authentication.  The user can
obtain the token and endpoint using the keystone client api:
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

The session object construction is a much broader topic. It involves picking
one of the following authorization methods:

* Password
* Token

Alternatively, if the Keystone version is known, you may choose:

* V2Password or V3Password
* V2Token of V3Token
* V3OidcClientCredentials
* V3OidcPassword
* V3OidcAuthorizationCode
* V3OidcAccessToken
* V3TOTP
* V3TokenlessAuth

For more details about each one of these methods, please visit
`official documentation <https://docs.openstack.org/keystoneauth/latest/authentication-plugins.html>`_.
