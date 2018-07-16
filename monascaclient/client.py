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

import logging
import warnings

from keystoneauth1 import identity
from keystoneauth1 import session as k_session

from monascaclient.osc import migration
from monascaclient import version


LOG = logging.getLogger(__name__)
_NO_VALUE_MARKER = object()


def Client(api_version, *args,  **kwargs):

    handle_deprecated(args, kwargs)

    client = migration.make_client(
        api_version=api_version,
        session=_session(kwargs),
        endpoint=kwargs.get('endpoint'),
        service_type=kwargs.get('service_type', 'monitoring')
    )

    return client


def _session(kwargs):
    """Returns or reuses session.

    Method takes care of providing instance of
    session object for the client.

    :param kwargs: all params (without api_version) client was initialized with
    :type kwargs: dict

    :returns: session object
    :rtype keystoneauth1.session.Session

    """
    if 'session' in kwargs:
        LOG.debug('Reusing session')
        sess = kwargs.get('session')
        if not isinstance(sess, k_session.Session):
            msg = ('session should be an instance of %s' % k_session.Session)
            LOG.error(msg)
            raise RuntimeError(msg)
    else:
        LOG.debug('Initializing new session')
        auth = _get_auth_handler(kwargs)
        sess = _get_session(auth, kwargs)
    return sess


def handle_deprecated(args, kwargs):
    """Handles all deprecations.

    Method goes through passed args and kwargs
    and handles all values that are invalid from POV
    of current client but:

    * has their counterparts
    * are candidates to be dropped

    """
    kwargs.update(_handle_deprecated_args(args))
    _handle_deprecated_kwargs(kwargs)


def _handle_deprecated_kwargs(kwargs):

    depr_map = {
        'tenant_name': ('project_name', lambda x: x),
        'insecure': ('verify', lambda x: not x)
    }

    for key, new_key_transform in depr_map.items():
        val = kwargs.get(key, _NO_VALUE_MARKER)
        if val != _NO_VALUE_MARKER:
            new_key = new_key_transform[0]
            new_handler = new_key_transform[1]

            warnings.warn(
                'Usage of {old_key} has been deprecated in favour '
                'of {new_key}. monascaclient will place value of {old_key} '
                'under {new_key}'.format(old_key=key, new_key=new_key),
                DeprecationWarning
            )

            kwargs[new_key] = new_handler(val)
            del kwargs[key]


def _handle_deprecated_args(args):
    kwargs_update = {}
    if args is not None and len(args) > 0:
        warnings.warn(
            'Usage or args is deprecated for the sake of '
            'explicit configuration of the client using '
            'named arguments (**kwargs). '
            'That argument will be removed in future releases.',
            DeprecationWarning
        )
        # have all permissible args set here
        kwargs_update.update({
            'endpoint': args[0]
        })
    return kwargs_update


def _get_session(auth, kwargs):
    return k_session.Session(auth=auth,
                             app_name='monascaclient',
                             app_version=version.version_string,
                             cert=kwargs.get('cert', None),
                             timeout=kwargs.get('timeout', None),
                             verify=kwargs.get('verify', True))


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
