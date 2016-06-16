# (C) Copyright 2014-2015 Hewlett Packard Enterprise Development Company LP
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

"""
Wrapper around keystoneauth to assist in getting a session, a properly scoped
token and the registered service endpoint for Monasca.

# FIXME(pauloewerton): this is not an appropriate name for this module nor
# for the class. Kept for backwards compatibility.
"""

from keystoneauth1.identity import v3
from keystoneauth1 import loading

from monascaclient import exc


class KSClient(object):

    def __init__(self, **kwargs):
        """Get a session, an endpoint and auth token from Keystone.

        :param username: name of user
        :param password: user's password
        :param user_domain_id: unique identifier of domain the username
                               resides in (optional)
        :param user_domain_name: name of domain for username (optional),
                                 if user_domain_id not specified
        :param project_id: unique identifier of project
        :param project_name: name of project
        :param project_domain_name: name of domain project is in
        :param project_domain_id: id of domain project is in
        :param auth_url: endpoint to authenticate against
        :param token: token to use instead of username/password
        """
        auth_params = {
            'auth_url': kwargs.get('auth_url'),
            'project_id': kwargs.get('project_id'),
            'project_name': kwargs.get('project_name'),
            'project_domain_id': kwargs.get('project_domain_id'),
            'project_domain_name': kwargs.get('project_domain_name')
        }

        password_params = {
            'username': kwargs.get('username'),
            'password': kwargs.get('password'),
            'user_domain_id': kwargs.get('user_domain_id'),
            'user_domain_name': kwargs.get('user_domain_name')
        }

        token = kwargs.get('token')

        if token:
            auth_params['token'] = token
            auth = v3.Token(**auth_params)
        else:
            auth_params.update(password_params)
            auth = v3.Password(**auth_params)

        session_params = {
            'insecure': kwargs.get('insecure'),
            'cacert': kwargs.get('os_cacert'),
            'cert': kwargs.get('cert_file'),
            'key': kwargs.get('key_file')
        }

        self._session = loading.session.Session().load_from_options(
            auth=auth, **session_params)

        self._kwargs = kwargs
        self._token = None
        self._monasca_url = None

    @property
    def session(self):
        """Return the keystoneauth session object used for authentication."""
        return self._session

    @property
    def token(self):
        """Token property

        Validate token is project scoped and return it if its project_id and
        token were fetched when keystoneauth session was created
        """
        if self._token is None:
            if self._session.get_project_id():
                self._token = self._session.get_token()
            else:
                raise exc.CommandError("No project id or project name.")
        return self._token

    @property
    def monasca_url(self):
        """Return the monasca publicURL registered in keystone."""
        service_type = self._kwargs.get('service_type', 'monitoring')
        service_name = self._kwargs.get('service_name', 'monasca')
        interface = self._kwargs.get('endpoint_type', 'public')
        region_name = self._kwargs.get('region_name')

        if not self._monasca_url:
            self._monasca_url = self._session.get_endpoint(
                service_type=service_type, service_name=service_name,
                interface=interface, region_name=region_name)
        return self._monasca_url
