# (C) Copyright 2014-2016 Hewlett Packard Enterprise Development LP
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

from copy import deepcopy

from six.moves.urllib import parse

from monascaclient.apiclient import base
from monascaclient.common import monasca_manager


class Metrics(base.Resource):

    def __repr__(self):
        return "<Metrics %s>" % self._info


class MetricsManager(monasca_manager.MonascaManager):
    resource_class = Metrics
    base_url = '/metrics'

    def create(self, **kwargs):
        local_kwargs = deepcopy(kwargs)
        """Create a metric."""
        url_str = self.base_url
        newheaders = self.get_headers()
        if 'tenant_id' in local_kwargs:
            url_str = url_str + '?tenant_id=%s' % local_kwargs['tenant_id']
            del local_kwargs['tenant_id']
        if 'jsonbody' in local_kwargs:
            resp, body = self.client.json_request('POST', url_str,
                                                  data=local_kwargs['jsonbody'],
                                                  headers=newheaders)
        else:
            resp, body = self.client.json_request('POST', url_str,
                                                  data=local_kwargs,
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
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        # print url_str
        resp, body = self.client.json_request(
            'GET', url_str, headers=newheaders)
        return body['elements'] if type(body) is dict else body

    def list_names(self, **kwargs):
        """Get a list of metric names."""
        url_str = self.base_url + '/names'
        newheaders = self.get_headers()
        if 'dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs['dimensions'])
            kwargs['dimensions'] = dimstr

        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        # print url_str
        resp, body = self.client.json_request(
            'GET', url_str, headers=newheaders)
        return body['elements'] if type(body) is dict else body

    def list_measurements(self, **kwargs):
        """Get a list of measurements based on metric definition filters."""
        url_str = self.base_url + '/measurements'
        newheaders = self.get_headers()
        if 'dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs['dimensions'])
            kwargs['dimensions'] = dimstr

        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        # print url_str
        resp, body = self.client.json_request(
            'GET', url_str, headers=newheaders)
        return body['elements'] if type(body) is dict else body

    def list_statistics(self, **kwargs):
        """Get a list of measurement statistics based on metric def filters."""
        url_str = self.base_url + '/statistics'
        newheaders = self.get_headers()
        if 'dimensions' in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs['dimensions'])
            kwargs['dimensions'] = dimstr

        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)
        # print url_str
        resp, body = self.client.json_request(
            'GET', url_str, headers=newheaders)
        return body['elements'] if type(body) is dict else body

    def list_dimension_names(self, **kwargs):
        """Get a list of metric dimension names."""
        url_str = self.base_url + '/dimensions/names'
        new_headers = self.get_headers()
        if kwargs:
            url_str += '?%s' % parse.urlencode(kwargs, True)
        # print url_str
        resp, body = self.client.json_request(
            'GET', url_str, headers=new_headers)
        return body['elements'] if type(body) is dict else body

    def list_dimension_values(self, **kwargs):
        """Get a list of metric dimension values."""
        url_str = self.base_url + '/dimensions/names/values'
        new_headers = self.get_headers()
        if kwargs:
            url_str += '?%s' % parse.urlencode(kwargs, True)
        # print url_str
        resp, body = self.client.json_request(
            'GET', url_str, headers=new_headers)
        return body['elements'] if type(body) is dict else body
