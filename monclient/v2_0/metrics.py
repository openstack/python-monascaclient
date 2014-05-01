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

from monclient.common import mon_manager
from monclient.openstack.common.apiclient import base
from monclient.openstack.common.py3kcompat import urlutils


class Metrics(base.Resource):

    def __repr__(self):
        return "<Metrics %s>" % self._info


class MetricsManager(mon_manager.MonManager):
    resource_class = Metrics
    base_url = '/metrics'

    def get_dimensions_url_string(self, dimdict):
        dim_list = list()
        for k, v in dimdict.items():
            dim_str = k + ':' + v
            dim_list.append(dim_str)
        return ','.join(dim_list)

    def create(self, **kwargs):
        """Create a metric."""
        newheaders = self.get_headers()
        resp, body = self.client.json_request('POST', self.base_url,
                                              data=kwargs,
                                              headers=newheaders)
        return resp

    def list(self, **kwargs):
        """Get a list of metrics."""
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
        return body

    def list_measurements(self, **kwargs):
        """Get a list of measurements based on metric definition filters."""
        url_str = self.base_url + '/measurements'
        newheaders = self.get_headers()
        if 'dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs['dimensions'])
            kwargs['dimensions'] = dimstr

        if kwargs:
            url_str = url_str + '?%s' % urlutils.urlencode(kwargs, True)
        # print url_str
        resp, body = self.client.json_request(
            'GET', url_str, headers=newheaders)
        return body
