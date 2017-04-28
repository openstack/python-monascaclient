# (C) Copyright 2014-2016 Hewlett Packard Enterprise Development LP
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

from monascaclient.common import monasca_manager


class NotificationsManager(monasca_manager.MonascaManager):
    base_url = '/notification-methods'

    def create(self, **kwargs):
        """Create a notification."""
        body = self.client.create(url=self.base_url,
                                  json=kwargs)
        return body

    def get(self, **kwargs):
        """Get the details for a specific notification."""

        # NOTE(trebskit) should actually be find_one, but
        # monasca does not support expected response format

        url = '%s/%s' % (self.base_url, kwargs['notification_id'])
        resp = self.client.list(path=url)
        return resp

    def list(self, **kwargs):
        """Get a list of notifications."""
        return self._list('', **kwargs)

    def delete(self, **kwargs):
        """Delete a notification."""
        url = self.base_url + '/%s' % kwargs['notification_id']
        resp = self.client.delete(url=url)
        return resp

    def update(self, **kwargs):
        """Update a notification."""
        url_str = self.base_url + '/%s' % kwargs['notification_id']
        del kwargs['notification_id']

        resp = self.client.create(url=url_str,
                                  method='PUT',
                                  json=kwargs)
        return resp

    def patch(self, **kwargs):
        """Patch a notification."""
        url_str = self.base_url + '/%s' % kwargs['notification_id']
        del kwargs['notification_id']

        resp = self.client.create(url=url_str,
                                  method='PATCH',
                                  json=kwargs)

        return resp
