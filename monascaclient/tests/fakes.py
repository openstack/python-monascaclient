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

from keystoneauth1.identity import v3
from keystoneauth1.loading import session
from oslo_serialization import jsonutils


def script_keystone_client(token=None):
    auth_params = {'auth_url': 'http://no.where',
                   'project_id': 'project_id',
                   'project_name': 'project_name',
                   'project_domain_id': 'project_domain_id',
                   'project_domain_name': 'project_domain_name'}

    password_params = {'username': 'username',
                       'password': 'password',
                       'user_domain_id': 'user_domain_id',
                       'user_domain_name': 'user_domain_name'}

    if token:
        auth_params['token'] = token
        auth = v3.Token(**auth_params).AndReturn(FakeKeystoneAuth(token, None))
    else:
        auth_params.update(password_params)
        auth = v3.Password(**auth_params).AndReturn(
            FakeKeystoneAuth('abcd1234', 'test'))

    session.Session().load_from_options(
        auth=auth, insecure=False, cacert=None, cert=None, key=None).AndReturn(
            FakeSession(auth))


def fake_headers():
    return {'X-Auth-Token': 'abcd1234',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-monascaclient'}


class FakeSession():

    def __init__(self, auth):
        self.auth = auth

    def get_token(self):
        return self.auth.auth_token

    def get_project_id(self):
        return self.auth.project_id

    def get_endpoint(self, service_type, service_name, interface, region_name):
        return 'http://192.168.1.5:8004/v1/f14b41234'


class FakeKeystoneAuth():

    def __init__(self, auth_token, project_id):
        self.auth_token = auth_token
        self.project_id = project_id

    def get_cache_id_elements(self):
        creds = {
            'password_username': 'username',
            'password_password': 'password'
        }
        return creds


class FakeRaw(object):
    version = 110


class FakeHTTPResponse(object):

    version = 1.1

    def __init__(self, status_code, reason, headers, content):
        self.headers = headers
        self.content = content
        self.status_code = status_code
        self.reason = reason
        self.raw = FakeRaw()

    def getheader(self, name, default=None):
        return self.headers.get(name, default)

    def getheaders(self):
        return self.headers.items()

    def read(self, amt=None):
        b = self.content
        self.content = None
        return b

    def iter_content(self, chunksize):
        return self.content

    def json(self):
        return jsonutils.loads(self.content)
