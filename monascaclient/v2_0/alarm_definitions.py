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

from monascaclient.common import monasca_manager
from monascaclient.openstack.common.apiclient import base
from monascaclient.openstack.common.py3kcompat import urlutils


class AlarmDefinitions(base.Resource):

    def __repr__(self):
        return "<AlarmDefinitions %s>" % self._info


class AlarmDefinitionsManager(monasca_manager.MonascaManager):
    resource_class = AlarmDefinitions
    base_url = '/alarm-definitions'

    def create(self, **kwargs):
        """Create an alarm definition."""
        newheaders = self.get_headers()
        resp, body = self.client.json_request('POST', self.base_url,
                                              data=kwargs,
                                              headers=newheaders)
        return body

    def get(self, **kwargs):
        """Get the details for a specific alarm definition."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        resp, body = self.client.json_request('GET', url_str,
                                              headers=newheaders)
        return body

    def list(self, **kwargs):
        """Get a list of alarm definitions."""
        url_str = self.base_url
        newheaders = self.get_headers()
        if 'dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs['dimensions'])
            kwargs['dimensions'] = dimstr

        if kwargs:
            url_str = url_str + '?%s' % urlutils.urlencode(kwargs, True)
        # print url_str
        resp, body = self.client.json_request(
            'GET', url_str, headers=newheaders)
        return body['elements'] if type(body) is dict else body

    def delete(self, **kwargs):
        """Delete a specific alarm definition."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        resp, body = self.client.json_request('DELETE', url_str,
                                              headers=newheaders)
        return resp

    def update(self, **kwargs):
        """Update a specific alarm definition."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        del kwargs['alarm_id']
        resp, body = self.client.json_request('PUT', url_str,
                                              data=kwargs,
                                              headers=newheaders)
        return body

    def patch(self, **kwargs):
        """Patch a specific alarm definition."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        del kwargs['alarm_id']
        resp, body = self.client.json_request('PATCH', url_str,
                                              data=kwargs,
                                              headers=newheaders)
        return body
