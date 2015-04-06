# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
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
Wrapper around python keystone client to assist in getting a properly scoped token and the registered service
endpoint for Monasca.
"""

from keystoneclient.v3 import client

from monascaclient import exc


class KSClient(object):
    def __init__(self, **kwargs):
        """Get an endpoint and auth token from Keystone.

        :param username: name of user
        :param password: user's password
        :param project_id: unique identifier of project
        :param project_name: name of project
        :param domain_name: name of domain project is in
        :param domain_id: id of domain project is in
        :param auth_url: endpoint to authenticate against
        :param token: token to use instead of username/password
        """
        kc_args = {'auth_url': kwargs.get('auth_url'),
                   'insecure': kwargs.get('insecure')}

        if kwargs.get('os_cacert'):
            kc_args['cacert'] = kwargs.get('os_cacert')
        if kwargs.get('project_id'):
            kc_args['project_id'] = kwargs.get('project_id')
        elif kwargs.get('project_name'):
            kc_args['project_name'] = kwargs.get('project_name')
            if kwargs.get('domain_name'):
                kc_args['project_domain_name'] = kwargs.get('domain_name')
            if kwargs.get('domain_id'):
                kc_args['project_domain_id'] = kwargs.get('domain_id')

        if kwargs.get('token'):
            kc_args['token'] = kwargs.get('token')
        else:
            kc_args['username'] = kwargs.get('username')
            kc_args['password'] = kwargs.get('password')

        self._kwargs = kwargs
        self._keystone = client.Client(**kc_args)
        self._token = None
        self._monasca_url = None

    @property
    def token(self):
        """Token property

        Validate token is project scoped and return it if it is
        project_id and auth_token were fetched when keystone client was created
        """
        if self._token is None:
            if self._keystone.project_id:
                self._token = self._keystone.auth_token
            else:
                raise exc.CommandError("User does not have a default project. "
                                       "You must provide a project id using "
                                       "--os-project-id or via env[OS_PROJECT_ID], "
                                       "or you must provide a project name using "
                                       "--os-project-name or via env[OS_PROJECT_NAME] "
                                       "and a domain using --os-domain-name, via "
                                       "env[OS_DOMAIN_NAME],  using --os-domain-id or "
                                       "via env[OS_DOMAIN_ID]")
        return self._token

    @property
    def monasca_url(self):
        """Return the monasca publicURL registered in keystone."""
        if self._monasca_url is None:
            if self._kwargs.get('region_name'):
                self._monasca_url = self._keystone.service_catalog.url_for(
                    service_type=self._kwargs.get('service_type') or 'monitoring',
                    attr='region',
                    filter_value=self._kwargs.get('region_name'),
                    endpoint_type=self._kwargs.get('endpoint_type') or 'publicURL')
            else:
                self._monasca_url = self._keystone.service_catalog.url_for(
                    service_type=self._kwargs.get('service_type') or 'monitoring',
                    endpoint_type=self._kwargs.get('endpoint_type') or 'publicURL')
        return self._monasca_url
