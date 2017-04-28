# (C) Copyright 2014-2016 Hewlett Packard Enterprise Development Company LP
# Copyright 2017 FUJITSU LIMITED
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

from monascaclient.common import monasca_manager


class AlarmsManager(monasca_manager.MonascaManager):
    base_url = '/alarms'

    def get(self, **kwargs):
        """Get the details for a specific alarm."""

        # NOTE(trebskit) should actually be find_one, but
        # monasca does not support expected response format

        url = '%s/%s' % (self.base_url, kwargs['alarm_id'])
        resp = self.client.list(path=url)
        return resp

    def list(self, **kwargs):
        """Get a list of alarms."""
        return self._list('', 'metric_dimensions', **kwargs)

    def delete(self, **kwargs):
        """Delete a specific alarm."""
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        resp = self.client.delete(url_str)
        return resp

    def update(self, **kwargs):
        """Update a specific alarm."""
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        del kwargs['alarm_id']

        body = self.client.create(url=url_str,
                                  method='PUT',
                                  json=kwargs)

        return body

    def patch(self, **kwargs):
        """Patch a specific alarm."""
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        del kwargs['alarm_id']

        resp = self.client.create(url=url_str,
                                  method='PATCH',
                                  json=kwargs)

        return resp

    def count(self, **kwargs):
        url_str = self.base_url + '/count'
        if 'metric_dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(
                kwargs['metric_dimensions'])
            kwargs['metric_dimensions'] = dimstr

        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        body = self.client.list(url_str)
        return body

    def history(self, **kwargs):
        """History of a specific alarm."""
        url_str = self.base_url + '/%s/state-history' % kwargs['alarm_id']
        del kwargs['alarm_id']
        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        resp = self.client.list(url_str)
        return resp['elements'] if type(resp) is dict else resp

    def history_list(self, **kwargs):
        """History list of alarm state."""
        url_str = self.base_url + '/state-history/'
        if 'dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs['dimensions'])
            kwargs['dimensions'] = dimstr
        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        resp = self.client.list(url_str)
        return resp['elements'] if type(resp) is dict else resp
