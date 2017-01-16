# (C) Copyright 2014-2016 Hewlett Packard Enterprise Development Company LP
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

from six.moves.urllib import parse

from monascaclient.apiclient import base
from monascaclient.common import monasca_manager


class Alarms(base.Resource):

    def __repr__(self):
        return "<Alarms %s>" % self._info


class AlarmsManager(monasca_manager.MonascaManager):
    resource_class = Alarms
    base_url = '/alarms'

    def get(self, **kwargs):
        """Get the details for a specific alarm."""
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        resp, body = self.client.json_request('GET', url_str)
        return body

    def list(self, **kwargs):
        """Get a list of alarms."""
        return self._list('', 'metric_dimensions', **kwargs)

    def delete(self, **kwargs):
        """Delete a specific alarm."""
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        resp, body = self.client.json_request('DELETE', url_str)
        return resp

    def update(self, **kwargs):
        """Update a specific alarm."""
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        del kwargs['alarm_id']
        resp, body = self.client.json_request('PUT', url_str,
                                              data=kwargs)
        return body

    def patch(self, **kwargs):
        """Patch a specific alarm."""
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        del kwargs['alarm_id']
        resp, body = self.client.json_request('PATCH', url_str,
                                              data=kwargs)
        return body

    def count(self, **kwargs):
        url_str = self.base_url + '/count'
        if 'metric_dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs['metric_dimensions'])
            kwargs['metric_dimensions'] = dimstr

        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        resp, body = self.client.json_request('GET', url_str)
        return body

    def history(self, **kwargs):
        """History of a specific alarm."""
        url_str = self.base_url + '/%s/state-history' % kwargs['alarm_id']
        del kwargs['alarm_id']
        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        resp, body = self.client.json_request('GET', url_str)
        return body['elements'] if type(body) is dict else body

    def history_list(self, **kwargs):
        """History list of alarm state."""
        url_str = self.base_url + '/state-history/'
        if 'dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs['dimensions'])
            kwargs['dimensions'] = dimstr
        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        resp, body = self.client.json_request('GET', url_str)
        return body['elements'] if type(body) is dict else body
