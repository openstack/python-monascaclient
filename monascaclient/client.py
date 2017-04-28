# (C) Copyright 2014-2016 Hewlett Packard Enterprise Development LP
# Copyright 2017 Fujitsu LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from keystoneauth1 import identity
from keystoneauth1 import session

from monascaclient.osc import migration
from monascaclient import version


def Client(api_version, **kwargs):

    auth = _get_auth_handler(kwargs)
    sess = _get_session(auth, kwargs)

    client = migration.make_client(
        api_version=api_version,
        session=sess,
        endpoint=kwargs.get('endpoint'),
        service_type=kwargs.get('service_type', 'monitoring')
    )

    return client


def _get_session(auth, kwargs):
    return session.Session(auth=auth,
                           app_name='monascaclient',
                           app_version=version.version_string,
                           cert=kwargs.get('cert', None),
                           timeout=kwargs.get('timeout', None),
                           verify=kwargs.get('verify',
                                             not kwargs.get('insecure',
                                                            False)))


def _get_auth_handler(kwargs):
    if 'token' in kwargs:
        auth = identity.Token(
            auth_url=kwargs.get('auth_url', None),
            token=kwargs.get('token', None),
            project_id=kwargs.get('project_id', None),
            project_name=kwargs.get('project_name', None),
            project_domain_id=kwargs.get('project_domain_id', None),
            project_domain_name=kwargs.get('project_domain_name', None)
        )
    elif {'username', 'password'} <= set(kwargs):
        auth = identity.Password(
            auth_url=kwargs.get('auth_url', None),
            username=kwargs.get('username', None),
            password=kwargs.get('password', None),
            project_id=kwargs.get('project_id', None),
            project_name=kwargs.get('project_name', None),
            project_domain_id=kwargs.get('project_domain_id', None),
            project_domain_name=kwargs.get('project_domain_name', None),
            user_domain_id=kwargs.get('user_domain_id', None),
            user_domain_name=kwargs.get('user_domain_name', None)
        )
    else:
        raise Exception('monascaclient can be configured with either '
                        '"token" or "username:password" but neither of '
                        'them was found in passed arguments.')
    return auth
