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


class MetricsManager(monasca_manager.MonascaManager):
    base_url = '/metrics'

    def create(self, **kwargs):
        """Create a metric."""
        url_str = self.base_url
        if 'tenant_id' in kwargs:
            url_str = url_str + '?tenant_id=%s' % kwargs['tenant_id']
            del kwargs['tenant_id']

        data = kwargs['jsonbody'] if 'jsonbody' in kwargs else kwargs
        body = self.client.create(url=url_str, json=data)
        return body

    def list(self, **kwargs):
        """Get a list of metrics."""
        return self._list('', 'dimensions', **kwargs)

    def list_names(self, **kwargs):
        """Get a list of metric names."""
        return self._list('/names', 'dimensions', **kwargs)

    def list_measurements(self, **kwargs):
        """Get a list of measurements based on metric definition filters."""
        return self._list('/measurements', 'dimensions', **kwargs)

    def list_statistics(self, **kwargs):
        """Get a list of measurement statistics based on metric def filters."""
        return self._list('/statistics', 'dimensions', **kwargs)

    def list_dimension_names(self, **kwargs):
        """Get a list of metric dimension names."""
        return self._list('/dimensions/names', **kwargs)

    def list_dimension_values(self, **kwargs):
        """Get a list of metric dimension values."""
        return self._list('/dimensions/names/values', **kwargs)
