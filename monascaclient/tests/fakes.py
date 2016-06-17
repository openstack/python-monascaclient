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

from keystoneclient.v3 import client as ksclient
from oslo_serialization import jsonutils


def script_keystone_client(token=None):
    if token:
        ksclient.Client(auth_url='http://no.where',
                        insecure=False,
                        tenant_id='tenant_id',
                        token=token).AndReturn(FakeKeystone(token, None))
    else:
        ksclient.Client(auth_url='http://no.where',
                        insecure=False,
                        password='password',
                        project_name='project_name',
                        timeout=20,
                        username='username').AndReturn(FakeKeystone(
                                                       'abcd1234', 'test'))


def fake_headers():
    return {'X-Auth-Token': 'abcd1234',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-monascaclient'}


class FakeServiceCatalog(object):

    def url_for(self, endpoint_type, service_type):
        return 'http://192.168.1.5:8004/v1/f14b41234'


class FakeKeystone(object):
    service_catalog = FakeServiceCatalog()

    def __init__(self, auth_token, project_id):
        self.auth_token = auth_token
        self.project_id = project_id


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
