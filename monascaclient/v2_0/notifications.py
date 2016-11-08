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

from monascaclient.common import monasca_manager
from monascaclient.openstack.common.apiclient import base


class Notifications(base.Resource):

    def __repr__(self):
        return "<Notifications %s>" % self._info


class NotificationsManager(monasca_manager.MonascaManager):
    resource_class = Notifications
    base_url = '/notification-methods'

    def create(self, **kwargs):
        """Create a notification."""
        newheaders = self.get_headers()
        resp, body = self.client.json_request('POST', self.base_url,
                                              data=kwargs,
                                              headers=newheaders)
        return body

    def get(self, **kwargs):
        """Get the details for a specific notification."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['notification_id']
        resp, body = self.client.json_request('GET', url_str,
                                              headers=newheaders)
        return body

    def list(self, **kwargs):
        """Get a list of notifications."""
        newheaders = self.get_headers()
        url_str = self.base_url
        if kwargs:
            url_str = url_str + '?%s' % parse.urlencode(kwargs, True)

        resp, body = self.client.json_request('GET', url_str,
                                              headers=newheaders)
        return body['elements'] if type(body) is dict else body

    def delete(self, **kwargs):
        """Delete a notification."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['notification_id']
        resp, body = self.client.json_request(
            'DELETE', url_str, headers=newheaders)
        return resp

    def update(self, **kwargs):
        local_kwargs = deepcopy(kwargs)
        """Update a notification."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % local_kwargs['notification_id']
        del local_kwargs['notification_id']
        resp, body = self.client.json_request(
            'PUT', url_str,
            data=local_kwargs,
            headers=newheaders)
        return body

    def patch(self, **kwargs):
        local_kwargs = deepcopy(kwargs)
        """Patch a notification."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % local_kwargs['notification_id']
        del local_kwargs['notification_id']
        resp, body = self.client.json_request(
            'PATCH', url_str,
            data=local_kwargs,
            headers=newheaders)
        return body
